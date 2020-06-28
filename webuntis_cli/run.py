import argparse
import logging
import webuntis
# Doc: https://python-webuntis.readthedocs.io/en/latest/objects.html
import webuntis.objects
import webuntis_cli
import configparser
import datetime
import locale
import os
import stat
import getpass


class WebuntisCli:
    def __init__(self, untis_user: str, untis_pass: str,
                 server: str, school: str):
        self.session = webuntis.Session(
            username=untis_user,
            password=untis_pass,
            server=server,
            school=school,
            useragent="webuntis_cli")
        self.days = 5
        self.session.login()
        self.start = datetime.datetime.now()

    def run(self):
        self._parse_args()

    def _create_parser(self):
        logging.debug("parsing arguments")
        parser = argparse.ArgumentParser()
        parser.epilog = "version " + webuntis_cli.VERSION
        parser.description = "Kommandozeilen-Client für WebUntis"
        parser.add_argument("--lehrer", "-l", nargs='*',
                            help="Ein oder mehrere Nachnamen von Lehrern")
        parser.add_argument("--klasse", "-k", nargs='*',
                            help="Ein oder mehrere Klassenbezeichnungen")
        parser.add_argument("--raum", "-r", nargs='*',
                            help="Ein oder mehrere Raumbezeichnungen")
        parser.add_argument("--tage", "-t", type=int,
                            default=5,
                            help="Anzahl Tage, die der Plan umfassen soll "
                                 "(Standard: 5)")
        parser.add_argument("--start", "-s",
                            help="Startdatum des Planes im Format 02.12. "
                                 "(Standard: heute)")

        return parser

    def _parse_args(self):
        parser = self._create_parser()
        args = parser.parse_args()
        if self._required_option_missing(args):
            parser.print_help()
            return
        self.days = args.tage - 1

        if args.start:
            start = datetime.datetime.strptime(args.start, "%d.%m.")
            self.start = start.replace(year = datetime.datetime.now().year)

        logging.debug("arguments: %s", args)
        if args.lehrer is not None:
            for l in args.lehrer:
                self._handle_lehrer(l)
                print()
        if args.klasse is not None:
            for k in args.klasse:
                self._handle_klasse(k)
                print()
        if args.raum is not None:
            for r in args.raum:
                self._handle_raum(r)
                print()

    def _required_option_missing(self, args):
        return (args.lehrer is None and
                args.klasse is None and
                args.raum is None)

    def _handle_lehrer(self, surname: str):
        logging.debug("handling lehrer %s", surname)
        lehrer = self.session.teachers().filter(surname=surname)
        if len(lehrer) != 1:
            print("Lehrer nicht gefunden: ", surname)
            return

        tt = self._create_timetable(lehrer[0])
        self._print_timetable(tt)

    def _handle_klasse(self, klassenname: str):
        logging.debug("handling klasse %s", klassenname)
        klassen = self.session.klassen().filter(name=klassenname)
        if len(klassen) != 1:
            print("Klasse nicht gefunden", klassenname)
            return
        tt = self._create_timetable(klassen[0])
        self._print_timetable(tt)

    def _handle_raum(self, raumname: str):
        logging.debug("handling raum %s", raumname)
        rooms = self.session.rooms().filter(name=raumname)
        if len(rooms) != 1:
            print("Raum nicht gefunden", raumname)
            return
        tt = self._create_timetable(rooms[0])
        self._print_timetable(tt)

        # TODO _handle_* Methoden zusammenfassen

    def _create_timetable(self, reference) -> webuntis.objects.PeriodList:
        """Create a time table for a teacher, klasse or room.

        :param reference: teacher, klasse or room object"""
        start = self.start.replace(day=self.start.day, month=self.start.month)
        end = start + datetime.timedelta(days=self.days)

        current_year = self.session.schoolyears().current
        assert current_year.start <= start <= current_year.end, f"Start date not in current school year {start}"
        assert current_year.start <= end <= current_year.end, f"End date not in current school year {end}"

        logging.debug("creating time table between %s and %s", start, end)

        args = dict(start=start, end=end)
        if isinstance(reference, webuntis.objects.TeacherObject):
            args['teacher'] = reference
        elif isinstance(reference, webuntis.objects.KlassenObject):
            args['klasse'] = reference
        elif isinstance(reference, webuntis.objects.RoomObject):
            args['room'] = reference

        return self.session.timetable(**args)

    def _print_timetable(self, timetable: webuntis.objects.PeriodList):
        logging.debug("sorting time table by starting time")
        tt = list(timetable)
        tt = sorted(tt, key=lambda x: x.start)
        logging.debug("printing timetable")
        time_format_end = "%H:%M"
        time_format_start = "%Y-%m-%d %a " + time_format_end

        for po in tt:
            s = po.start.strftime(time_format_start)
            e = po.end.strftime(time_format_end)
            k = " ".join([k.name for k in po.klassen])
            t = " ".join([t.name for t in po.teachers])
            r = " ".join([r.name for r in po.rooms])
            sub = " ".join([r.name for r in po.subjects])
            c = "(" + po.code + ")" if po.code is not None else ""
            print(s + "-" + e, k, sub, t, r, c)


class Configuration:
    def __init__(self):
        self.configfile = os.path.expanduser('~/.webuntis-cli.ini')
        self.config = configparser.ConfigParser()
        self._create_default_if_missing()

        if 'password' not in self.config['credentials']:
            logging.debug("No password found in config file. Asking user")
            self.config['credentials']['password'] = \
                getpass.getpass("Passwort eingeben:")

    def _create_default_if_missing(self):
        if not os.path.isfile(self.configfile):
            logging.debug("No config file found. Creating %s", self.configfile)
            self.config['credentials'] = {
                "user": "user",
                "password": "123",
                "server": "https://server.webuntis.com",
                "school": "your-school"
            }
            with open(self.configfile, 'w') as f:
                self.config.write(f)

            # change file permissions to 600
            os.chmod(self.configfile, stat.S_IRUSR | stat.S_IWUSR)

            print("Passe die Einträge in der Konfigurationsdatei an: ",
                  self.configfile)
            exit(0)

        else:
            self.config.read(self.configfile)


def main():
    # setting locale to the default language
    locale.setlocale(locale.LC_ALL, '')

    if 'WEBUNTIS_CLI_DEBUG' in os.environ:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("environment var found. enabling debugging")

    logging.debug("Reading config file")
    config = Configuration()
    cred = config.config['credentials']

    wcli = WebuntisCli(cred['user'], cred['password'],
                       cred['server'], cred['school'])
    wcli.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
