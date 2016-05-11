.. index:: ! Kommandozeilenparameter

Kommandozeilenparameter
=======================

Kommandozeilenparameter für opsi PackageBuilder

Neben der normalen Fensteroberfläche lassen sich zur Automatisierung viele Funktionen per Kommandozeile aufrufen. Nachfolgend eine Aufstellung der Möglichen Parameter und Kombinationen. Die Parameter können hierbei sowohl in Lang- als auch in Kurzform geschrieben werden (siehe Beipiele unten).

WICHTIG: siehe auch die Hinweise bei Verwendung :ref:`mehrerer Konfigurationen <multiple_configs>`.

+--------------------+--------------------+--------------------+----------------------------+
| Kurz               | Lang               | Beschreibung       | Hinweise                   |
+====================+====================+====================+============================+
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
|                    |                    |                    |   Paketversionsnummer um   |
|                    |                    |                    |   eine incrementierte      |
|                    |                    |                    |   Markierung               |
|                    |                    |                    |   erweitert und es         |
|                    |                    |                    |   wird neu                 |
|                    |                    |                    |   paketiert.               |
|                    |                    |                    |                            |
|                    |                    |                    | Beispiel zum               |
|                    |                    |                    | Zeitstempel der            |
|                    |                    |                    | Variante c):               |
|                    |                    |                    |                            |
|                    |                    |                    |   Paketname mit            |
|                    |                    |                    |   ursprünglicher           |
|                    |                    |                    |   Versionsnummerierung:    |
|                    |                    |                    |                            |
|                    |                    |                    |   -> productname\_2.5-1    |
|                    |                    |                    |                            |
|                    |                    |                    | Paketname mit              |
|                    |                    |                    | autom. Markierun:          |
|                    |                    |                    |                            |
|                    |                    |                    |   -> productname\_2.5-1    |
|                    |                    |                    |   .corr1corr               |
|                    |                    |                    |                            |
|                    |                    |                    | *Bei Variante c)           |
|                    |                    |                    | werden immer neue          |
|                    |                    |                    | Pakete erzeugt.            |
|                    |                    |                    | Hierbei ist auf            |
|                    |                    |                    | den                        |
|                    |                    |                    | Speicherplatzbedarf        |
|                    |                    |                    | zu achten!*                |
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
| -s                 | --instsetup        | Paket installieren | *Kann nicht mit            |
|                    |                    | und auf allen      | --install                  |
|                    |                    | Clients Aktion auf | kombiniert werden.*        |
|                    |                    | "setup" setzen, wo |                            |
|                    |                    | der Produktstatus  |                            |
|                    |                    | "installed" ist    |                            |
+--------------------+--------------------+--------------------+----------------------------+
| -u                 | --uninstall        | Paket auf opsi     |                            |
|                    |                    | Server             |                            |
|                    |                    | deinstallieren     |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
|                    |                    |                    |                            |
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
+--------------------+--------------------+--------------------+----------------------------+
| -l                 | --log              | Schreibe           | Wir die Logdatei           |
|                    |                    | sämtliche          | mit relativem Pfad         |
|                    |                    | Ausgaben in        | angegeben, so schreibt     |
|                    |                    | Log-Datei          | opsi PackageBuilder in     |
|                    |                    |                    | einen temporären Ordner.   |
|                    |                    |                    | Windows:                   |
|                    |                    |                    |                            |
|                    |                    |                    |    %AppData%\Local\Temp    |
|                    |                    |                    |                            |
|                    |                    |                    | Linux:                     |
|                    |                    |                    |                            |
|                    |                    |                    |    /tmp                    |
|                    |                    |                    |                            |
|                    |                    |                    | Beispiel um eine           |
|                    |                    |                    | Log-Datei                  |
|                    |                    |                    | anzulegen:                 |
|                    |                    |                    |                            |
|                    |                    |                    | --log=c:\\temp\\op         |
|                    |                    |                    | sipackagebuilder.l         |
|                    |                    |                    | og                         |
+--------------------+--------------------+--------------------+----------------------------+
| <keine>            | --log-level        | Gibt die           | Es werden ja Stufe         |
|                    |                    | Protokollstufe an  | zusätzliche Meldungen      |
|                    |                    |                    | ausgegeben.                |
|                    |                    |                    |                            |
|                    |                    |                    | Folgende Logstufen sind    |
|                    |                    |                    | möglich (aufsteigende      |
|                    |                    |                    | Anzahl an Meldungen:       |
|                    |                    |                    |                            |
|                    |                    |                    |     CRITICAL               |
|                    |                    |                    |     ERROR                  |
|                    |                    |                    |     SSH                    |
|                    |                    |                    |     WARNING                |
|                    |                    |                    |     SSHINFO                |
|                    |                    |                    |     INFO                   |
|                    |                    |                    |     DEBUG                  |
|                    |                    |                    |                            |
|                    |                    |                    | *DEBUG erzeugt SEHR viele  |
|                    |                    |                    | Meldungen.*                |
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


*Hinweis:*
Wenn der Parameter --no-gui nicht angegeben ist, öffnet sich die normale Fensteroberfläche und es werden sämtliche Prozessschritte abgearbeitet.

**Beispiel 1:**

Langform: opsiPackageBuilder.exe --path=w:\\opsi\\testpak --build=new --no-gui --log=c:\\temp\\opb.log

Kurzform: opsiPackageBuilder.exe -p=w:\\opsi\\testpak -b=new -n -l=c:\\temp\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak, erzeugt bei Vorhandensein ein neues Paket inkl. Zeitstempel und schreibt sämtliche Ausgaben in die Datei C:\\temp\\opb.log.

**Beispiel 2:**

Langform: opsiPackageBuilder.exe --path=testpak --build=interactive --install --no-gui --log

Kurzform: opsiPackageBuilder.exe -p=testpak -b=interactive -n -l

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte Entwicklungsordner ist), fragt bei Vorhandensein des Pakets interaktiv nach dem weiteren Vorgehen, installiert das Paket nach Erstellung auf dem Server und schreibt sämtliche Ausgaben in die Datei %AppData%\\Local\\Temp\\opb-session.log.

