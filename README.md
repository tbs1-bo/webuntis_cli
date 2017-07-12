Das Projekt `webuntis-cli` stellt eine Kommandozeile
für [WebUntis](https://www.untis.at) zur Verfügung. Bei Webuntis
handelt es sich um eine Software zum Erstellen und Verwalten von
Stundenplänen in Schulen.


Installation/Upgrade
====================

Benutze `pip` (oder `pip3`) für eine einfache Installation. Hierfür muss 
[python](https://www.python.org) installiert sein. 

    $ pip install --upgrade webuntis-cli

Mit der Option `--upgrade` wird immer die jeweils aktuelle Version installiert. 


Benutzung
=========

Nach der Installation steht der Befehl `webuntis-cli` zur Verfügung. Dieser 
verfügt über eine Hilfefunktion.

    $ webuntis-cli --help

Nach dem ersten Aufruf wird die Konfigurationsdatei  `.webuntis-cli.ini` im 
Home-Verzeichnis des Nutzers angelegt. Diese muss bearbeitet und mit den 
korrekten Nutzerdaten wie Schulname, Server, Benutzername und Passwort befüllt 
werden.

Beispiele
---------

Ein Aufruf für den aktuellen Stundenplan von Herr Mustermann würde wie folgt
aussehen:

    $ webuntis-cli --lehrer Mustermann    

Es können auch mehrere Personen angegeben werden:

    $ webuntis-cli --lehrer Mustermann Musterfrau
    
Ebeso können die Pläne für verschiedene Räume oder Klassen angezeigt werden.

    $ webuntis-cli --raum 12 13 14
    $ webuntis-cli --klasse 10a 10b 10c


Probleme oder Fehler
====================

Wenn dir ein Fehler auffällt, so kannst du ihn einfach über den [Bugtracker bei
github](https://github.com/tbs1-bo/webuntis_cli/issues/new) melden. Hierfür 
benötigst du einen einen Account bei github.
