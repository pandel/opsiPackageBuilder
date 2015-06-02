Paketfunktionen
===============

|image17|

Im unteren Teil des Anwendungsfensters bleiben die Onlinefunktionen, die
zur Verfügung, stehen jederzeit sichtbar.

Funktionsbeschreibung

| Hinweis zur nachfolgenden Aufstellung:
| Es können ab Version 7.0 erweiterten Depotfunktionen aktiviert werden.
  Dann sind alle manuell hinterlegten Befehle außer Kraft,
| sondern werden ja nach verwendetem Depot intern autom. erzeugt.

+-------------------------+----------------------------------+-------------------------+
| Funktion                | Beschreibung                     | Besonderheiten bei      |
|                         |                                  | Offline Nutzung         |
+-------------------------+----------------------------------+-------------------------+
| Paketordner             | Der Ordnername des               |                         |
|                         | aktuell geöffneten               |                         |
|                         | Pakets.                          |                         |
+-------------------------+----------------------------------+-------------------------+
| Basis                   | Der in den                       | Temporärer              |
| Entwicklungsordner      | `Einstellungen                   | Entwicklungsordner      |
|                         | <#Allgemein>`__                  | Laufwerk C:\\ wird      |
|                         | hinterlegte Stammordner          | automatisch             |
|                         | für Paketentwicklung.            | eingestellt.            |
+-------------------------+----------------------------------+-------------------------+
| |image18|               | Onlinefunktion:                  | Die Funktion steht      |
|                         |                                  | nicht zur Verfügung.    |
|                         | Löst per SSH Verbindung          |                         |
|                         | zum opsi Server die              |                         |
|                         | Paketerzeugung aus.              |                         |
|                         |                                  |                         |
|                         | `Standardeinstellung             |                         |
|                         | <#opsiVerwaltungsbefehle>`__     |                         |
|                         |                                  |                         |
|                         | des verwendeten                  |                         |
|                         | Befehls:                         |                         |
|                         |                                  |                         |
|                         | opsi-makeproductfile             |                         |
|                         | -vv                              |                         |
|                         |                                  |                         |
|                         | Weitere Informationen            |                         |
|                         | dazu im opsi Handbuch.           |                         |
+-------------------------+----------------------------------+-------------------------+
| |image19|               | Onlinefunktion:                  | Die Funktion steht      |
|                         |                                  | nicht zur Verfügung.    |
|                         | Weist per SSH                    |                         |
|                         | Verbindung den opsi              |                         |
|                         | Server an, dass zu               |                         |
|                         | dieser Version                   |                         |
|                         | vorliegende                      |                         |
|                         | Installationspaket in            |                         |
|                         | das Depot einzuspielen.          |                         |
|                         |                                  |                         |
|                         | `Standardeinstellung             |                         |
|                         | <#opsiVerwaltungsbefehle>`__     |                         |
|                         |                                  |                         |
|                         | des verwendeten                  |                         |
|                         | Befehls:                         |                         |
|                         |                                  |                         |
|                         | opsi-package-manager -i          |                         |
|                         | -q                               |                         |
|                         |                                  |                         |
|                         | Es können auch mehrere           |                         |
|                         | Depots angesprochen              |                         |
|                         | werden. Um bspw. 2               |                         |
|                         | bestimmte Depots zu              |                         |
|                         | versorgen, ändern sie            |                         |
|                         | den eingetragenen                |                         |
|                         | Befehl wie folgt ab:             |                         |
|                         |                                  |                         |
|                         | opsi-package-manager -i          |                         |
|                         | -d <depot1>,<depot2> -q          |                         |
|                         |                                  |                         |
|                         | wobei für <depot1> und           |                         |
|                         | <depot2> die jeweilige           |                         |
|                         | DepotID verwendet                |                         |
|                         | werden muss.                     |                         |
|                         |                                  |                         |
|                         | Um alle Depots mit               |                         |
|                         | einem Paket zu                   |                         |
|                         | versorgen, ändern sie            |                         |
|                         | den eingetragenen                |                         |
|                         | Befehl wie folgt ab:             |                         |
|                         |                                  |                         |
|                         | opsi-package-manager -i          |                         |
|                         | -d all -q                        |                         |
|                         |                                  |                         |
|                         | WICHTIG: "-q" muss               |                         |
|                         | immer als letzter                |                         |
|                         | Parameter verwendet              |                         |
|                         | werden!                          |                         |
|                         |                                  |                         |
|                         | Weitere Informationen            |                         |
|                         | dazu im opsi Handbuch.           |                         |
|                         |                                  |                         |
+-------------------------+----------------------------------+-------------------------+
| |image20|               | siehe "Installieren"             | Die Funktion steht      |
|                         | zusätzlich dazu wird             | nicht zur Verfügung.    |
|                         | das Paket  auf allen             |                         |
|                         | Maschinen, auf denen es          |                         |
|                         | als "installed"                  |                         |
|                         | gekennzeichnet ist, auf          |                         |
|                         | "setup" gesetzt.                 |                         |
+-------------------------+----------------------------------+-------------------------+
| |image21|               | Onlinefunktion:                  | Die Funktion steht      |
|                         |                                  | nicht zur Verfügung.    |
|                         | Weist per SSH                    |                         |
|                         | Verbindung den opsi              |                         |
|                         | Server an, die aktuell           |                         |
|                         | geöffnete Version aus            |                         |
|                         | dem Softwaredepot zu             |                         |
|                         | entfernen.                       |                         |
|                         |                                  |                         |
|                         | `Standardeinstellung             |                         |
|                         | <#opsiVerwaltungsbefehle>`__     |                         |
|                         |                                  |                         |
|                         | des verwendeten                  |                         |
|                         | Befehls:                         |                         |
|                         |                                  |                         |
|                         | opsi-package-manager -r          |                         |
|                         | -q                               |                         |
|                         |                                  |                         |
|                         | WICHTIG: "-q" muss               |                         |
|                         | immer als letzter                |                         |
|                         | Parameter verwendet              |                         |
|                         | werden!                          |                         |
|                         |                                  |                         |
|                         | Weitere Informationen            |                         |
|                         | dazu im opsi Handbuch.           |                         |
+-------------------------+----------------------------------+-------------------------+
| |image22|               | Öffnet den aktuellen             |                         |
|                         | Paketordner in einem             |                         |
|                         | Explorerfenster.                 |                         |
+-------------------------+----------------------------------+-------------------------+
| |image23|               | Backup der                       |                         |
|                         | vorhergehenden                   |                         |
|                         | Paketkonfiguration und           |                         |
|                         | Speichern der aktuellen          |                         |
|                         | Informationen. Dies              |                         |
|                         | erzeugt die control              |                         |
|                         | Datei des Pakets neu.            |                         |
+-------------------------+----------------------------------+-------------------------+