**Beispiel 3:**

Gemischte Form: OPSIPackageBuilder.exe --path=testpak -b=rebuild --install --uninstall --set-rights -q -l=.\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte Entwicklungsordner ist), setzt die Rechte auf dem Paketordner neu, überschreibt beim Paketieren ein evtl. vorhandenes Paket gleicher Version, deinstalliert die bestehende Version (falls vorhanden) und installiert die gerade neu paketierte Fassung. Auf der Konsole wird nichts ausgegeben, sämtliche Ausgaben gehen in die Log-Datei .\\opb.log.

.. index:: ! Mehrere Konfigurationen

.. _multiple_configs:

Mehrere Konfigurationen (DERZEIT NICHT VERFÜGBAR)
=================================================

**Mehrere Konfigurationen für opsi PackageBuilder anlegen**

Normalerweise werden sämtliche Konfigurationsoptionen über den Einstellungsdialog definiert. Diese Einstellungen finden sich in der Datei "config.ini" in folgenden Pfaden:

    -  Windows XP: C:\\Dokumente und Einstellungen\\<Benutzer>Anwendungsdaten\\opsiPackageBuilder
    -  höhere Windows Versionen: C:\\Users\\<Benutzer>\\AppData\\Roaming\\opsiPackageBuilder

Um verschiedene Konfigurationen zu nutzen, können in dem jeweiligen Pfad einfach mehrere, unterschiedlich benannte INI-Dateien hinterlegt werden. Beim Start des Programms wird dann nach der zu verwendenden gefragt und diese in "config.ini" umkopiert.

