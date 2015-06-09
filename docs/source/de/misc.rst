.. index:: ! Kommandozeilenparameter

Kommandozeilenparameter
=======================

Kommandozeilenparameter für opsi Package Builder

Neben der normalen Fensteroberfläche lassen sich zur Automatisierung einige Funktionen per Kommandozeile aufrufen. Nachfolgend eine Aufstellung der Möglichen Parameter und Kombinationen. Die Parameter können hierbei sowohl in Lang- als auch in Kurzform geschrieben werden (siehe Beipiele unten).

WICHTIG: siehe auch die Hinweise bei Verwendung mehrerer Konfigurationen \ `hier <#MehrereKonfigurationen>`__

+--------------------+--------------------+--------------------+----------------------------+
| Kurz               | Lang               | Beschreibung       | Hinweise                   |
+--------------------+--------------------+--------------------+----------------------------+
| -p                 | --path             | Paketname oder     | Hier kann entweder         |
|                    |                    | -pfad              | der komplette Pfad         |
|                    |                    |                    | zum                        |
|                    |                    |                    | Entwicklungsordner         |
|                    |                    |                    | oder nur der Name          |
|                    |                    |                    | des Pakets                 |
|                    |                    |                    | angegeben sein:            |
|                    |                    |                    |                            |
|                    |                    |                    | Hinweis: ein Pfad          |
|                    |                    |                    | außerhalb des in           |
|                    |                    |                    | den Einstellungen          |
|                    |                    |                    | hinterlegten               |
|                    |                    |                    | Entwicklungsordners        |
|                    |                    |                    | ist nicht                  |
|                    |                    |                    | zulässig.                  |
+--------------------+--------------------+--------------------+----------------------------+
| -w                 | --no-netdrv        | Entwicklungsordner | Falls das Programm         |
|                    |                    | nicht mounten      | so eingestellt             |
|                    |                    |                    | ist, dass es beim          |
|                    |                    |                    | Start zuerst               |
|                    |                    |                    | versucht, die              |
|                    |                    |                    | Freigabe                   |
|                    |                    |                    | opsi\_workbench            |
|                    |                    |                    | als Laufwerk zu            |
|                    |                    |                    | mappen, so kann            |
|                    |                    |                    | das mit dieser             |
|                    |                    |                    | Option deaktiviert         |
|                    |                    |                    | werden. Das ist            |
|                    |                    |                    | dann sinnvoll,             |
|                    |                    |                    | wenn in einem              |
|                    |                    |                    | größeren Script            |
|                    |                    |                    | das Verzeichnis            |
|                    |                    |                    | vorher manuell             |
|                    |                    |                    | zugeordnet wurde.          |
+--------------------+--------------------+--------------------+----------------------------+
| -b                 | --build            | Paketieren         | Diese Option hat           |
|                    |                    |                    | zusätzlich vier            |
|                    |                    |                    | verschiedene               |
|                    |                    |                    | Parameter:                 |
|                    |                    |                    |                            |
|                    |                    |                    |   a)                       |
|                    |                    |                    |   --build=cancel           |
|                    |                    |                    |   Besteht das              |
|                    |                    |                    |   Paket bereits,           |
|                    |                    |                    |   erfolgt keine            |
|                    |                    |                    |   Paketierung              |
|                    |                    |                    |   (Vorgabe).               |
|                    |                    |                    |                            |
|                    |                    |                    |   b)                       |
|                    |                    |                    |   --build=rebuild          |
|                    |                    |                    |   Ein bestehendes          |
|                    |                    |                    |   Paket wird mit           |
|                    |                    |                    |   der gleichen             |
|                    |                    |                    |   Versionierung            |
|                    |                    |                    |   überschrieben.           |
|                    |                    |                    |                            |
|                    |                    |                    |   c) --build=new           |
|                    |                    |                    |   Die                      |
|                    |                    |                    |   Paketversionsnummer      |
|                    |                    |                    |   wird um einen            |
|                    |                    |                    |   Zeitstempel              |
|                    |                    |                    |   erweitert und es         |
|                    |                    |                    |   wird neu                 |
|                    |                    |                    |   paketiert.               |
|                    |                    |                    |                            |
|                    |                    |                    |   d)                       |
|                    |                    |                    |   --build=interactive      |
|                    |                    |                    |   Der Anwender             |
|                    |                    |                    |   wird interaktiv          |
|                    |                    |                    |   um eine                  |
|                    |                    |                    |   Entscheidung             |
|                    |                    |                    |   gebeten (nicht           |
|                    |                    |                    |   mit --quiet),            |
|                    |                    |                    |   falls das Paket          |
|                    |                    |                    |   existiert.               |
|                    |                    |                    |                            |
|                    |                    |                    | Beispiel zum               |
|                    |                    |                    | Zeitstempel der            |
|                    |                    |                    | Variante c):               |
|                    |                    |                    |                            |
|                    |                    |                    |   Paketname mit            |
|                    |                    |                    |   ursprünglicher           |
|                    |                    |                    |   Versionsnummerierung:    |
|                    |                    |                    |   -> productname\_2.5-1    |
|                    |                    |                    |                            |
|                    |                    |                    | Paketname mit              |
|                    |                    |                    | zusätzlichem               |
|                    |                    |                    | Zeitstempel:               |
|                    |                    |                    |                            |
|                    |                    |                    | -> productname\_2.5-1      |
|                    |                    |                    | .corr170739corr            |
|                    |                    |                    |                            |
|                    |                    |                    | Bei Variante c)            |
|                    |                    |                    | werden immer neue          |
|                    |                    |                    | Pakete erzeugt.            |
|                    |                    |                    | Hierbei ist auf            |
|                    |                    |                    | den                        |
|                    |                    |                    | Speicherplatzbedarf        |
|                    |                    |                    | zu achten!                 |
+--------------------+--------------------+--------------------+----------------------------+
| -i                 | --install          | Paket auf opsi     | Sollte in den              |
|                    |                    | Server             | Einstellungen              |
|                    |                    | installieren       | "Depotfunktionen           |
|                    |                    |                    | aktivieren"                |
|                    |                    |                    | gesetzt sein, wird         |
|                    |                    |                    | diese Einstellung          |
|                    |                    |                    | temporär                   |
|                    |                    |                    | deaktiviert und            |
|                    |                    |                    | der ursprünglich           |
|                    |                    |                    | konfigurierte              |
|                    |                    |                    | Installationsbefeh         |
|                    |                    |                    | l                          |
|                    |                    |                    | verwendet.                 |
+--------------------+--------------------+--------------------+----------------------------+
| -s                 | --instsetup        | Paket installieren | Kann nicht mit             |
|                    |                    | und auf allen      | --install                  |
|                    |                    | Clients Aktion auf | kombiniert werden.         |
|                    |                    | "setup" setzen, wo |                            |
|                    |                    | der Produktstatus  |                            |
|                    |                    | "installed" ist    |                            |
+--------------------+--------------------+--------------------+----------------------------+
| -u                 | --uninstall        | Paket auf opsi     | Sollte in den              |
|                    |                    | Server             | Einstellungen              |
|                    |                    | deinstallieren     | "Depotfunktionen           |
|                    |                    |                    | aktivieren"                |
|                    |                    |                    | gesetzt sein, wird         |
|                    |                    |                    | diese Einstellung          |
|                    |                    |                    | temporär                   |
|                    |                    |                    | deaktiviert und            |
|                    |                    |                    | der ursprünglich           |
|                    |                    |                    | konfigurierte              |
|                    |                    |                    | Deinstallationsbef         |
|                    |                    |                    | ehl                        |
|                    |                    |                    | verwendet.                 |
+--------------------+--------------------+--------------------+----------------------------+
| -r                 | --set-rights       | Paketverzeichnisre |                            |
|                    |                    | chte               |                            |
|                    |                    | neu setzen         |                            |
+--------------------+--------------------+--------------------+----------------------------+
| -n                 | --no-gui           | Starte ohne        | Die Ausgabe von            |
|                    |                    | Oberfläche         | Meldungen erfolgt          |
|                    |                    |                    | im aufrufenden CMD         |
|                    |                    |                    | - Fenster.                 |
+--------------------+--------------------+--------------------+----------------------------+
| -x                 | --no-update        | Deaktiviere den    | Überschreibt die           |
|                    |                    | internen Updater   | im Einstellungen           |
|                    |                    | dauerhaft          | Dialog gesetzte            |
|                    |                    |                    | Option.                    |
+--------------------+--------------------+--------------------+----------------------------+
| -q                 | --quiet            | Kein Ausgabe       | Das Programm kehrt         |
|                    |                    |                    | nach Aufruf ohne           |
|                    |                    |                    | weitere Meldungen          |
|                    |                    |                    | zum Prompt zurück.         |
|                    |                    |                    | Ist gleichzeitig           |
|                    |                    |                    | der Parameter              |
|                    |                    |                    | --log angegeben,           |
|                    |                    |                    | so werden                  |
|                    |                    |                    | weiterhin alle             |
|                    |                    |                    | Meldungen in der           |
|                    |                    |                    | Log-Datei                  |
|                    |                    |                    | protokolliert.             |
|                    |                    |                    |                            |
|                    |                    |                    | Hinweis: kann              |
|                    |                    |                    | nicht mit                  |
|                    |                    |                    | --build=interactiv         |
|                    |                    |                    | e                          |
|                    |                    |                    | verwendet werden!          |
+--------------------+--------------------+--------------------+----------------------------+
| -l                 | --log              | | Schreibe         | | Wir nur --log            |
|                    |                    |   sämtliche        |   angegeben, so            |
|                    |                    |   Ausgaben in      |   schreibt opsi            |
|                    |                    |   Log-Datei        |   Package Builder          |
|                    |                    | | (auch bei        |   die Datei                |
|                    |                    |   --quiet)         |   standardmäßig in         |
|                    |                    |                    |   den                      |
|                    |                    |                    |   Ordner                   |
|                    |                    |                    |   %AppData%\\opsi          |
|                    |                    |                    |   PackageBuilder.          |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    | Beispiel um eine           |
|                    |                    |                    | andere Log-Datei           |
|                    |                    |                    | anzulegen:                 |
|                    |                    |                    |                            |
|                    |                    |                    | --log=c:\\temp\\op         |
|                    |                    |                    | sipackagebuilder.l         |
|                    |                    |                    | og                         |
+--------------------+--------------------+--------------------+----------------------------+
| -d                 | --debug            | Schreibe           | Hier werden                |
|                    |                    | zusätzliche Debug  | zusätzliche Debug          |
|                    |                    | Informationen      | Ausgaben erzeugt.          |
|                    |                    |                    | Im Regelfall nicht         |
|                    |                    |                    | benötigt.                  |
|                    |                    |                    |                            |
|                    |                    |                    | Hinweis: kann zu           |
|                    |                    |                    | SEHR viel                  |
|                    |                    |                    | Textausgabe                |
|                    |                    |                    | führen.                    |
+--------------------+--------------------+--------------------+----------------------------+
| -h                 | --help             | Anzeige der Hilfe  | a) --help erzeugt          |
|                    |                    |                    | ein Dialogfenster          |
|                    |                    |                    |                            |
|                    |                    |                    | b) --help --no-gui         |
|                    |                    |                    | gibt die Hilfe auf         |
|                    |                    |                    | der Kommandozeile          |
|                    |                    |                    | aus                        |
+--------------------+--------------------+--------------------+----------------------------+

