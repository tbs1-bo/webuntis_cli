import argparse
import logging
import webuntis
import configparser

class WebuntisCli:
    def __init__(self, untis_user: str, untis_pass: str,
                 server: str, school: str):
        self.session = webuntis.Session(
            username=untis_user,
            password=untis_pass,
            server=server,
            school=school,
            useragent="webuntis_cli")
        self.session.login()

    def run(self):
        self._parsing_args()

    def _parsing_args(self):
        logging.debug("parsing arguments")
        parser = argparse.ArgumentParser()
        parser.add_argument("--lehrer",
                            help="Lehrerkürzel")
        parser.add_argument("--klasse",
                            help="Klassenbezeichnung")
        parser.add_argument("--raum",
                            help="Raumbezeichnung")

        args = parser.parse_args()

        logging.debug("arguments: %s", args)
        if args.lehrer is not None:
            self._handle_lehrer(args.lehrer)
        if args.klasse is not None:
            self._handle_klasse(args.klasse)
        if args.raum is not None:
            self._handle_raum(args.raum)

    def _handle_lehrer(self, kuerzel: str):
        logging.debug("handling lehrer %s", kuerzel)

    def _handle_klasse(self, klassenname: str):
        logging.debug("handling klasse %s", klassenname)

    def _handle_raum(self, raumname: str):
        logging.debug("handling raum %s", raumname)


def main():
    logging.debug("Reading config file")
    config = configparser.ConfigParser()
    config.read("config.ini")
    cred = config['credentials']

    wcli = WebuntisCli(cred['user'], cred['password'],
                       cred['server'], cred['school'])
    wcli.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()