*Beispielhafte Vorgehensweise:*

    -  beim allerersten Start nach der Installation erzwingt opsi PackageBuilder die Erstellung einer Konfiguration
    -  opsi PackageBuilder schließen, dann die erstellte Datei config.ini (bspw.) im selben Ordner in die neue Datei produktiv.ini kopieren
    -  beim jetzt folgenden Start fragt opsi PackageBuilder bereits, welche Konfiguration verwendet werden soll, dies einfach mit OK bestätigen
    -  mit Hilfe des Einstellungedialogs die gewünschte alternative Konfiguration erfassen
    -  opsi PackageBuilder schließen, dann die geänderte Datei config.ini (bspw.) im selben Ordner in eine weitere Datei testumgebung.ini kopieren

Jetzt liegen zwei getrennte Konfigurationen vor.

Bei jedem nachfolgenden Start wird opsi PackageBuilder jetzt erst fragen, welche verwendet werden soll und kopiert diese dann entsprechend die Datei config.ini um.

**ACHTUNG:**

Wird opsi PackageBuilder über die Kommandozeile aufgerufen wird der Auswahldialog ausgeblendet, wenn folgende \ `Parameter <#Kommandozeilenparameter>`__\  verwendet werden:

Es wird in diesem Fall immer die zuletzt gewählte Konfiguration verwendet. Wurde also beim letzten Start per GUI bspw. die "produktiv.ini" ausgewählt, so wird danach beim Start über die Kommandozeile genau diese Konfiguration verwendet.

+--------------------------------------+--------------------------------------+
| Kurz                                 | Lang                                 |
+======================================+======================================+
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

opsi PackageBuilder gibt bei Ausführung über die Kommandozeile folgende Fehlercodes zurück:

+-----------------------+---------------------------------------------------------------------------------------+
| Internal name and val | Description                                                                           |
+=======================+=======================================================================================+
| RET_OK = 0            | Err  0: OK                                                                            |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_EOPEN = 10        | Err 10: Can't open project                                                            |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_BCANCEL = 20      | Err 20: Package file already exists, build canceled automatically                     |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_BFILEDEL = 21     | Err 21: Package could not be deleted before re-building                               |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_BSAVE = 22        | Err 22: Package could not be saved before building                                    |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_BUNDEF = 23       | Err 23: Undefined error in build routine                                              |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_SSHCONNERR = 25   | Err 25: Can't establish SSH connection                                                |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_SSHCMDERR = 26    | Err 26: Error during command execution via SSH                                        |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PEXISTS = 30      | Err 30: SSH - Package exists already                                                  |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PBUILD = 31       | Err 31: SSH - Error while building package on server                                  |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PINSTALL = 32     | Err 32: SSH - Error while installing package on server                                |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PINSTSETUP = 33   | Err 33: SSH - Error while installing package on server or activating for setup        |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PUNINSTALL = 34   | Err 34: SSH - Error while uninstalling package on server                              |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PUPLOAD = 35      | Err 34: SSH - Error while uploading package on server                                 |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_SINGLETON = 51    | Err 51: Program already running                                                       |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_NOINI = 52        | Err 52: No INI file available                                                         |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_QICOMB = 53       | Err 53: Mode incompatibility: --quiet and interactive mode combined on command line   |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_CMDLINE = 54      | Err 54: Incorrect commandline parameters                                              |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_NOWINEXE = 57     | Err 57: Winexe not found                                                              |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_PRODUPDRUN = 58   | Err 58: opsi-product-updater already running                                          |
+-----------------------+---------------------------------------------------------------------------------------+
| RET_NOREPO = 59       | Err 59: could not get repo content                                                    |
+-----------------------+---------------------------------------------------------------------------------------+

.. index:: ! Systemvoraussetzungen

Systemvoraussetzungen
=====================

(Muss noch geschrieben werden...)

.. index:: ! Weitere Hilfe

Weitere Hilfe...
================

Weitere Hilfe, Anregungen und Tipps finden sich im eigenen Community Bereich des opsi Forums für den opsi PackageBuilder.

Jegliche Form von sachlicher Kritik, Verbesserungsvorschlägen und Anregung sind natürlich herzlich willkommen.

Zum Community Bereich geht es `hier lang <https://forum.opsi.org/viewforum.php?f=22>`__.

Copyright © 2013-2016 by Holger Pandel. All Rights Reserved.