Verarbeitungsreihenfolge, falls mehrere Prozessparameter angegeben werden:

1.) Rechte setzen -> 2.) Paketieren -> 3.) Deinstallieren (falls existent) -> 4.) Installieren

Wichtig:

Sollten die Depotfunktionen für den normalen GUI Betrieb aktiviert sein, so werden sie bei Verwendung des Schalters --no-gui temporär deaktiviert. Das

Ziel für sämtliche Aktionen ist dann der im Reiter "Allgemein" (Einstellungen) angegebene Konfigserver.

Genauso werden in diesem Fall die ursprünglichen Befehle verwendet, die in den Eingabefeldern des Reiters "opsi Verwaltungsbefehle" (Einstellungen) hinterlegt wurden. Um diese Parameter trotz aktivierter Depotfunktionen für den no-GUI Betrieb zu ändern, wie folgt vorgehen:

    - die Option "Depotfunktionen aktivieren" ausschalten
    - die Befehle in den Eingabefeldern entsprechend abändern
    - Einstellungen speichern
    - die Option "Depotfunktionen aktivieren" einschalten
    - Einstellungen erneut speichern

Hinweis:

Wenn der Parameter --no-gui nicht angegeben ist, öffnet sich zuerst die normale Fensteroberfläche und danach werden sämtliche Prozessschritte abgearbeitet.

