Webuntis CLI
=======================

Eine Kommandozeile für [WebUntis](https://www.untis.at) - einer Software zum 
Erstellen und Verwalten von Stundenplänen in Schulen.


Installation/Upgrade
--------------------

Benutze `pip` (oder `pip3`) für eine einfache Installation. Hierfür muss python
installiert sein. 

Dann erfolgt die Installation über eine Konsole:

    $ pip install --upgrade webuntis-cli

Mit der Option `--upgrade` wird die immer jeweils aktuellste Version 
installiert. 


Benutzung
---------

Das Programm wird mit `webuntis-cli` aufgerufen und verfügt über eine 
Hilfefunktion.

    $ webuntis-cli --help

Nach dem ersten Aufruf wird die Konfigurationsdatei  
`.webuntis-cli.ini` im Home-Verzeichnis des Nutzers angelegt. Diese muss 
bearbeitet und mit den korrekten Nutzerdaten wie Schulname, Server, 
Benutzername und Passwort befüllt werden.

### Beispiele

Ein Aufruf für den aktuellen Stundenplan von Herr Mustermann würde wie folgt
aussehen:

    $ webuntis-cli --lehrer Mustermann    

Es können auch mehrere Personen angegeben werden:

    $ webuntis-cli --lehrer Mustermann Musterfrau
    
Ebeso können die Pläne für verschiedene Räume oder Klassen angezeigt werden.

    $ webuntis-cli --raum 12 13 14
    $ webuntis-cli --klasse 10a 10b 10c


Probleme oder Fehler
-------------------

Wenn dir ein Fehler auffällt, so kannst du ihn einfach über den [Bugtracker bei
github](https://github.com/tbs1-bo/webuntis_cli/issues/new) melden.
