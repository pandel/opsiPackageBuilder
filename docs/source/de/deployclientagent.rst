Client Agent verteilen
======================

|image73|

**Erläuterung zur Option "Nicht warten":**

Wird diese Option angewählt, so wird der Deploy Befehl auf dem Server abgesetzt und nicht auf die Beendigung der Ausführung gewartet, d. h. es gibt keine Rückmeldung über das PLINK Log. Bei größeren Deploys führt das dazu, dass der opsi PackageBuilder nicht "ewig" zu hägen scheint, sondern man kann direkt weiterarbeiten.

Hinweise zum Feld "Vorab-Befehl":

Steht in diesem Fehle eine Anweisung, so wird sie vor dem Deploy via winexe (entspricht weitestgehend psexec für Linux) direkt auf dem Client ausgeführt.

Daran sind allerdings einige Bedingungen geknüpft:

    - Auf dem Server muss das Programm 'winexe' über die Pfadvariable erreichbar sein vorhanden sein (mit whereis prüfen) / hierbei wird nicht auf die im opsi-client-agent mitgelieferte Version zurückgegriffen.
    - Er kann nur auf einen einzelnen Client abgesetzt werden. Bei Verteilung an mehrere Clients ist der Eintrag außer Kraft.
    - Befehlsverkettung funktioniert begrenzt. && und \|\| müssen in normale Anführungszeichen (kein Apostroph) gesetzt werden, bspw. "&&" oder "\|\|"
    - Piping und Ausgabeumlenkung sind sehr fallabhängig. Da hilft nur opsiPackageBuilder Log einschalten und ausprobieren.

**Beispiel:**

- folgender Befehl soll abgesetzt werden:
    ``cd c:\\TEMP\\RZInstall\\ETHLineSpeed && set NWDUPLEXMODE=AUTOSENS && start install.cmd``
- gem. obiger Hinweise muss in das Feld:
    ``cd c:\\TEMP\\RZInstall\\ETHLineSpeed "&&" set NWDUPLEXMODE=AUTOSENS "&&" start install.cmd``

- opsiPackageBuilder macht daraus im Hintergrund (plink Authorisation, Port können ja nach Einstellung variieren):
    ``winexe --debug-stderr --user "esaadm" --password "<localadminpass>" //client 'cmd /c cd c:\\TEMP\\RZInstall\\ETHLineSpeed "&&" set NWDUPLEXMODE=AUTOSENS "&&" start install.cmd'``

Das Kommando wir natürlich ohne Zeilenumbrüche abgesetzt. Die Werte in <> sind entsprechend der eigenen Umgebung zu ersetzen.)

Am besten ist es, den zu setzenden Befehl per Hand auf der Kommandozeile erst an einer Maschine zu prüfen und dann entsprechend im Feld zu hinterlegen. Die letzten 20 Befehle werden in der INI Datei gespeichert und bleiben somit für zukünftige Verwendung erhalten (Sollte in einem dieser Befehle das Paragraphensymbol "§" verwendet worden sein, wird die Liste beim erneuten Öffnen des Dialogs merkwürdig aussehen, da dieses Symbol intern für die Trennung der Kombobox Elemente verwendet wird.)

**Achtung:**

- Wird an einen einzelnen Client verteilt, so kann im Multi-Depot Betrieb der Quelldepotserver ausgewählt werden, um Leitungskapazitäten zu schonen.
- Wenn an mehrere Clients verteilt wird, dann kann im Multi-Depot Betrieb KEIN Depotserver ausgewählt werden, da für den Deploybefehl eine Liste in Dateiform erstellt werden muss. Dies ist momentan nur auf dem Workbench Share des zugeordneten Konfigservers zulässig. Ebenfalls führt es zu Fehlern, wenn der Entwicklungsordner nicht auf dem Workbench Share des Konfigservers liegt. Dann kann der Deploybefehl ebenfalls nicht ordnungsgemäß abgesetzt werden.

.. |image73| image:: ../img/DeployAgent.jpg