**Beispiel 1:**

Langform: opsiPackageBuilder.exe --path=w:\\opsi\\testpak --build=new --no-gui --log=c:\\temp\\opb.log

Kurzform: opsiPackageBuilder.exe -p=w:\\opsi\\testpak -b=new -n -l=c:\\temp\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak, erzeugt bei Vorhandensein ein neues Paket inkl. Zeitstempel und schreibt sämtliche Ausgaben in die Datei C:\\temp\\opb.log.

**Beispiel 2:**

Langform: OPSIPackageBuilder.exe --path=testpak --build=interactive --install --no-gui --log

Kurzform: OPSIPackageBuilder.exe -p=testpak -b=interactive -n -l

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte Entwicklungsordner ist), fragt bei Vorhandensein des Pakets interaktiv nach dem weiteren Vorgehen, installiert das Paket nach Erstellung auf dem Server und schreibt sämtliche Ausgaben in die Datei %AppData%\\opsi PackageBuilder\\opb-session.log.

**Beispiel 3:**

Gemischte Form: OPSIPackageBuilder.exe --path=testpak -b=rebuild --install --uninstall --set-rights -q -l=.\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte Entwicklungsordner ist), setzt die Rechte auf dem Paketordner neu, überschreibt beim Paketieren ein evtl. vorhandenes Paket gleicher Version, deinstalliert die bestehende Version (falls vorhanden) und installiert die gerade neu paketierte Fassung. Auf der Konsole wird nichts ausgegeben, sämtliche Ausgaben gehen in die Log-Datei .\\opb.log.

