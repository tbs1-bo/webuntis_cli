Webuntis CLI
=======================

Eine Kommandozeile für WebUntis - eine Software zum Erstellen und Verwalten von
Stundenplänen in Schulen.

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

Nach dem ersten Aufruf wird eine Konfigurationsdatei angelegt 
`.webuntis-cli.ini` im Home-Verzeichnis des Nutzers angelegt. Diese muss 
bearbeitet und mit den korrekten Nutzerdaten wie Schulname, Server, 
Benutzername und Passwort befüllt werden.