Einschränkungen

Einige der o. a. Funktionen stehen nur unter bestimmten Voraussetzungen
zur Verfügung:

+--------------------------------------+--------------------------------------+
| Funktion                             | Voraussetzung                        |
+--------------------------------------+--------------------------------------+
| |image24|                            | Liegt zur aktuellen Paketversion     |
|                                      | eine bereits gepackte \*.opsi Datei  |
|                                      | im Paketordner vor, so wird diese    |
|                                      | Schaltfläche aktiviert.              |
+--------------------------------------+--------------------------------------+
| |image25|                            | Schaltfläche wird aktiviert, wenn    |
|                                      | ein Produkt mit der zugehörigen      |
|                                      | ProduktID auf dem Server installiert |
|                                      | ist und entfernt werden kann.        |
+--------------------------------------+--------------------------------------+

.. |image17| image:: ../img/Paketfunktionen.jpg
.. |image18| image:: ../img/btnPacken.png
.. |image19| image:: ../img/btnInstallieren.png
.. |image20| image:: ../img/InstSetup.jpg
.. |image21| image:: ../img/btnEntfernen.png
.. |image22| image:: ../img/btnOrdner.png
.. |image23| image:: ../img/btnSpeichern.png
.. |image24| image:: ../img/btnInstallieren.png
.. |image25| image:: ../img/btnEntfernen.png