.. index:: ! Mehrere Konfigurationen

Mehrere Konfigurationen
=======================

**Mehrere Konfigurationen für opsi Package Builder anlegen**

Normalerweise werden sämtliche Konfigurationsoptionen über den Einstellungsdialog definiert. Diese Einstellungen finden sich in der Datei "config.ini" in folgenden Pfaden:

    -  Windows XP: C:\\Dokumente und Einstellungen\\<Benutzer>Anwendungsdaten\\opsiPackageBuilder
    -  höhere Windows Versionen: C:\\Users\\<Benutzer>\\AppData\\Roaming\\opsiPackageBuilder

Um verschiedene Konfigurationen zu nutzen, können in dem jeweiligen Pfad einfach mehrere, unterschiedlich benannte INI-Dateien hinterlegt werden. Beim Start des Programms wird dann nach der zu verwendenden gefragt und diese in "config.ini" umkopiert.

*Beispielhafte Vorgehensweise:*

    -  beim allerersten Start nach der Installation erzwingt opsi Package Builder die Erstellung einer Konfiguration
    -  opsi Package Builder schließen, dann die erstellte Datei config.ini (bspw.) im selben Ordner in die neue Datei produktiv.ini kopieren
    -  beim jetzt folgenden Start fragt opsi Package Builder bereits, welche Konfiguration verwendet werden soll, dies einfach mit OK bestätigen
    -  mit Hilfe des Einstellungedialogs die gewünschte alternative Konfiguration erfassen
    -  opsi Package Builder schließen, dann die geänderte Datei config.ini (bspw.) im selben Ordner in eine weitere Datei testumgebung.ini kopieren

Jetzt liegen zwei getrennte Konfigurationen vor.

Bei jedem nachfolgenden Start wird opsi Package Builder jetzt erst fragen, welche verwendet werden soll und kopiert diese dann entsprechend die Datei config.ini um.

