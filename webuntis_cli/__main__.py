import argparse
import logging
import webuntis
# Doc: https://python-webuntis.readthedocs.io/en/latest/objects.html
import webuntis.objects
import configparser
import datetime
import locale


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

    def run(self):
        self._parse_args()

    def _create_parser(self):
        logging.debug("parsing arguments")
        parser = argparse.ArgumentParser()
        parser.description = "Kommandozeilen-Client für WebUntis."
        parser.add_argument("--lehrer", nargs='*',
                            help="Lehrerkürzel")
        parser.add_argument("--klasse", nargs='*',
                            help="Klassenbezeichnung")
        parser.add_argument("--raum", nargs='*',
                            help="Raumbezeichnung")
        parser.add_argument("--tage", type=int,
                            default=5,
                            help="Anzahl Tage für den Plan (Standard: 5)")
        return parser

    def _parse_args(self):
        parser = self._create_parser()

        args = parser.parse_args()
        self.days = args.tage - 1

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
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=self.days)

        if isinstance(reference, webuntis.objects.TeacherObject):
            logging.debug("Creating time table for teacher from % til %s",
                          reference, start, end)
            return self.session.timetable(start=start, end=end,
                                          teacher=reference)
        elif isinstance(reference, webuntis.objects.KlassenObject):
            return self.session.timetable(start=start, end=end,
                                          klasse=reference)
        elif isinstance(reference, webuntis.objects.RoomObject):
            return self.session.timetable(start=start, end=end,
                                          room=reference)

    def _print_timetable(self, timetable: webuntis.objects.PeriodList):
        logging.debug("sorting time table by starting time")
        tt = list(timetable)
        tt = sorted(tt, key=lambda x: x.start)
        logging.debug("printing timetable")
        time_format_end = "%H:%M"
        time_format_start = "%a " + time_format_end
        for po in tt:
            s = po.start.strftime(time_format_start)
            e = po.end.strftime(time_format_end)
            k = " ".join([k.name for k in po.klassen])
            t = " ".join([t.name for t in po.teachers])
            r = " ".join([r.name for r in po.rooms])
            print(s, e, k, t, r)


def main():
    # setting locale to the default language
    locale.setlocale(locale.LC_ALL, '')


    logging.debug("Reading config file")
    config = configparser.ConfigParser()
    config.read("config.ini")
    cred = config['credentials']

    wcli = WebuntisCli(cred['user'], cred['password'],
                       cred['server'], cred['school'])
    wcli.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
