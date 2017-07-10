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
            useragent="webuntis_cli"
        )
        self.session.login()

    def run(self):
        self.parsing_args()

    def parsing_args(self):
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
        if parser.lehrer is not None:
            pass
        elif parser.klasse is not None:
            pass
        elif parser.raum is not None:
            pass
        else:
            logging.error("No option given!")
            assert raise Exception("No Option given!")


def main():
    logging.debug("Reading config file")
    config = configparser.ConfigParser()
    config.read("config.ini")
    cred = config['credentials']

    wcli = WebuntisCli(cred['user'], cred['password'],
                       cred['server'], cred['school'])
    wcli.parsing_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()