ACHTUNG

Wird opsi Package Builder über die Kommandozeile aufgerufen wird der Auswahldialog ausgeblendet, wenn folgende \ `Parameter <#Kommandozeilenparameter>`__\  verwendet werden:

Es wird in diesem Fall immer die zuletzt gewählte Konfiguration verwendet. Wurde also beim letzten Start per GUI bspw. die "produktiv.ini" ausgewählt, so wird danach beim Start über die Kommandozeile genau diese Konfiguration verwendet.

+--------------------------------------+--------------------------------------+
| -p                                   | --path                               |
+--------------------------------------+--------------------------------------+
| -b                                   | --build                              |
+--------------------------------------+--------------------------------------+
| -i                                   | --install                            |
+--------------------------------------+--------------------------------------+
| -s                                   | --instsetup                          |
+--------------------------------------+--------------------------------------+
| -u                                   | --uninstall                          |
+--------------------------------------+--------------------------------------+
| -r                                   | --set-rights                         |
+--------------------------------------+--------------------------------------+
| -n                                   | --no-gui                             |
+--------------------------------------+--------------------------------------+
| -q                                   | --quiet                              |
+--------------------------------------+--------------------------------------+
| -h                                   | --help                               |
+--------------------------------------+--------------------------------------+

.. index:: ! Rückgabewerte

Return Codes
============

Return Codes

opsi Package Builder gibt bei Ausführung über die Kommandozeile folgende Fehlercodes zurück:

+--------------------------------------+--------------------------------------+
| 0                                    | OK                                   |
+--------------------------------------+--------------------------------------+
| 1010                                 | Can't open project                   |
+--------------------------------------+--------------------------------------+
| 2010                                 | Package file already exists, build   |
|                                      | canceled automatically               |
+--------------------------------------+--------------------------------------+
| 2020                                 | Package could not be deleted before  |
|                                      | re-building                          |
+--------------------------------------+--------------------------------------+
| 2030                                 | Package could not be saved before    |
|                                      | building                             |
+--------------------------------------+--------------------------------------+
| 2090                                 | Undefined error in build routine     |
+--------------------------------------+--------------------------------------+
| 3000                                 | Plink.exe not found                  |
+--------------------------------------+--------------------------------------+
| 3010                                 | PLINK - package exists already       |
+--------------------------------------+--------------------------------------+
| 3020                                 | PLINK - Error while building package |
|                                      | on server, check plink output        |
+--------------------------------------+--------------------------------------+
| 3030                                 | PLINK - Error while installing       |
|                                      | package on server, check plink       |
|                                      | output                               |
+--------------------------------------+--------------------------------------+
| 3040                                 | PLINK - Error while uninstalling     |
|                                      | package on server, check plink       |
|                                      | output                               |
+--------------------------------------+--------------------------------------+
| 5100                                 | Program already running              |
+--------------------------------------+--------------------------------------+
| 5200                                 | No INI file available                |
+--------------------------------------+--------------------------------------+
| 5300                                 | Mode incompatibility: --quiet and    |
|                                      | interactive mode combined on command |
|                                      | line                                 |
+--------------------------------------+--------------------------------------+
| 5400                                 | Incorrect commandline parameters     |
+--------------------------------------+--------------------------------------+
| 5500                                 | Could not allocate console window    |
+--------------------------------------+--------------------------------------+
| 5600                                 | Program exit due to running updater  |
+--------------------------------------+--------------------------------------+

.. index:: ! Systemvoraussetzungen

Systemvoraussetzungen
=====================

(Muss noch geschrieben werden...)

.. index:: ! Weitere Hilfe

Weitere Hilfe...
================

Weitere Hilfe, Anregungen und Tipps finden sich im eigenen Community Bereich des opsi Forums für den opsi Package Builder.

Jegliche Form von sachlicher Kritik, Verbesserungsvorschlägen und Anregung sind natürlich herzlich willkommen.

Zum Community Bereich geht es \ `hier lang <https://forum.opsi.org/viewforum.php?f=22>`__\ !

Copyright © 2013-2015 by Holger Pandel. All Rights Reserved.