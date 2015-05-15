Einleitung
==========

|image0|\  opsi Package Builder

opsi Package Builder ist ein Werkzeug zur Erstellung und Verwaltung von
Softwarepaketen in Zusammenarbeit mit dem

opsi (open pc server integration) Clientmanagementsystem der Firma uib
GmbH.

Hauptmerkmale der Anwendung sind:

-  Paketstrukturen anlegen und wiederholt bearbeiten
-  Abhängigkeiten und Produktvariablen anlegen, löschen, bearbeiten
-  Changelog pflegen
-  Skriptverwaltung, inkl. eigenem SkriptEditor
-  Paketrechte setzen
-  Pakete bauen, installieren und entfernen
-  Zeitplaner: zeitgesteuerte Installationsaufträge per AT Job am Server
   verwalten (inkl. on\_demand und WakeOnLan)

Mit dem Personal Edition von HelpNDoc erstellt: \ `Kindle eBooks einfach
herstellen <http://www.helpndoc.com/de/funktionen-tour/ebooks-fuer-den-amazon-kindle-erstellen>`__

Technisches und Danke an...
===========================

Ein paar "Interna"...

-  Anwendung basiert auf der Skriptsprache AutoIt
-  EXE in 32Bit
-  Serververbindungen sind SSH-basiert und verschlüsselt
-  Jobsteuerung per ATD Dämon direkt am Server
-  Zugriff zu spezifischen Informationen direkt über die JSON
   Schnittstelle des opsi Servers

...und ein herzliches "Danke!" an:

`opsi - open pc server integration <http://www.opsi.org>`__

Ohne opsi würde es das ganze Projekt schließlich nicht geben...

`AutoIt v3 <http://www.autoitscript.com/site/autoit/>`__

`ISN AutoIt
Studio <http://isnetwork.isi-webportal.at/index.php/meine-programme/isn-autoit-studio>`__

Speziell die Entwicklungsumgebung ISN AutoIt Studio hat mir bei der
Umsetzung der GUI großartige Dienste geleistet.

`PuTTY/Plink SSH
Client <http://www.chiark.greenend.org.uk/~sgtatham/putty/>`__

PuTTY, ein echtes Urgestein...

`HelpNDoc Personal Edition <http://www.helpndoc.com>`__

`Console UDF by Prog@ndy (with some small
modifications) <http://www.autoit.de/index.php?page=Thread&amp;threadID=25634>`__

`Marquee UDF by
Melba23 <http://www.autoitscript.com/forum/index.php?showtopic=143711>`__

`ModernMenu UDF by Holger
Kotsch <http://www.autoitscript.com/forum/index.php?showtopic=20967>`__

`Translate UDF by
Prog@ndy <http://www.autoit.de/index.php?page=Thread&amp;postID=157444#post157444>`__

`JSMN UDF (2013/05/19) by
Ward <http://www.autoitscript.com/forum/topic/104150-json-udf-library-fully-rfc4627-compliant/>`__

`Extracts from WinAPI Extended UDF by
Yashied <http://www.autoitscript.com/forum/topic/98712-winapiex-udf/>`__

`IniArray UDF by
Raupi <http://ipv4.autoit.de/index.php?page=Thread&amp;postID=152417>`__

Tolle UDFs, die die Funktionalität von AutoIt extrem erweitern!

... und vielen anderen im \ `deutschen <http://www.autoit.de/>`__\  und
\ `englischen <http://www.autoitscript.com/forum/>`__\  AutoIt Forum,
deren Hilfe mir bei der Umsetzung der Entwicklung geholfen hat!

Mit dem Personal Edition von HelpNDoc erstellt: \ `Einfacher EPub und
Dokumentationseditor <http://www.helpndoc.com/de>`__

Programmoberfläche
==================

|image1|

Nachfolgend werden die einzelnen Oberflächenbestandteile der Anwendung
beschrieben und, wenn vorhanden, auf Besonderheiten im Umgang damit
eingegangen.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Kindle eBooks
Generator <http://www.helpndoc.com/de/funktionen-tour/ebooks-fuer-den-amazon-kindle-erstellen>`__

Start
-----

|image2|

Beim Programmstart können die meist verwendeten Funktionen aufgerufen
werden. Für einen schnellen Arbeitsablauf lassen sich die einzelnen
Funktionen per Funktionstasten aufrufen.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| Funktion                | Hotkey                  | Beschreibung            |
+-------------------------+-------------------------+-------------------------+
| Neues Paket             | F1                      | Ein neues Software      |
|                         |                         | Installationspaket im   |
|                         |                         | Entwicklungsordner      |
|                         |                         | anlegen                 |
+-------------------------+-------------------------+-------------------------+
| Paket öffnen            | F2                      | Aus dem                 |
|                         |                         | Entwicklungsordner eine |
|                         |                         | bestehende              |
|                         |                         | Paketstruktur einlesen. |
|                         |                         | Es können keine         |
|                         |                         | gepackten Pakete        |
|                         |                         | (\*.opsi) geöffnet      |
|                         |                         | werden.                 |
+-------------------------+-------------------------+-------------------------+
| Zuletzt...              | F3                      | Die letzten fünf        |
|                         |                         | bearbeiteten            |
|                         |                         | Paketstrukturen         |
+-------------------------+-------------------------+-------------------------+
| Paketbündel erzeugen    | F5                      | Hilfsfunktion zur       |
|                         |                         | Schnellanlage von       |
|                         |                         | Paketbündeln. Diese     |
|                         |                         | Funktion erzeugt ein    |
|                         |                         | Paket, welches nur      |
|                         |                         | Abhängigkeiten zu       |
|                         |                         | weiteren Pakete         |
|                         |                         | beinhaltet, um immer    |
|                         |                         | wiederkehrende          |
|                         |                         | Installationen der      |
|                         |                         | gleichen Produkte zu    |
|                         |                         | vereinfachen.           |
+-------------------------+-------------------------+-------------------------+
| Paket installieren      | F6                      | Bereits bestehende      |
|                         |                         | Paketdateien (\*.opsi)  |
|                         |                         | können hierüber direkt  |
|                         |                         | auf dem Server          |
|                         |                         | installiert werden.     |
+-------------------------+-------------------------+-------------------------+
| Paket hochladen         | F7                      | Paket ohne Installation |
|                         |                         | in einen Repository     |
|                         |                         | Ordner hochladen        |
+-------------------------+-------------------------+-------------------------+
| Paket(e) entfernen      | F8                      | Bereits auf dem Server  |
|                         |                         | bestehende Pakete       |
|                         |                         | können hierüber direkt  |
|                         |                         | deinstalliert werden.   |
+-------------------------+-------------------------+-------------------------+
| Zeitplaner              | F4                      | Öffnen des Zeitplaners  |
|                         |                         | zum Einstellen von AT   |
|                         |                         | Aufträgen am opsi       |
|                         |                         | Server                  |
+-------------------------+-------------------------+-------------------------+
| Depot Manager           | F9                      | Depotverwaltung, bei    |
|                         |                         | ersten Öffnen werden    |
|                         |                         | alle Depotserver        |
|                         |                         | ausgelesen und für      |
|                         |                         | einen schnelleren       |
|                         |                         | Zugriff später gecacht. |
+-------------------------+-------------------------+-------------------------+
| Client Agent            | F10                     | Verteilung des          |
| installieren            |                         | opsi-client-agent via   |
|                         |                         | /var/lib/opsi/depot/ops |
|                         |                         | i-client-agent/opsi-dep |
|                         |                         | loy-client-agent        |
+-------------------------+-------------------------+-------------------------+
| Einstellungen           |                         | Öffnet den              |
|                         |                         | Einstellungendialog     |
+-------------------------+-------------------------+-------------------------+
| Beenden                 | Q / Esc                 | Beendet die Anwendung   |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `Hilfedokumente
einfach erstellen <http://www.helpndoc.com/de/funktionen-tour>`__

Reiter "Paket"
--------------

|image3|

Dieser Reiter beinhaltet die wesentlichen Paketinformationen, wie sie
auch durch das opsi Tool "opsi-newprod" zur Paketanlage abgefragt
werden.

Die Bezeichnungen sind weitestgehend selbsterklärend, daher nur einige
Hinweise:

.. raw:: html

   <div class="rvps2">

+--------------------------------------+-------------------------------------+
| Feld / Funktion                      | Hinweis                             |
+--------------------------------------+-------------------------------------+
| Priorität                            | Mit dem Schieber läßt sich die      |
|                                      | Priorität von -100 bis +100         |
|                                      | einstellen. Zum Zurücksetzen auf 0  |
|                                      | einmal auf das Anzeigefeld daneben  |
|                                      | klicken.                            |
+--------------------------------------+-------------------------------------+
| Skripteingabefelder                  | Diese Felder entsprechen den        |
| (Install/Deinstall./Aktualisieren/Im | unterschiedlichen opsi-winst        |
| mer/Einmalig/Benutzer/Anmeldung)     | Installationsskripten. Nähere       |
|                                      | Informationen dazu finden sich in   |
|                                      | den opsi Anwendungshandbüchern.     |
+--------------------------------------+-------------------------------------+
| |image4|                             | Öffnet das nebenstehende Skript im  |
|                                      | in den                              |
|                                      | \ `Einstellungen <#Programmeinstellu|
|                                      | ngen>`__\                           |
|                                      | hinterlegten Editor. Standard ist   |
|                                      | notepad.exe.                        |
+--------------------------------------+-------------------------------------+
| |image5|                             | Zeigt einen Dateiauswahldialog      |
|                                      | relativ zum Paketordner an und      |
|                                      | stellt sicher, dass nur Skripte     |
|                                      | innerhalb des Paketes ausgewählt    |
|                                      | werden können.                      |
+--------------------------------------+-------------------------------------+
| |image6|                             | Öffnet den in den                   |
|                                      | \ `Einstellungen <#Programmeinstellu|
|                                      | ngen>`__\                           |
|                                      | gewählten Changelog Editor Typ.     |
|                                      | Näheres dazu unter "\ `Changelog    |
|                                      | Editor <#ChangelogEditor>`__\ "     |
+--------------------------------------+-------------------------------------+
| |image7|                             | Öffnet die                          |
|                                      | \ `Strukturanzeige <#Skriptbaum>`__ |
|                                      |                                     |
|                                      | der Installationsskripte. Von dort  |
|                                      | können auch sämtliche per "sub" bzw.|
|                                      | "include" eingebundenen Skripte     |
|                                      | eingesehen und, sofern im           |
|                                      | Paketordner befindlich, bearbeitet  |
|                                      | werden. Außerhalb des Paketordners  |
|                                      | abgelegte Skripte können aus        |
|                                      | Sicherheitsgründen nicht bearbeitet |
|                                      | werden.                             |
+--------------------------------------+-------------------------------------+

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
Hilfeverfassungsumfeld <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Reiter "Abhängigkeit"
---------------------

|image8|

Auf diesem Reiter können Paketabhängigkeiten (product dependencies)
definiert und bearbeitet werden.

Der obere Teil des Fensters beinhaltet eine tabellarische Aufstellung
der derzeit im Paket definierten Abhängigkeiten. Sollte in der Liste nur
ein einziger Eintrag in der Spalte "Aktion" mit dem Inhalt "empty"
angezeigt werden, so weißt das daraufhin, dass noch keinerlei
Abhängigkeiten definiert worden sind.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| Feld / Funktion         | Beschreibung            | Hinweise                |
+-------------------------+-------------------------+-------------------------+
| Aktionsbezug            | Für welche angeforderte | Mögliche Werte: setup / |
|                         | Aktion ist diese        | uninstall / update      |
|                         | Abhängigkeit gültig.    |                         |
+-------------------------+-------------------------+-------------------------+
| Notw. Produkt ID        | Produkt zu dem die      | Entweder ein            |
| (Auswahlliste /         | Abhängigkeit besteht    | bestehendes,            |
| Freitextfeld)           |                         | installiertes Produkt   |
|                         |                         | aus der Liste           |
|                         |                         | auswählen, oder im      |
|                         |                         | Freitextfeld die        |
|                         |                         | Produkt ID eines        |
|                         |                         | derzeit nicht           |
|                         |                         | vorhandenen Produkts    |
|                         |                         | eingeben.               |
+-------------------------+-------------------------+-------------------------+
| Geford. Aktion          | Aktion, die für das     | Mögliche Werte: none /  |
|                         | abhängige Produkt       | setup / update          |
|                         | angefordert werden soll |                         |
|                         |                         | Werden "setup" oder     |
|                         |                         | "update" gewählt, wird  |
|                         |                         | der "Notw.              |
|                         |                         | Installationsstatus"    |
|                         |                         | autom. auf "none"       |
|                         |                         | gesetzt.                |
+-------------------------+-------------------------+-------------------------+
| Notw.                   | Installationsstatus,    | Mögliche Werte: none /  |
| Installationsstatus     | den das abhängige       | installed               |
|                         | Produkt besitzen muss   |                         |
|                         |                         | Wird "installed"        |
|                         |                         | gewählt, wird die       |
|                         |                         | "Geford. Aktion" autom. |
|                         |                         | auf "none" gesetzt.     |
+-------------------------+-------------------------+-------------------------+
| Reihenfolge             | Reihenfolge, in der die | Mögliche Werte: before  |
|                         | Abhängigkeit zum        | / after                 |
|                         | aktuellen Paket         |                         |
|                         | aufgelöst werden soll.  |                         |
+-------------------------+-------------------------+-------------------------+
| |image9|                | Eine neue Abhängigkeit  |                         |
|                         | anlegen.                |                         |
|                         |                         |                         |
|                         | Es öffnet sich ein      |                         |
|                         | Dialogfenster, in dem   |                         |
|                         | die neuen Werte erfasst |                         |
|                         | werden können. Die      |                         |
|                         | Feldbezeichnungen und   |                         |
|                         | -vorgaben lauten        |                         |
|                         | entsprechend.           |                         |
+-------------------------+-------------------------+-------------------------+
| |image10|               | Eine bestehende         | Wenn der Reiter         |
|                         | Abhängigkeit ändern und | gewechselt wird, ohne   |
|                         | aktualisieren.          | die Änderung zu         |
|                         |                         | übernehmen, gehen diese |
|                         | Um eine bestehende      | i d. R. verloren.       |
|                         | Abhängigkeit zu         |                         |
|                         | verändern, wie folgt    |                         |
|                         | vorgehen:               |                         |
|                         |                         |                         |
|                         | #. in der               |                         |
|                         |    tabellarischen       |                         |
|                         |    Auflistung die       |                         |
|                         |    entsprechende Zeile  |                         |
|                         |    anklicken            |                         |
|                         | #. die Werte in den     |                         |
|                         |    einzelnen Feldern    |                         |
|                         |    entsprechend         |                         |
|                         |    anpassen             |                         |
|                         | #. auf "Übernehmen"     |                         |
|                         |    klicken              |                         |
|                         |                         |                         |
|                         | Die Änderung wird       |                         |
|                         | sofort in die           |                         |
|                         | tabellarische           |                         |
|                         | Auflistung übernommen.  |                         |
+-------------------------+-------------------------+-------------------------+
| |image11|               | Eine bestehende         | Solange das Paket nicht |
|                         | Abhängigkeit entfernen. | gespeichert wurde, kann |
|                         |                         | eine ungewollte         |
|                         | Um eine bestehende      | Löschung durch erneutes |
|                         | Abhängigkeit zu         | Einladen rückgängig     |
|                         | entfernen, wie folgt    | gemacht werden. Nach    |
|                         | vorgehen:               | dem Speichern muss die  |
|                         |                         | Vorgängerversion der    |
|                         | #. in der               | control Datei manuell   |
|                         |    tabellarischen       | aus dem                 |
|                         |    Auflistung die       | Unterverzeichnis "OPSI" |
|                         |    entsprechende Zeile  | des Pakets              |
|                         |    anklicken            | zurückgesichert werden. |
|                         | #. auf "Löschen"        |                         |
|                         |    klicken              |                         |
|                         | #. den nachfolgenden    |                         |
|                         |    Warnhinweis          |                         |
|                         |    bestätigen           |                         |
|                         |                         |                         |
|                         | Die Änderung wird       |                         |
|                         | sofort in die           |                         |
|                         | tabellarische           |                         |
|                         | Auflistung übernommen.  |                         |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
HTML-Hilfedokumentationsgenerator <http://www.helpndoc.com/de>`__

Reiter "Produktvariablen"
-------------------------

|image12|

Auf diesem Reiter können Produktvariablen (product properties) definiert
und bearbeitet werden.

Der obere Teil des Fensters beinhaltet eine tabellarische Aufstellung
der derzeit im Paket definierten Produktvariablen. Sollte in der Liste
nur ein einziger Eintrag in der Spalte "Bezeichner" mit dem Inhalt
"empty" angezeigt werden, so weißt das daraufhin, dass noch keinerlei
Produktvariablen definiert worden sind.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| Feld / Funktion         | Beschreibung            | Hinweise                |
+-------------------------+-------------------------+-------------------------+
| Bezeichner              | Name der                | Dieser Bezeichner wird  |
|                         | Produktvariable         | in der                  |
|                         |                         | Produktkonfiguration im |
|                         |                         | opsi-configed angezeigt |
|                         |                         | und ist innerhalb der   |
|                         |                         | Skripte mit der         |
|                         |                         | Funktion                |
|                         |                         | "GetProductProperty"    |
|                         |                         | auslesbar.              |
|                         |                         |                         |
|                         |                         | Weitere Informationen   |
|                         |                         | siehe OPSI Getting      |
|                         |                         | Started Handbuch.       |
+-------------------------+-------------------------+-------------------------+
| Typ                     | Variablentyp            | Mögliche Werte: unicode |
|                         |                         | / bool                  |
|                         |                         |                         |
+-------------------------+-------------------------+-------------------------+
| Mehrfachwert            | Bestimmt, ob die        | Nur bei Typ "unicode"   |
|                         | Produktvariable nur     | verfügbar               |
|                         | genau einen oder        |                         |
|                         | mehrere Werte annehmen  |                         |
|                         | kann                    |                         |
+-------------------------+-------------------------+-------------------------+
| Änderbar                | Bestimmt, ob die        | Nur bei Typ "unicode"   |
|                         | Vorgabewerte mit neuen  | verfügbar               |
|                         | oder zusätzlichen       |                         |
|                         | Werten überschrieben    |                         |
|                         | werden können oder      |                         |
|                         | nicht                   |                         |
+-------------------------+-------------------------+-------------------------+
| Beschreibung            | Beschreibung der        | Wird im opsi-configed   |
|                         | Variablenfunktion       | als Tooltip angezeigt   |
+-------------------------+-------------------------+-------------------------+
| Werte                   | Komma-separiert Liste   | Falls "Änderbar" auf    |
|                         | der möglichen           | "True" gesetzt wurde,   |
|                         | Eingabewerte            | kann die Liste später   |
|                         |                         | innerhalb von           |
|                         |                         | opsi-configed ergänzt   |
|                         |                         | werden.                 |
|                         |                         |                         |
|                         |                         | Nur bei Typ "unicode"   |
|                         |                         | verfügbar               |
|                         |                         |                         |
+-------------------------+-------------------------+-------------------------+
| Vorgabe (Freitextfeld / | Vorgabewert             | Nur bei Typ "unicode"   |
| Auswahlliste)           |                         | verfügbar: Freitextfeld |
|                         |                         |                         |
|                         |                         | Nur bei Typ "bool"      |
|                         |                         | verfügbar: Auswahlliste |
+-------------------------+-------------------------+-------------------------+
| |image13|               | Eine neue               |                         |
|                         | Produktvariable         |                         |
|                         | anlegen.                |                         |
|                         |                         |                         |
|                         | Es öffnet sich ein      |                         |
|                         | Dialogfenster, in dem   |                         |
|                         | die neuen Werte erfasst |                         |
|                         | werden können. Die      |                         |
|                         | Feldbezeichnungen und   |                         |
|                         | -vorgaben lauten        |                         |
|                         | entsprechend.           |                         |
+-------------------------+-------------------------+-------------------------+
| |image14|               | Eine bestehende         | Wenn der Reiter         |
|                         | Produktvariable ändern  | gewechselt wird, ohne   |
|                         | und aktualisieren.      | die Änderung zu         |
|                         |                         | übernehmen, gehen diese |
|                         | Um eine bestehende      | i d. R. verloren.       |
|                         | Produktvariable zu      |                         |
|                         | verändern, wie folgt    |                         |
|                         | vorgehen:               |                         |
|                         |                         |                         |
|                         | #. in der               |                         |
|                         |    tabellarischen       |                         |
|                         |    Auflistung die       |                         |
|                         |    entsprechende Zeile  |                         |
|                         |    anklicken            |                         |
|                         | #. die Werte in den     |                         |
|                         |    einzelnen Feldern    |                         |
|                         |    entsprechend         |                         |
|                         |    anpassen             |                         |
|                         | #. auf "Übernehmen"     |                         |
|                         |    klicken              |                         |
|                         |                         |                         |
|                         | Die Änderung wird       |                         |
|                         | sofort in die           |                         |
|                         | tabellarische           |                         |
|                         | Auflistung übernommen.  |                         |
+-------------------------+-------------------------+-------------------------+
| |image15|               | Diese Funktion          | Werden Produktvariablen |
|                         | ermöglicht das          | gefunden, so wird für   |
|                         | automatische Ermitteln  | jede neue Variable ein  |
|                         | und Einlesen von        | kompletter Datensatz    |
|                         | Produktvariablen, die   | abgefragt.              |
|                         | in den verschiedenen    |                         |
|                         | Installationsskripten   | Die bereits vorhandenen |
|                         | definiert sind.         | und definierten         |
|                         |                         | Produktvariablen werden |
|                         | Das erleichtert         | berücksichtigt und nur  |
|                         | allerdings die Suche    | neue aufgenommen.       |
|                         | und Eintragung neuer    |                         |
|                         | Produktvariablen, die   |                         |
|                         | im Rahmen der           |                         |
|                         | Skriptentwicklung hinzu |                         |
|                         | gekommen sind.          |                         |
|                         |                         |                         |
+-------------------------+-------------------------+-------------------------+
| |image16|               | Eine bestehende         | Solange das Paket nicht |
|                         | Produktvariable         | gespeichert wurde, kann |
|                         | entfernen.              | eine ungewollte         |
|                         |                         | Löschung durch erneutes |
|                         | Um eine bestehende      | Einladen rückgängig     |
|                         | Produktvariable zu      | gemacht werden. Nach    |
|                         | entfernen, wie folgt    | dem Speichern muss die  |
|                         | vorgehen:               | Vorgängerversion der    |
|                         |                         | control Datei manuell   |
|                         | #. in der               | aus dem                 |
|                         |    tabellarischen       | Unterverzeichnis "OPSI" |
|                         |    Auflistung die       | des Pakets              |
|                         |    entsprechende Zeile  | zurückgesichert werden. |
|                         |    anklicken            |                         |
|                         | #. auf "Löschen"        |                         |
|                         |    klicken              |                         |
|                         | #. den nachfolgenden    |                         |
|                         |    Warnhinweis          |                         |
|                         |    bestätigen           |                         |
|                         |                         |                         |
|                         | Die Änderung wird       |                         |
|                         | sofort in die           |                         |
|                         | tabellarische           |                         |
|                         | Auflistung übernommen.  |                         |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Dokumentationsgenerator <http://www.helpndoc.com/de>`__

Paketfunktionen
---------------

|image17|

Im unteren Teil des Anwendungsfensters bleiben die Onlinefunktionen, die
zur Verfügung, stehen jederzeit sichtbar.

Funktionsbeschreibung

| Hinweis zur nachfolgenden Aufstellung:
| Es können ab Version 7.0 erweiterten Depotfunktionen aktiviert werden.
  Dann sind alle manuell hinterlegten Befehle außer Kraft,
| sondern werden ja nach verwendetem Depot intern autom. erzeugt.

.. raw:: html

   <div class="rvps2">

+-------------------------+---------------------------+-------------------------+
| Funktion                | Beschreibung              | Besonderheiten bei      |
|                         |                         = | Offline Nutzung         |
+-------------------------+---------------------------+-------------------------+
| Paketordner             | Der Ordnername des      - |                         |
|                         | aktuell geöffneten        |                         |
|                         | Pakets.                 - |                         |
+-------------------------+---------------------------+-------------------------+
| Basis                   | Der in den             -- | Temporärer              |
| Entwicklungsordner      | \ `Einstellungen <#Allg   | Entwicklungsordner      |
|                         | emein>`__\             -- | Laufwerk C:\\ wird      |
|                         | hinterlegte Stammordner   | automatisch             |
|                         | für Paketentwicklung.  -- | eingestellt.            |
+-------------------------+---------------------------+-------------------------+
| |image18|               | Onlinefunktion:        -- | Die Funktion steht      |
|                         |                           | nicht zur Verfügung.    |
|                         | Löst per SSH Verbindung-- |                         |
|                         | zum opsi Server die       |                         |
|                         | Paketerzeugung aus.    -- |                         |
|                         |                           |                         |
|                         |                        -  |                         |
|                         |  `<#opsiVerwaltungsbefeh  |                         |
|                         | le>`__                 -- |                         |
|                         |                           |                         |
|                         | `Standardeinstellung <#-- |                         |
|                         | opsiVerwaltungsbefehle>   |                         |
|                         | `__\                   -- |                         |
|                         | des verwendeten           |                         |
|                         | Befehls:               -- |                         |
|                         |                           |                         |
|                         | opsi-makeproductfile   -- |                         |
|                         | -vv                       |                         |
|                         |                        -- |                         |
|                         | Weitere Informationen     |                         |
|                         | dazu im opsi Handbuch. -- |                         |
+-------------------------+---------------------------+-------------------------+
| |image19|               | Onlinefunktion:        -- | Die Funktion steht      |
|                         |                           | nicht zur Verfügung.    |
|                         | Weist per SSH          -- |                         |
|                         | Verbindung den opsi       |                         |
|                         | Server an, dass zu     -- |                         |
|                         | dieser Version            |                         |
|                         | vorliegende            -- |                         |
|                         | Installationspaket in     |                         |
|                         | das Depot einzuspielen.-- |                         |
|                         |                           |                         |
|                         | `Standardeinstellung ---- |                         |
|                         | <#opsiVerwaltungsbefehle> |                         |
|                         | `__\                   -- |                         |
|                         | des verwendeten           |                         |
|                         | Befehls:                - |                         |
|                         |                           |                         |
|                         | opsi-package-manager -i-- |                         |
|                         | -q                        |                         |
|                         |                        -- |                         |
|                         | Es können auch mehrere    |                         |
|                         | Depots angesprochen    -- |                         |
|                         | werden. Um bspw. 2        |                         |
|                         | bestimmte Depots zu    -- |                         |
|                         | versorgen, ändern sie     |                         |
|                         | den eingetragenen      -- |                         |
|                         | Befehl wie folgt ab:      |                         |
|                         |                        -- |                         |
|                         | opsi-package-manager -i   |                         |
|                         | -d <depot1>,<depot2> -q-- |                         |
|                         |                           |                         |
|                         | wobei für <depot1> und -- |                         |
|                         | <depot2> die jeweilige    |                         |
|                         | DepotID verwendet      -- |                         |
|                         | werden muss.              |                         |
|                         |                        -- |                         |
|                         | Um alle Depots mit        |                         |
|                         | einem Paket zu         -- |                         |
|                         | versorgen, ändern sie     |                         |
|                         | den eingetragenen      -- |                         |
|                         | Befehl wie folgt ab:      |                         |
|                         |                        -- |                         |
|                         | opsi-package-manager -i   |                         |
|                         | -d all -q              -- |                         |
|                         |                           |                         |
|                         | WICHTIG: "-q" muss     -- |                         |
|                         | immer als letzter         |                         |
|                         | Parameter verwendet    -- |                         |
|                         | werden!                   |                         |
|                         |                        -- |                         |
|                         | Weitere Informationen     |                         |
|                         | dazu im opsi Handbuch. -- |                         |
|                         |                           |                         |
+-------------------------+---------------------------+-------------------------+
| |image20|               | siehe "Installieren" -    | Die Funktion steht      |
|                         | zusätzlich dazu wird   -- | nicht zur Verfügung.    |
|                         | das Paket  auf allen      |                         |
|                         | Maschinen, auf denen es-- |                         |
|                         | als "installed"           |                         |
|                         | gekennzeichnet ist, auf-- |                         |
|                         | "setup" gesetzt.          |                         |
+-------------------------+---------------------------+-------------------------+
| |image21|               | Onlinefunktion:           | Die Funktion steht      |
|                         |                        -- | nicht zur Verfügung.    |
|                         | Weist per SSH             |                         |
|                         | Verbindung den opsi    -- |                         |
|                         | Server an, die aktuell    |                         |
|                         | geöffnete Version aus  -- |                         |
|                         | dem Softwaredepot zu      |                         |
|                         | entfernen.             -- |                         |
|                         |                           |                         |
|                         | `Standardeinstellung <#-- |                         |
|                         | opsiVerwaltungsbefehle>   |                         |
|                         | `__\                   -- |                         |
|                         | des verwendeten           |                         |
|                         | Befehls:               -- |                         |
|                         |                           |                         |
|                         | opsi-package-manager -r-- |                         |
|                         | -q                        |                         |
|                         |                        -- |                         |
|                         | WICHTIG: "-q" muss        |                         |
|                         | immer als letzter      -- |                         |
|                         | Parameter verwendet       |                         |
|                         | werden!                -- |                         |
|                         |                           |                         |
|                         | Weitere Informationen  -- |                         |
|                         | dazu im opsi Handbuch.    |                         |
+-------------------------+---------------------------+-------------------------+
| |image22|               | Öffnet den aktuellen      |                         |
|                         | Paketordner in einem   -- |                         |
|                         | Explorerfenster.          |                         |
+-------------------------+---------------------------+-------------------------+
| |image23|               | Backup der                |                         |
|                         | vorhergehenden         -- |                         |
|                         | Paketkonfiguration und    |                         |
|                         | Speichern der aktuellen-- |                         |
|                         | Informationen. Dies       |                         |
|                         | erzeugt die control    -- |                         |
|                         | Datei des Pakets neu.     |                         |
+-------------------------+---------------------------+-------------------------+

.. raw:: html

   </div>

Einschränkungen

Einige der o. a. Funktionen stehen nur unter bestimmten Voraussetzungen
zur Verfügung:

.. raw:: html

   <div class="rvps2">

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

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `CHM-Hilfedokumente
einfach erstellen <http://www.helpndoc.com/de/funktionen-tour>`__

Changelog Editor
----------------

|image26|

Beschreibung zur Changelog Editor Funktionalität

Mit Hilfe des Changelog Editors können die in der Control Dateisektion
[Changelog] hinterlegten Einträge gepflegt werden. Da der Aufbau dieser
Sektion, im Gegensatz zur sonstigen Struktur der Control Datei, nicht
fest vorgegeben ist, ist es grundsätzlich möglich, diese Sektion
unterschiedlich mit Informationen anzureichern.

Variante 1:

Unterhalb der Sektionsüberschrift wird unstrukturierter Freitext
hinterlegt. Auch wenn damit eine Dokumentation natürlich grundsätzlich
möglich ist, so kann diese Art der Dokumentation mit einigen
Einschränkungen verbunden sein. Neben der Tatsache, daß Fließtext nicht
zwingend die Lesbarkeit erhöht, so dokumentiert er ggf. auch nicht
notwendige Informationen, um die zu dokumentierenden Änderungen
zeitlich, bzgl. ihrer Wichtigkeit oder auch bezogen auf den Autor der
Änderung einzugliedern.

Variante 2:

Die Changelog Einträge werden nach einem festen Schema zeitlich
absteigend sortiert in Textblöcken hinterlegt. Sie erhalten eine
feststehende Überschrift (=Kopfzeile) und einen Abschlussvermerk
(=Fußzeile), der den Eintrag näher beschreibt. Diese Eintragungsart wird
auch bei der Paketanlage von opsi-newprod für den ersten Eintrag
verwendet.

Um diesen beiden Paradigmen Rechnung zu tragen, enthält opsi Package
Builder zwei verschiedene Arten von Editoren für die Changelog Einträge,
den \ `einfachen <#Einfach>`__\  (Variante 1) und den
\ `erweiterten <#Erweitert>`__\  (Variante 2) Editor.

Beim Öffnen eines Pakets wird der gesamte Text innerhalb der
[Changelog]-Sektion der Control Datei gemäß der in den \ `Einstellungen
gewählten Editorvariante <#Programmeinstellungen>`__\  eingelesen. Für
den Betrieb des erweiterten Editors spielt dabei zusätzlich der Eintrag
im \ `Feld "Blockerkennung" <#Programmeinstellungen>`__\  eine
entscheidende Rolle. Findet opsi Package Builder beim Einlesen eine
Textzeile, die den dort hinterlegten Eintrag beinhaltet, wird der
nachfolgende Text als neuer Changelog Textblock erkannt.

Achtung:

Die Changelog Einträge der Control Datei werden nur einmalig beim Öffnen
des Pakets geladen und interpretiert. Sollten in der Zwischenzeit bei
geöffnetem Paket Änderungen an den Einstellungen zur Verwendung des
Editors oder der Blockerkennung durchgeführt werden, so muss das
geöffnete Paket geschlossen und wieder geöffnet werden.

Hinweise zur Bestandspflege "alter" Pakete

Soll ein bereits bestehendes Paket mit opsi Package Builder gepflegt
werden, so ist es für die weiterführende Pflege der "alten" Changelog
Einträge wichtig, ob in der Vergangenheit mit Variante 1 oder 2
gearbeitet wurde.

-  wurde ausschließlich mit Variante 1 gearbeitet:

| In den Einstellungen sollte der Haken bei "Erweiterten Changelog
  Editor verwenden" entfernt werden. Damit kann die Pflege auf gewohnte
  Weise fortgesetzt werden. Sollen die alten Einträge in die neue,
  strukturierte Form überführt werden, ist wie in der Hilfe unter
  \ `Konvertierungshinweise <#Konvertierungshinweise>`__\  beschrieben
  vorzugehen.
| 

-  wurde ausschließlich mit Variante 2 gearbeitet:

In den Einstellungen sollte der Haken bei "Erweiterten Changelog Editor
verwenden" gesetzt werden. Zusätzlich sollte überprüft werden, ob die
verwendete Überschrift (=Kopfzeile) den in den \ `Einstellungen im Feld
"Blockerkennung" <#Programmeinstellungen>`__\  hinterlegten Text
beinhaltet. Wurde eine eigene, wiederkehrende Textmarkierung verwendet,
ist der Wert in den Einstellungen entsprechend anzupassen. Weitere
Informationen dazu \ `hier <#Konvertierungshinweise>`__\ .

Beispiele für strukturierte Changelog Einträge in der Control Datei zur
Verwendung mit opsi Package Builder

        

1. Einträge gem. opsi-newprod Vorgabe und Grundeinstellung in opsi
Package Builder:

[Changelog]

acroread (11.0.01-2) stable; urgency=low

  \* Test abgeschlossen

  \* Paket in stable

 -- Holger Pandel <holger.pandel@....de>  Wed, 31 Jan 2013 11:43:01
+0000

acroread (11.0.01-1) testing; urgency=low

  \* Initial package

 -- Holger Pandel <holger.pandel@....de>  Wed, 30 Jan 2013 16:25:01
+0000

Die grün markierte Textstelle kehrt bei jedem Changelog Eintrag wieder
und kennzeichnet damit den Beginn eines neuen Textblocks. Sie wird gem.
der Standardeinstellung in opsi Package Builder zur Blockerkennung
verwendet.

2. Einträge mit selbstgewählter, wiederkehrender Struktur

[Changelog]

Lfd. Nr. der Änderung: 2 am  31 Jan 2013 11:43:01

Paketversion: 11.0.01-2

Status: stable

urgency=low

  \* Test abgeschlossen

  \* Paket in stable

 -- Holger Pandel <holger.pandel@....de>

Lfd. Nr. der Änderung: 1 am 15 Jan 2013 13:28:15

Paketversion: 11.0.01-1

Status: testing

urgency=low

  \* Initial package

 -- Holger Pandel <holger.pandel@....de>

Die grün markierte Textstelle kehrt bei jedem Changelog Eintrag wieder
und kennzeichnet damit den Beginn eines neuen Textblocks. Sie kann somit
ebenfalls zur Blockerkennung verwendet werden und muss in
den\ `Einstellungen im Feld
"Blockerkennung" <#Programmeinstellungen>`__\  hinterlegt werden. Es ist
jedoch hierbei darauf zu achten, dass dieser Begriff nicht zusätzlich im
Langtext des Changelog Eintrags auftaucht, um Fehler bei der
Blockerkennung zu vermeiden.

Vorteile bei der Nutzung des Standardverhaltens

Wird das Standardverhalten von opsi Package Builder beibehalten, können
mit den Funktionen und zusätzlichen Auswahlfeldern im erweiterten Editor
komfortabel und schnell neue Einträge angelegt werden, die vollständig
kompatibel zur Blockerkennung von opsi Package Builder sind. Falls doch
eine individuelle Blockgestaltung genutzt werden soll ist
sicherzustellen, dass die Blockmarkierung, die im individuellen
Eingabefeld eingegeben wird eindeutig ist.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
iPhone-Dokumentationsgenerator <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Einfach
~~~~~~~

|image27|

Ist in den \ `Einstellungen <#Programmeinstellungen>`__\  die Nutzung
des erweiterten Changelog Editors deaktiviert, erscheint beim Klick auf
die Schaltfläche "Changelog" im \ `Reiter "Paket" <#ReiterPaket>`__\ 
das einfache Editorfenster. Hier kann reiner Fließtext in beliebiger
Form als Hinterlegt werden.

Wird der Editor über die Schaltfläche \ |image28|\  geschlossen, werden
autom. sämtliche Änderungen übernommen.

Hinweis:

Ist der erweiterte Editor ausgewählt und es tritt beim Einlesen eines
Pakets ein Fehler bei der Changelog Blockerkennung auf, so wird
ebenfalls der einfache Editor geöffnet. Der Benutzer erhält einen
entsprechenden Warnhinweis.

Mit dem Personal Edition von HelpNDoc erstellt: \ `iPhone Websites
einfach
gemacht <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Erweitert
~~~~~~~~~

|image29|

Ist in den \ `Einstellungen <#Programmeinstellungen>`__\  die Nutzung
des erweiterten Changelog Editors aktiviert, erscheint beim Klick auf
die Schaltfläche "Changelog" im \ `Reiter "Paket" <#ReiterPaket>`__\ 
das erweiterte Editorfenster. Damit können die einzelnen Changelog
Einträge komfortabel verwaltet werden.

Hinweis:

Ist der erweiterte Editor ausgewählt und es tritt beim Einlesen eines
Pakets ein Fehler bei der Changelog Blockerkennung auf, so wird der
einfache Editor geöffnet. Der Benutzer erhält einen entsprechenden
Warnhinweis.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| Feld / Funktion         | Beschreibung            | Hinweise                |
+-------------------------+-------------------------+-------------------------+
| Tabelle "Changelog      | Alle vorhandenen        | absteigend sortiert     |
| Entry"                  | Changelog Einträge in   |                         |
|                         | der Reihenfolge der     |                         |
|                         | Anlage                  |                         |
+-------------------------+-------------------------+-------------------------+
| Feld 1                  | Paketversion des        | nur Anzeige             |
|                         | Changelog Eintrags      |                         |
|                         |                         | nur aktiv bei           |
|                         |                         | Standardblockerkennung  |
+-------------------------+-------------------------+-------------------------+
| Feld 2                  | Paketstatus Markierung  | Mögliche Werte: testing |
|                         |                         | / stable                |
|                         |                         |                         |
|                         |                         | nur aktiv bei           |
|                         |                         | Standardblockerkennung  |
+-------------------------+-------------------------+-------------------------+
| Feld 3                  | Dringlichkeitsmarkierun | Mögliche Werte:         |
|                         | g                       | urgency=low /           |
|                         | der Änderung            | urgency=middle /        |
|                         |                         | urgency=high            |
|                         |                         |                         |
|                         |                         | nur aktiv bei           |
|                         |                         | Standardblockerkennung  |
+-------------------------+-------------------------+-------------------------+
| Feld 4                  | Individuelles Header    | nur aktiv bei           |
|                         | Feld                    | individueller           |
|                         |                         | Blockerkennung          |
+-------------------------+-------------------------+-------------------------+
| unteres Editorfeld      | Langtext des Changelog  |                         |
|                         | Eintrags                |                         |
+-------------------------+-------------------------+-------------------------+
| |image30|               | Erzeugen eines neuen    | Der Eintrag bekommt     |
|                         | Eintrags                | einen initialen Text    |
|                         |                         | und eine letzte Zeile   |
|                         |                         | nach dem Schema         |
|                         |                         |                         |
|                         |                         | Maintainer/Mail/Datum/U |
|                         |                         | hrzeit/UTC              |
+-------------------------+-------------------------+-------------------------+
| |image31|               | Änderungen übernehmen   | Sämtliche Änderungen    |
|                         |                         | großen Textfeld, die    |
|                         |                         | nicht übernommen        |
|                         |                         | wurden, gehen beim      |
|                         |                         | Schließen des Dialogs   |
|                         |                         | verloren.               |
+-------------------------+-------------------------+-------------------------+
| |image32|               | Entfernen eines         | Es kann immer nur ein   |
|                         | Changelog Eintrags      | Eintrag auf einmal      |
|                         |                         | entfernt werden.        |
+-------------------------+-------------------------+-------------------------+
| |image33|               | Beenden des Dialogs     | Alle nicht übernommenen |
|                         |                         | Änderungen im Textfeld  |
|                         |                         | gehen verloren.         |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

Unterschiede in der Darstellung zwischen Standardblockerkennung und
individueller Blockerkennung

Standardblockerkennung

Bei der Standardblockerkennung sind die erweiterten Auswahl- und
Eingabefelder aktiv.

|image34|

Individuelle Blockerkennung

Bei der individuellen Blockerkennung ist nur das freie Eingabefeld
verfügbar.

|image35|

Mit dem Personal Edition von HelpNDoc erstellt: \ `CHM, PDF, DOC und
HTML Hilfeerstellung von einer einzigen Quelle
aus <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Konvertierungshinweise
~~~~~~~~~~~~~~~~~~~~~~

Konvertierung von einfacher in erweiterte Darstellung und Funktionalität

Alte Changelog Einträge, die nicht einer festen strukturierten Form
entsprechen, können in die strukturierte Form überführt werden, ohne
dass die Inhalte verloren gehen.

Dazu ist folgende Reihenfolge in der Vorgehensweise einzuhalten:

#. opsi Package Builder starten
#. unter "Einstellungen" - "Programmeinstellungen" den Haken bei
   "Erweiterten Changelog Editor verwenden" entfernen (die auftretende
   Meldung kann ignoriert werden, solange kein Paket geladen ist)
#. das Paket mit den zu konvertierenden Changelog Einträgen öffnen
#. unter "Einstellungen" - "Programmeinstellungen" den Haken bei
   "Erweiterten Changelog Editor verwenden" setzen
   es erfolgt folgende Meldung:
   |image36|

#. das Paket speichern

Jetzt liegt das Changelog inkl. der alten Einträge im neuen Format vor
und kann mit dem erweiterten Editor bearbeitet werden.

Beispiel für umgestellte Einträge

Einträge vor der Konvertierung:

[Changelog]

Das hier ist nur allgemeines Changelog blabla ohne Struktur

damit läßt sich nicht viel anfangen

aber gehen tuts auch

brabrabra

tätäta

Einträge nach der Konvertierung:

[Changelog]

acroread (11.0.01-2) testing; urgency=low

  \* ChangeLog converted via opsi PackageBuilder editor

                ----------- ALTES CHANGELOG FORMAT -----------

                Das hier ist nur allgemeines Changelog blabla ohne
Struktur

                

                damit läßt sich nicht viel anfangen

                aber gehen tuts auch

                

                brabrabra

                

                tätäta

                

                

                ----------- ALTES CHANGELOG FORMAT -----------

 -- Holger Pandel <holger.pandel@....de> Tue, 02 Apr 2013 18:03:37 +
0100

Konvertierung von erweiterter in einfache Darstellung und Funktionalität

In diese Richtung findet keine Konvertierung statt. Es reicht, unter
"Einstellungen" - "Programmeinstellungen" den Haken bei "Erweiterten
Changelog Editor verwenden" zu entfernen.

Sollte zu diesem Zeitpunkt bereits ein Paket geladen sein, erfolgt
nachstehender Hinweis:

|image37|

Dies erfolgt aus Sicherheitsgründen, um keinen der bestehenden Einträge
zu verlieren.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
EPub-Generator <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Skriptbaum
----------

|image38|

Im Skriptbaum werden die einzelnen möglichen Steuerskripte für
opsi-winst dargestellt, inklusive der verwendeten Include-Dateien.

Mit einem Doppelklick kann ein vorhandenes Skript direkt aus der
Baumdarstellung heraus mit dem in den
\ `Einstellungen <#Programmeinstellungen>`__\  verknüpften Editor
(\ `intern <#ToolSkriptEditor>`__\  oder extern) geöffnet werden.

opsi-winst bietet die Möglichkeit, immer wiederkehrende Funktionen in
separate Dateien auszulagern, die dann per Include-Anweisung eingebunden
werden. Diese Include-Dateien werden dabei in der Regel von mehreren
Paketen referenziert.

Um zu verhindern, dass diese Skripte unbeabsichtigt oder aus
Unwissenheit heraus fehlerhaft geändert werden und diese Änderung sich
automatisch auf sämtliche Pakete auswirkt, die diese Skripte verwenden,
können daher aus der Baumdarstellung heraus nur Dateien geöffnet werden,
die sich im CLIENT\_DATA Ordner des aktuell geöffneten Pakets befinden.

Skripte, die nicht geändert werden können, werden in Klammern "( .. )"
dargestellt. Zusätzlich erhält der Anwender beim Versuch ein solches
Skript zu öffnen, eine Warnmeldung.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Web-basierte
iPhone-Dokumentation
erstellen <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Zeitplaner
----------

|image39|

Der Zeitplaner ermöglicht die Anlage und Verwaltung von zeitgesteuerten
(De-)Installationsaufträgen von localboot Paketen direkt am opsi Server.
Bitte die \ `technischen Voraussetzungen <#TechnischeHinweise>`__\ 
dafür unbedingt lesen!

Hinweis:

Da sowohl beim Öffnen des Zeitplaners, als auch nach dem Schließen des
Auftragsanlagedialogs die bestehenden Aufträge direkt vom Server
abgerufen werden, kann es einen Moment dauern. Bitte hier um etwas
Geduld, vor allem bei vielen vorhandenen Aufträgen.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| Funktion                | Hotkey                  | Beschreibung            |
+-------------------------+-------------------------+-------------------------+
| |image40|               | F1                      | Neue                    |
|                         |                         | (De-)Installationsauftr |
|                         |                         | äge                     |
|                         |                         | anlegen                 |
+-------------------------+-------------------------+-------------------------+
| |image41|               | F2                      | Einzelne, ausgewählte   |
|                         |                         | Aufträge löschen, es    |
|                         |                         | erfolgt eine            |
|                         |                         | Sicherheitsabfrage      |
+-------------------------+-------------------------+-------------------------+
| |image42|               | F3                      | Aktualisieren der       |
|                         |                         | Anzeige                 |
+-------------------------+-------------------------+-------------------------+
| |image43|               | F4                      | Sämtliche aktiven       |
|                         |                         | Aufträge entfernen, es  |
|                         |                         | erfolgt eine            |
|                         |                         | Sicherheitsabfrage      |
+-------------------------+-------------------------+-------------------------+
| |image44|               |                         | Schließen der Anzeige   |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

Erläuterungen zur Spalte "Aktion"

Hier werden die unterschiedlichen Auftragstypen angezeigt:

setup:                Installanstionsanforderung

uninstall:        Deinstallationsanforderung

wol:                Vor dem eigentlichen Auftrag wird ein Wake On Lan
Paket an die betreffende Maschine gesendet.

on\_demand:        Nachdem die Aufträge eingestellt worden sind, wird
ein "on\_demand" Ereignis ausgelöst.

Mit dem Personal Edition von HelpNDoc erstellt: \ `iPhone-Dokumentation
einfach
erstellen <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Aufträge anlegen
~~~~~~~~~~~~~~~~

|image45|

In diesem Dialog wird ein neuer (Massen-)Auftrag definiert. Bitte auf
jeden Fall auch die \ `technischen Hinweise <#TechnischeHinweise>`__\ 
beachten!

.. raw:: html

   <div class="rvps2">

+--------------------------------------+--------------------------------------+
| Feld / Funktion                      | Hinweis                              |
+--------------------------------------+--------------------------------------+
| Liste "Arbeitsplätze"                | Alle am opsi Server definierten      |
|                                      | Clients                              |
|                                      |                                      |
|                                      | Mit Hilfe der <Ctrl>-Taste können    |
|                                      | mehrere Arbeitsplätze auf einmal     |
|                                      | ausgewählt werden. Die Aufträge      |
|                                      | werden dann für alle ausgewählten    |
|                                      | Arbeitsplätzen gleichermaßen         |
|                                      | angelegt.                            |
+--------------------------------------+--------------------------------------+
| Liste "Produkte"                     | Sämtliche aktive localboot Pakete    |
|                                      |                                      |
|                                      | Die Auswahl erfolgt über die         |
|                                      | Kontrollkästchen vor der Produkt ID. |
+--------------------------------------+--------------------------------------+
| Kalenderansicht                      | Geplantes Datum der Aufträge, der    |
|                                      | aktuelle Tag ist dabei hervorgehoben |
+--------------------------------------+--------------------------------------+
| Uhrzeitfeld                          | Startzeit der Aufträge               |
+--------------------------------------+--------------------------------------+
| Durchzuführende Aktion               | Install = Setzt den                  |
|                                      | Anforderungsstatus des Pakets an der |
|                                      | Maschine auf "setup"                 |
|                                      |                                      |
|                                      | Uninstall = Setzt den                |
|                                      | Anforderungsstatus des Pakets an der |
|                                      | Maschine auf "uninstall"             |
|                                      |                                      |
|                                      | (Update = derzeit nicht verwendet)   |
+--------------------------------------+--------------------------------------+
| Event 'on\_demand'                   | Haken setzen, um einen on\_demand    |
|                                      | Auftrag pro Maschine zusätzlich      |
|                                      | erstellen zu lassen                  |
+--------------------------------------+--------------------------------------+
| Wake On Lan                          | Haken setzen, um einen WakeOnLan     |
|                                      | Auftrag pro Maschine zusätzlich      |
|                                      | erstellen zu lassen                  |
|                                      |                                      |
|                                      | Der WakeOnLan Auftrag wird mit dem   |
|                                      | in den                               |
|                                      | \ `Einstellungen <#opsiVerwaltungsbe |
|                                      | fehle>`__\                           |
|                                      | hinterlegten Vorlauf erstellt.       |
|                                      | Standardvorlauf ist 15 Minuten.      |
+--------------------------------------+--------------------------------------+
| |image46|                            | Joberzeugung anstoßen                |
+--------------------------------------+--------------------------------------+
| |image47|                            | Abbrechen, es werden keine Jobs      |
|                                      | erstellt.                            |
+--------------------------------------+--------------------------------------+

.. raw:: html

   </div>

Hinweise

Mit dem Personal Edition von HelpNDoc erstellt: \ `EPub-Bücher für das
iPad verfassen <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Technische Hinweise
~~~~~~~~~~~~~~~~~~~

Verwendung des Zeitplaners:

Die von opsi Package Builder verwalteten Softwareverwaltungsaufträge
werden im Hintergrund direkt am opsi Server als sogenannte AT Aufträge
eingestellt. Dazu ist die Installation des ATD Dämon und der zugehörigen
Kommandozeilentools erforderlich. Wie dieser Dämon zu installieren ist,
kann der technischen Beschreibung der verwendeten Linux Distribution,
auf der der opsi Server installiert ist, entnommen werden.

AT Aufträge bestehen technisch gesehen aus einzelnen Linux Skripten, die
in einer bestimmten Reihenfolge und zu einem vordefinierten Zeitpunkt
ausgeführt werden. Diese befinden sich im sogenannten Spool-Verzeichnis
des ATD Dämon und können durch den Anwender oder Administrator direkt an
der Serverkonsole über die Kommandozeilentools at, atq, atrm, etc.
verwaltet werden. opsi Package Builder verwendet die gleichen Tools zur
Pflege der AT Aufträge.

Wenn viele AT Aufträge angelegt werden, spielt es im Rahmen der
Verwaltung mittels opsi Package Builder eine große Rolle, wie viele
Dateien durch einen Benutzer gleichzeitig geöffnet werden dürfen, da der
opsi Package Builder beim Anlegen und Auslesen der Aufträge jeden
einzelnen Auftrag analysieren muss. Da in großen Netzwerken aufgrund der
hohen Rechneranzahl durchaus viele Aufträge vorhanden sein können, ist
es gar nicht selten, dass auch mehrere tausend Aufträge erzeugt werden.

Linux ist als Betriebssystem in einem hohen Maß konfigurierbar, um u. a.
vielen Einsatzmöglichkeiten gerecht zu werden. Aus Sicherheitsgründen
läßt sich daher die Anzahl der gleichzeitig zu öffnenden Dateien
limitieren. Dieses Limit wird auch 'ulimit' genannt. Wenn dieses Limit
zu gering eingestellt ist, kann es bei der Verwaltung der AT Aufträge zu
Fehlern kommen. Daher sollte das eingestellte Limit VOR der Anlage einer
größeren Anzahl von Aufträgen auf jeden Fall kontrolliert und ggf.
angepasst werden.

Um das ulimit zu überprüfen, meldet man sich am opsi Server direkt als
root Benutzer an und setzt folgendes Kommando ab: ulimit -n

Die damit ermittelte Zahl entspricht der Anzahl der gleichzeitig
geöffneten Dateien. In vielen Fällen wird dieser Wert auf 1024
eingestellt sein, sofern man nicht bereits vorher Anpassungen
vorgenommen hat. Um diesen Wert dauerhaft zu erhöhen, muss ein evtl.
bereits vorhandener Eintrag in der Datei /etc/security/limits.conf
angepasst oder eine neue Zeile hinzugefügt werden. Um bspw. diesen Wert
auf 5000 zu erhöhen, wird folgender Eintrag benötigt:

\* soft nofile 5000

Dabei haben die 4 Werte folgende Bedeutung:

\*        - der Eintrag gilt für jeden Benutzer -> damit ließe sich die
Anzahl der offenen Dateien auch nur speziell für den opsi-admin Benutzer
anpassen

soft        - der Wert kann nachträglich durch den Benutzer wieder
geändert werden

nofile        - der Eintrag regelt die Anzahl der offenen Dateien

5000        - Wert der eingestellt werden soll

Mit der beispielhaft angegeben Zeile wird also für jeden User die Anzahl
der gleichzeitig offenen Dateien nachträglich änderbar auf 5000 gesetzt.

Zusätzlicher Hinweis zu CentOS (aufgetreten bei Version 6.4), könnte
aber auch bei anderen Linux-Distributionen wichtig sein:

Sollte der ATD zwischen der Abarbeitung der Jobs immer eine Pause
einlegen (1 od. mehrere Minuten), dann kann das folgendermaßen
korrigiert werden:

In der Datei /etc/sysconfig/atd dafür sorgen, dass die OPTS-Variable mit
den Parametern -b 0 ergänzt wird. Falls die Variable noch gar nicht
vorhanden ist, den folgenden Eintrag ans Ende der Datei anhängen:

OPTS="-b 0"

Der Parameter -b 0 deaktiviert die Pause zwischen der Ausführung der
einzelnen AT-Jobs.

Ist der Wert eingetragen und gespeichert, muss der ATD neu gestartet
werden. Unter CentOS 6.4 kann das durch einen service atd restart Befehl
an der Konsole als root User erfolgen.

(Diese Beschreibung gilt nur für CentOS, dass die Startparameter für den
ATD aus der genannten Datei zieht. Es ist im Einzelfall pro Distribution
zu prüfen, wo der genannte Parameter eingefügt werden muss, damit der
ATD die Anpassung beim Neustart mitbekommt.)

Verwendung des Auftragsanlagedialogs:

-  Beim ersten Öffnen werden sämtliche Maschinen und aktiven Localboot
   Produkte vom opsi Server ermittelt. Das kann bei einer hohen Anzahl
   Clients und Produkten einige Zeit in Anspruch nehmen! Bitte hier
   Geduld bewahren. Der Auslesevorgang findet auch nur einmalig nach
   Programmstart statt, außer es wurde in den Einstellungen der Haken
   bei "Beim Öffnen des Zeitplaners Maschinen und Produkte immer
   einlesen" gesetzt. Dann werden die Daten bei jedem Öffnen des
   Zeitplaners ermittelt.
-  Wenn viele Aufträge auf einmal am Server eingestellt werden sollen,
   bitte Geduld bewahren! Das kann eine je nach Menge eine Weile in
   Anspruch nehmen:
   Beispielrechnung: 100 Clients á 5 Produkte, inkl. on\_demand und wol
   bedeutet 700 (!) Einzelaufträge
   In solchen Fällen kann es sinnvoll sein, statt der Einzelaufträge ein
   Paketbündel anzulegen und die (wie in diesem Beispiel 5) Produkte
   zusammenzufassen. Das senkt die Anzahl der Aufträge maximal.
   Für die \ `Schnellanlage von Paketbündeln <#Paketbndelerzeugen>`__\ 
   kann die daüfr vorgesehen Funktion in opsi Package Builder genutzt
   werden.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Kindle eBooks
Generator <http://www.helpndoc.com/de/funktionen-tour/ebooks-fuer-den-amazon-kindle-erstellen>`__

Paketbündel erzeugen
--------------------

|image48|

Mit der Funktion "Paketbündel erzeugen" können sog.
Meta-Installationspakete erstellt werden. Diese Pakete beinhalten
keinerlei Skriptfunktionalität, sondern bestehen nur aus Abhängigkeiten
zu anderen Paketen.

Beispiel:

Auf allen Clients sollen immer wieder die gleichen 15 Softwarepakete
installiert werden. Um nicht bei jedem Client 15 Pakete auf "setup"
setzen zu müssen mit der Gefahr, einzelne Pakete oder Clients
auszulassen, kann alternativ ein weiteres Paket erzeugt werden, das eine
Abhängigkeit zu allen anderen 15 Paketen besitzt. Wird dieses Paket auf
"setup" gesetzt, wird es gemäß seiner Abhängigkeiten erst dann
installiert, wenn sämtliche anderen, abhängigen Pakete erfolgreich
installiert worden sind.

Damit lassen sich sehr leicht gruppen- und zweckorientierte
Anwendungspakete schnüren.

Vorgehensweise

Um mit Hilfe von opsi Package Builder solche Bündel zu erzeugen, einfach
wie folgt vorgehen:

#. Über den Startdialog oder das Anwendungsmenü die Funktion
   "Paketbündel erzeugen" auswählen Daraufhin werden sämtliche aktiven
   Localboot Pakete des verbundenen opsi Servers ermittelt (sofern noch
   nicht geschehen, bspw. durch Öffnen des Zeitplaners) und in einer
   Tabelle dargestellt.
#. Die zu bündelnden Produkte mit einem Haken vor der Produkt ID
   versehen.
#. Den Dialog mit der Schaltfläche "OK" bestätigen.
#. In der nachfolgenden Abfrage eine neue Produkt ID für das Meta-Paket
   erfassen und den Dialog mit "Ok" bestätigen. Es wird geprüft, ob ein
   Paket gleichen Namens existiert.

Damit ist generell ein neues Paket mit den entsprechenden Gegebenheiten
angelegt. Soll das Paket jetzt noch zusätzlich direkt auf dem Server
gebaut und installiert werden, so auch den nachfolgenden Dialog mit "Ja"
bestätigen.

|image49|

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis EPub und
Dokumentationsgenerator <http://www.helpndoc.com/de>`__

Depot Manager
-------------

|image50|

Mit dem Depot Manager können Verwaltungsaufgaben im Bereich der
Softwaredepots vorgenommen. Hierzu gehören:

- Einlesen der einzelnen Depotstände

- Einlesen des Repository Ordners (/var/lib/opsi/repository)

- Vergleichen verschiedener Depots untereinander, hierbei sind alle
Kombination möglich: Depot<->Depot, Repo<->Repo und Depot<->Repo

- Installieren / Deinstallieren /Upload von Paketen in einzelne Depots

- Löschen von Paketen aus dem Repository Verzeichnis

Hinweis:

Die Depotfunktionen sind bei der ersten Inbetriebnahme deaktiviert und
können in den Einstellungen, Reiter opsi Verwaltungsbefehle aktiviert
werden. Nach erfolgtem Neustart

derAnwendung werden autom. alle Depots vom Configserver ermittelt.

.. raw:: html

   <div class="rvps2">

+-------------------------+-------------------------+-------------------------+
| |image51|               | Die Tabellenanzeige     | Der Schalter arbeitet   |
|                         | schaltet zwischen       | wie ein Umschalter, d.  |
| |image52|               | Depotansicht und        | h. so lange er farbig   |
|                         | Repository              | markiert ist, wird der  |
|                         | Ordneransicht um.       | Inhalt des Repository   |
|                         |                         | Ordners angezeigt.      |
|                         |                         |                         |
|                         |                         | Ist diese Funktion      |
|                         |                         | gewählt, zeigt die      |
|                         |                         | Spalte "Typ" der        |
|                         |                         | Tabelle die MD5 Summe   |
|                         |                         | des Pakets an.          |
+-------------------------+-------------------------+-------------------------+
| |image53|               | Beendet den Dialog      |                         |
+-------------------------+-------------------------+-------------------------+
| |image54|               | | Vergleich der beiden  | Der Schalter arbeitet   |
|                         |   Tabelleninhalte       | wie ein Umschalter, d.  |
| |image55|               |   durchführen.          | h. so lange er farbig   |
|                         | |                       | markiert ist, werden in |
|                         | | WICHTIG: Werden REPO  | den beiden Tabellen nur |
|                         |   Stände miteinander    | die Unterschiede        |
|                         |   verglichen, so        | angezeigt.              |
|                         |   erfolgt der Vergleich |                         |
|                         |   inklusive MD5 der     | Während der Vergleich   |
|                         |   Datei.                | durchgeführt wird, ist  |
|                         |                         | die Schrift rot, nach   |
|                         |                         | Abschluss des           |
|                         |                         | Vergleichs grün.        |
+-------------------------+-------------------------+-------------------------+
| |image56|               | Depots und Depotstände  | Achtung: Die            |
|                         | neu einlesen            | vorhandenen Depotserver |
|                         |                         | werden über einen       |
|                         |                         | Programmneustart hinaus |
|                         |                         | zwischengespeichert!    |
|                         |                         | Falls Server in der     |
|                         |                         | Auflistung fehlen, kann |
|                         |                         | einmaliges Neueinlesen  |
|                         |                         | helfen.                 |
+-------------------------+-------------------------+-------------------------+
| |image57|               | Vergleichsreporte       |                         |
|                         | generieren              |                         |
+-------------------------+-------------------------+-------------------------+
| |image58|               | Paket in ein Depot      | Es wird nach dem        |
|                         | installieren            | Zieldepot gefragt.      |
+-------------------------+-------------------------+-------------------------+
| |image59|               | Diese Schaltfläche      | Die Schaltfläche ändert |
|                         | erfüllt eine            | ihre Funktionsweise je  |
| |image60|               | Doppelfunktion:         | nachdem, was in der     |
|                         |                         | zuletzt angeklickten    |
|                         | Deinstallieren: das     | Tabelle gerade          |
|                         | zuletzt angeklickte     | angezeigt wird.         |
|                         | Paket in einer der      |                         |
|                         | beiden Tabellen wird    |                         |
|                         | auf dem zugehörigen     |                         |
|                         | Depot deinstalliert     |                         |
|                         |                         |                         |
|                         | Löschen: das zuletzt    |                         |
|                         | angeklickte Paket wird  |                         |
|                         | aus dem Repository      |                         |
|                         | Ordner (auf             |                         |
|                         | Dateisystemebene)       |                         |
|                         | gelöscht                |                         |
|                         |                         |                         |
|                         | (Mehrfachauswahl        |                         |
|                         | möglich)                |                         |
+-------------------------+-------------------------+-------------------------+
| |image61|               | Paket in ein Repository | Die temporär auf den    |
|                         | hochladen. Dabei wird   | Configserver            |
|                         | das Paket erst auf den  | übertragene Datei wird  |
|                         | Configserver in ein     | sicherheitshalber nicht |
|                         | temporäres Verzeichnis  | autom. gelöscht.        |
|                         | geschrieben             |                         |
|                         | ("!inst\_tmp!"          |                         |
|                         | unterhalb der           |                         |
|                         | opsi\_workbench) und    |                         |
|                         | dann per                |                         |
|                         | "opsi-package-manager   |                         |
|                         | -u -d" verarbeitet.     |                         |
+-------------------------+-------------------------+-------------------------+
| |image62|               | Hebt die Registrierung  |                         |
|                         | des Depotservers am     |                         |
|                         | Konfigserver auf. Damit |                         |
|                         | wird der Depotserver    |                         |
|                         | ABER NICHT gelöscht,    |                         |
|                         | sondern nur aus der     |                         |
|                         | internen Hosttabelle    |                         |
|                         | entfernt!               |                         |
+-------------------------+-------------------------+-------------------------+
| |image63|               | Führt den Befehl        | Kann nur dann verwendet |
|                         | "opsi-setup             | werden, wenn "Hole REPO |
|                         | --set-rights            | Inhalt" aktiv ist.      |
|                         | /var/lib/opsi/repositor |                         |
|                         | y"                      | Ist bspw. dann          |
|                         | auf dem ausgewählten    | erforderlich, wenn auf  |
|                         | Depot aus.              | den Inhalt einer        |
|                         |                         | MD5-Datei eines Pakets  |
|                         |                         | nicht zugegriffen       |
|                         |                         | werden kann.            |
+-------------------------+-------------------------+-------------------------+
| |image64|               | Führt den Befehl        | Kann nur dann verwendet |
|                         | "opsi-package-updater   | werden, wenn "Hole REPO |
|                         | -vv" auf dem gewählten  | Inhalt" aktiv ist.      |
|                         | Depot aus.              |                         |
+-------------------------+-------------------------+-------------------------+
| |image65|               | Generiert für die       |                         |
|                         | ausgewählten Produkte   |                         |
|                         | auf dem betreffenden    |                         |
|                         | Repository die MD5      |                         |
|                         | Dateien.                |                         |
+-------------------------+-------------------------+-------------------------+
| |image66|               | Ping-Check auf das      |                         |
|                         | gewählte Depot          |                         |
+-------------------------+-------------------------+-------------------------+
| |image67|               | Reboot eines Depots     |                         |
+-------------------------+-------------------------+-------------------------+
| |image68|               | Shutdown eines Depots   |                         |
+-------------------------+-------------------------+-------------------------+
| |image69|               | Anzeige des Logbuchs    |                         |
+-------------------------+-------------------------+-------------------------+

.. raw:: html

   </div>

Beispiel I für eine Vergleichssituation zwischen zwei Depots:

|image70|

Im linken Depot befinden sich jede Menge Produkte, die das rechte Depot
nicht kennt. Umgekehrt hat das rechte ein zusätzlich Produkt.

Beispiel II für eine Vergleichssituation zwischen Depot und Repository
Ordner:

|image71|

Wie man erkennen kann, sind folgende Funktionen aktiv:

- linke Tabelle: Ansicht Repository Ordner

- rechte Tabelle: Depot

- Vergleichsmodus ist eingeschaltet

-> Im rechten Repo sind 4 Pakete vorhanden, die sich im linken Depot
nicht befinden.

Hinweis:

Das in der Spalte "Typ" nur "(depo<->repo)" angezeigt wird, liegt daran,
dass im Repository Ordner die Produkttypen "NetbootProduct" bzw.
"LocalbootProduct" nicht einfach ermittelbar sind.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
EPub-Generator <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Report generieren
~~~~~~~~~~~~~~~~~

|image72|

Mit Hilfe des Reportauswahl-Dialogs können gezielt Depotvergleiche
durchgeführt und als druckbare HTML Reporte ausgegeben werden.

HINWEIS:

Wird als Vergleichsbasis "Inhalt Repository Ordner" gewählt, kann die
Berichtsgenerierung bei einer großen Serveranzahl recht lange dauern.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
EBook-Editor <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Client Agent verteilen
----------------------

|image73|

Erläuterung zur Option "Nicht warten":

Wird diese Option angewählt, so wird der Deploy Befehl auf dem Server
abgesetzt und nicht auf die Beendigung der Ausführung gewartet, d. h. es
gibt keine Rückmeldung über das PLINK Log. Bei größeren Deploys führt
das dazu, dass der opsiPackageBuilder nicht "ewig" zu hägen scheint,
sondern man kann direkt weiterarbeiten.

Hinweise zum Feld "Vorab-Befehl":

Steht in diesem Fehle eine Anweisung, so wird sie vor dem Deploy via
winexe (entspricht weitestgehend psexec für Linux) direkt auf dem Client
ausgeführt.

| 
| Daran sind allerdings einige Bedingungen geknüpft:

- Auf dem Server muss das Programm 'winexe' über die Pfadvariable
erreichbar sein vorhanden sein (mit whereis prüfen) / hierbei wird nicht
auf die im opsi-client-agent mitgelieferte Version zurückgegriffen.

- Er kann nur auf einen einzelnen Client abgesetzt werden. Bei
Verteilung an mehrere Clients ist der Eintrag außer Kraft.

- Befehlsverkettung funktioniert begrenzt. && und \|\| müssen in normale
Anführungszeichen (kein Apostroph) gesetzt werden, bspw. "&&" oder
"\|\|"

- Piping und Ausgabeumlenkung sind sehr fallabhängig. Da hilft nur
opsiPackageBuilder Log einschalten und ausprobieren.

.. raw:: html

   <div class="rvps2">

+--------------------------------------------------------------------------+
| Beispiel:                                                                |
|                                                                          |
| - folgender Befehl soll abgesetzt werden:                cd              |
| c:\\TEMP\\RZInstall\\ETHLineSpeed && set NWDUPLEXMODE=AUTOSENS && start  |
| install.cmd                                                              |
|                                                                          |
| - gem. obiger Hinweise muss in das Feld:        cd                       |
| c:\\TEMP\\RZInstall\\ETHLineSpeed "&&" set NWDUPLEXMODE=AUTOSENS "&&"    |
| start install.cmd                                                        |
|                                                                          |
| - opsiPackageBuilder macht daraus im Hintergrund (plink Authorisation,   |
| Port können ja nach Einstellung variieren):                              |
|                                                                          |
| "plink.exe" -batch -P 22 <opsi admin>@<config server> -pw                |
| "<opsiserverpass>" winexe --debug-stderr --user "esaadm" --password      |
| "<localadminpass>" //client 'cmd /c cd c:\\TEMP\\RZInstall\\ETHLineSpeed |
| "&&" set NWDUPLEXMODE=AUTOSENS "&&" start install.cmd'                   |
|                                                                          |
| Das Kommando wir natürlich ohne Zeilenumbrüche abgesetzt. Die Werte in   |
| <> sind entsprechend der eigenen Umgebung zu ersetzen.)                  |
|                                                                          |
| Am besten ist es, den zu setzenden Befehl per Hand auf der Kommandozeile |
| erst an einer Maschine zu prüfen und dann entsprechend im Feld zu        |
| hinterlegen. Die letzten 20 Befehle werden in der INI Datei gespeichert  |
| und bleiben somit für zukünftige Verwendung erhalten (Sollte in einem    |
| dieser Befehle das Paragraphensymbol "§" verwendet worden sein, wird die |
| Liste beim erneuten Öffnen des Dialogs merkwürdig aussehen, da dieses    |
| Symbol intern für die Trennung der Kombobox Elemente verwendet wird.)    |
|                                                                          |
                                                                          
+--------------------------------------------------------------------------+

.. raw:: html

   </div>

Achtung:

- Wird an einen einzelnen Client verteilt, so kann im Multi-Depot
Betrieb der Quelldepotserver ausgewählt werden, um Leitungskapazitäten
zu schonen.

- Wenn an mehrere Clients verteilt wird, dann kann im Multi-Depot
Betrieb KEIN Depotserver ausgewählt werden, da für den Deploybefehl eine
Liste in Dateiform erstellt werden muss. Dies ist momentan nur auf dem
Workbench Share des zugeordneten Konfigservers zulässig. Ebenfalls führt
es zu Fehlern, wenn der Entwicklungsordner nicht auf dem Workbench Share
des Konfigservers liegt. Dann kann der Deploybefehl ebenfalls nicht
ordnungsgemäß abgesetzt werden.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Benutzerfreundliches
Werkzeug zum Erstellen von HTML-Hilfedateien und
Hilfewebsites <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Menü
====

Das Hauptmenü im Einzelnen.

`Menü "Datei" <#Datei>`__

`Menü "Werkzeuge" <#Werkzeuge>`__

`Menü "Extras" <#Extras>`__

`Menü "?" <#NeuesThema>`__

Erläuterungen erfolgen in den einzelnen Kapiteln, falls notwendig.

Mit dem Personal Edition von HelpNDoc erstellt: \ `EBooks einfach
erstellen <http://www.helpndoc.com/de/funktionen-tour>`__

Datei
-----

|image74|

Mit dem Personal Edition von HelpNDoc erstellt: \ `eBooks für den Kindle
verfassen <http://www.helpndoc.com/de/funktionen-tour/ebooks-fuer-den-amazon-kindle-erstellen>`__

Werkzeuge
---------

|image75|

-  Skripte neu scannen
   Wenn Änderungen an den Installationsskripten durchgeführt und
   insbesondere weitere Include- oder Sub-Anweisungen eingebaut wurden,
   so kann die Paketstruktur hiermit für eine korrekte Darstellung im
   Skriptbaum neu eingelesen werden.

-  Paketrechte setzen
   Die Linux-seitig bestehenden Verzeichnisrechte auf den opsi Standard
   korrigieren. Dazu ist allerdings in den
   \ `Einstellungen <#Allgemein>`__\  die Hinterlegung des root
   Kennworts des opsi Servers notwendig.
-  Start opsi-winst
   Starten der opsi-winst Entwicklungsoberfläche zum Starten/ Überwachen
   und Debuggen von opsi-winst Skripten.
   Der Menüpunkt setzte eine bestehende opsi-winst-client Installation
   voraus, bzw sucht die winst32.exe in folgendem Pfad:
   %ProgramFiles%\\opsi.org\\opsi-client-agent\\opsi-winst\\winst32.exe
-  Skripteditor
   Startet den in den Einstellungen hinterlegten Editor.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Hilfegenerator <http://www.helpndoc.com/de/funktionen-tour>`__

Extras
------

|image76|

-  Zeige PLINK Log
   Für den Fall, die Anzeige des PLINK Logs nach erfolgter
   Onlinefunktion wurde in den Einstellungen abgeschaltet, kann die
   Anzeige hier manuell aufgerufen werden.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
Kindle-Hersteller <http://www.helpndoc.com/de/funktionen-tour/ebooks-fuer-den-amazon-kindle-erstellen>`__

?
-

|image77|

-  Nach Updates suchen
   Manuellen Aktualisierung der installierten Version von opsi Package
   Builder durchführen, falls eine neuere Version verfügbar ist.
-  Zeige Changelog
   Das opsi Package Builder Versions-Changelog anzeigen (im Gegensatz
   zum Paket-Changelog!)

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Multiformat-Hilfsgenerator <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Einstellungen
=============

Nachfolgend werden die einzelnen Bestandteile des Einstellungen Dialog
kurz aufgezeigt:

`Allgemein <#Allgemein>`__

`Programmeinstellungen <#Programmeinstellungen>`__

`opsi Verwaltungsbefehle <#opsiVerwaltungsbefehle>`__

`Automatische Updates <#Nachrichten>`__

Hinweis: es kann mehr als eine Konfiguration parallel betrieben werden.
Genaueres zum Vorgehen dazu unter \ `Mehrere
Konfigurationen. <#MehrereKonfigurationen>`__

Mit dem Personal Edition von HelpNDoc erstellt: \ `Benutzerfreundliches
Werkzeug zum Erstellen von HTML-Hilfedateien und
Hilfewebsites <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Allgemein
---------

|image78|

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
Webhilfegenerator <http://www.helpndoc.com/de>`__

Programmeinstellungen
---------------------

|image79|

Mit dem Personal Edition von HelpNDoc erstellt: \ `EPub-Bücher für das
iPad verfassen <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

opsi Verwaltungsbefehle
-----------------------

|image80|

Mit dem Personal Edition von HelpNDoc erstellt: \ `iPhone-Dokumentation
einfach
erstellen <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Nachrichten
-----------

|image81|

Mit dem Personal Edition von HelpNDoc erstellt: \ `Elektronische Bücher
einfach verfassen <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Automatische Updates
--------------------

|image82|

Mit dem Personal Edition von HelpNDoc erstellt: \ `iPhone Websites
einfach
gemacht <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Tool "Skript Editor"
====================

Zusatztool "Skript Editor"

Ab opsi Package Builder Version 5.3 wird ein kleiner Skripteditor
mitinstalliert. Dieser Skripteditor kann, wenn entsprechend
konfiguriert, direkt über den Skriptbaum oder über den Link im Startmenü
aufgerufen werden.

|image83|

Wesentliche Merkmale:

-  Farbige Syntaxhervorhebung
-  "Falten" des Quellcodes (optional: kompakt, mit Kommentaren)
-  Lexerdefinition anpassbar (dazu muss der Editor per Startmenü Eintrag
   aufgerufen werden)
-  Autocomplete für Syntaxelemente und Variablen
-  Frei definierbare und wiederverwendbare Codeblöcke ("Snippets")

Die Kernkomponente des Editors bildet das Modul
"\ `Scintilla <http://www.scintilla.org/>`__\ ", welches auch in
bekannten Editoren, wie bspw.
\ `Notepad++ <http://notepad-plus-plus.org/>`__\ , verwendet wird. Die
lexikalischen Elemente (Syntaxhervorhebung und Faltung) sind allerdings
komplett in AutoIt geschrieben ist, da Scintilla für opsi Skripte kein
eigenes Modul zur Darstellung mitliefert. Dadurch, dass AutoIt eine
Interpretersprache ist, ist er damit langsamer als andere Editoren und
eignet sich daher nur bedingt zur Bearbeitung sehr großer Skripte, vor
allem bei eingeschalteter Syntaxhervorhebung und/oder Faltung. In den
\ `Einstellungen <#Programmeinstellungen>`__\  von opsi Package Builder
lässt sich jedoch vorgeben, ob der Editor mit diesen Funktionen
überhaupt aufgerufen wird oder nicht, sofern der Aufruf direkt über den
Skriptbaum erfolgt. Bei einem Aufruf über den Link im Startmenü sind
Syntaxhervorhebung und Faltung generell beim Start ausgeschaltet und
können über das Editormenü "Ansicht" aktiviert werden.

Alle weiteren Menüfunktionen entsprechen denen gängiger Editoren und
werden nicht weiter beschrieben.

(Der Editor kann auch über die Kommandozeile aufgerufen werden. Weitere
Informationen zu den möglichen Kommandozeilenparametern können mit der
Option "--help" aufgerufen werden.)

Mit dem Personal Edition von HelpNDoc erstellt: \ `EPub-Bücher einfach
erstellen <http://www.helpndoc.com/de/funktionen-tour>`__

Tutorial
========

(Muss noch geschrieben werden...)

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
Multiformat-Hilfsgenerator <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Kommandozeilenparameter
=======================

Kommandozeilenparameter für opsi Package Builder

Neben der normalen Fensteroberfläche lassen sich zur Automatisierung
einige Funktionen per Kommandozeile aufrufen. Nachfolgend eine
Aufstellung der Möglichen Parameter und Kombinationen. Die Parameter
können hierbei sowohl in Lang- als auch in Kurzform geschrieben werden
(siehe Beipiele unten).

WICHTIG: siehe auch die Hinweise bei Verwendung mehrerer Konfigurationen
\ `hier <#MehrereKonfigurationen>`__

.. raw:: html

   <div class="rvps2">

+--------------------+--------------------+--------------------+--------------------+
| Kurz               | Lang               | Beschreibung       | Hinweise           |
+--------------------+--------------------+--------------------+--------------------+
| -p                 | --path             | Paketname oder     | Hier kann entweder |
|                    |                    | -pfad              | der komplette Pfad |
|                    |                    |                    | zum                |
|                    |                    |                    | Entwicklungsordner |
|                    |                    |                    | oder nur der Name  |
|                    |                    |                    | des Pakets         |
|                    |                    |                    | angegeben sein:    |
|                    |                    |                    |                    |
|                    |                    |                    | Hinweis: ein Pfad  |
|                    |                    |                    | außerhalb des in   |
|                    |                    |                    | den Einstellungen  |
|                    |                    |                    | hinterlegten       |
|                    |                    |                    | Entwicklungsordner |
|                    |                    |                    | s                  |
|                    |                    |                    | ist nicht          |
|                    |                    |                    | zulässig.          |
+--------------------+--------------------+--------------------+--------------------+
| -w                 | --no-netdrv        | Entwicklungsordner | Falls das Programm |
|                    |                    | nicht mounten      | so eingestellt     |
|                    |                    |                    | ist, dass es beim  |
|                    |                    |                    | Start zuerst       |
|                    |                    |                    | versucht, die      |
|                    |                    |                    | Freigabe           |
|                    |                    |                    | opsi\_workbench    |
|                    |                    |                    | als Laufwerk zu    |
|                    |                    |                    | mappen, so kann    |
|                    |                    |                    | das mit dieser     |
|                    |                    |                    | Option deaktiviert |
|                    |                    |                    | werden. Das ist    |
|                    |                    |                    | dann sinnvoll,     |
|                    |                    |                    | wenn in einem      |
|                    |                    |                    | größeren Script    |
|                    |                    |                    | das Verzeichnis    |
|                    |                    |                    | vorher manuell     |
|                    |                    |                    | zugeordnet wurde.  |
+--------------------+--------------------+--------------------+--------------------+
| -b                 | --build            | Paketieren         | Diese Option hat   |
|                    |                    |                    | zusätzlich vier    |
|                    |                    |                    | verschiedene       |
|                    |                    |                    | Parameter:         |
|                    |                    |                    |                    |
|                    |                    |                    | | a)               |
|                    |                    |                    |   --build=cancel   |
|                    |                    |                    | | Besteht das      |
|                    |                    |                    |   Paket bereits,   |
|                    |                    |                    |   erfolgt keine    |
|                    |                    |                    |   Paketierung      |
|                    |                    |                    |   (Vorgabe).       |
|                    |                    |                    |                    |
|                    |                    |                    | | b)               |
|                    |                    |                    |   --build=rebuild  |
|                    |                    |                    | | Ein bestehendes  |
|                    |                    |                    |   Paket wird mit   |
|                    |                    |                    |   der gleichen     |
|                    |                    |                    |   Versionierung    |
|                    |                    |                    |   überschrieben.   |
|                    |                    |                    |                    |
|                    |                    |                    | | c) --build=new   |
|                    |                    |                    | | Die              |
|                    |                    |                    |   Paketversionsnum |
|                    |                    |                    | mer                |
|                    |                    |                    |   wird um einen    |
|                    |                    |                    |   Zeitstempel      |
|                    |                    |                    |   erweitert und es |
|                    |                    |                    |   wird neu         |
|                    |                    |                    |   paketiert.       |
|                    |                    |                    |                    |
|                    |                    |                    | | d)               |
|                    |                    |                    |   --build=interact |
|                    |                    |                    | ive                |
|                    |                    |                    | | Der Anwender     |
|                    |                    |                    |   wird interaktiv  |
|                    |                    |                    |   um eine          |
|                    |                    |                    |   Entscheidung     |
|                    |                    |                    |   gebeten (nicht   |
|                    |                    |                    |   mit --quiet),    |
|                    |                    |                    |   falls das Paket  |
|                    |                    |                    |   existiert.       |
|                    |                    |                    |                    |
|                    |                    |                    | Beispiel zum       |
|                    |                    |                    | Zeitstempel der    |
|                    |                    |                    | Variante c):       |
|                    |                    |                    |                    |
|                    |                    |                    | | Paketname mit    |
|                    |                    |                    |   ursprünglicher   |
|                    |                    |                    |   Versionsnummerie |
|                    |                    |                    | rung:              |
|                    |                    |                    | | ->               |
|                    |                    |                    |   productname\_2.5 |
|                    |                    |                    | -1                 |
|                    |                    |                    |                    |
|                    |                    |                    | Paketname mit      |
|                    |                    |                    | zusätzlichem       |
|                    |                    |                    | Zeitstempel:       |
|                    |                    |                    |                    |
|                    |                    |                    | ->                 |
|                    |                    |                    | productname\_2.5-1 |
|                    |                    |                    | .corr170739corr    |
|                    |                    |                    |                    |
|                    |                    |                    | Bei Variante c)    |
|                    |                    |                    | werden immer neue  |
|                    |                    |                    | Pakete erzeugt.    |
|                    |                    |                    | Hierbei ist auf    |
|                    |                    |                    | den                |
|                    |                    |                    | Speicherplatzbedar |
|                    |                    |                    | f                  |
|                    |                    |                    | zu achten!         |
+--------------------+--------------------+--------------------+--------------------+
| -i                 | --install          | Paket auf opsi     | Sollte in den      |
|                    |                    | Server             | Einstellungen      |
|                    |                    | installieren       | "Depotfunktionen   |
|                    |                    |                    | aktivieren"        |
|                    |                    |                    | gesetzt sein, wird |
|                    |                    |                    | diese Einstellung  |
|                    |                    |                    | temporär           |
|                    |                    |                    | deaktiviert und    |
|                    |                    |                    | der ursprünglich   |
|                    |                    |                    | konfigurierte      |
|                    |                    |                    | Installationsbefeh |
|                    |                    |                    | l                  |
|                    |                    |                    | verwendet.         |
+--------------------+--------------------+--------------------+--------------------+
| -s                 | --instsetup        | Paket installieren | Kann nicht mit     |
|                    |                    | und auf allen      | --install          |
|                    |                    | Clients Aktion auf | kombiniert werden. |
|                    |                    | "setup" setzen, wo |                    |
|                    |                    | der Produktstatus  |                    |
|                    |                    | "installed" ist    |                    |
+--------------------+--------------------+--------------------+--------------------+
| -u                 | --uninstall        | Paket auf opsi     | Sollte in den      |
|                    |                    | Server             | Einstellungen      |
|                    |                    | deinstallieren     | "Depotfunktionen   |
|                    |                    |                    | aktivieren"        |
|                    |                    |                    | gesetzt sein, wird |
|                    |                    |                    | diese Einstellung  |
|                    |                    |                    | temporär           |
|                    |                    |                    | deaktiviert und    |
|                    |                    |                    | der ursprünglich   |
|                    |                    |                    | konfigurierte      |
|                    |                    |                    | Deinstallationsbef |
|                    |                    |                    | ehl                |
|                    |                    |                    | verwendet.         |
+--------------------+--------------------+--------------------+--------------------+
| -r                 | --set-rights       | Paketverzeichnisre |                    |
|                    |                    | chte               |                    |
|                    |                    | neu setzen         |                    |
+--------------------+--------------------+--------------------+--------------------+
| -n                 | --no-gui           | Starte ohne        | Die Ausgabe von    |
|                    |                    | Oberfläche         | Meldungen erfolgt  |
|                    |                    |                    | im aufrufenden CMD |
|                    |                    |                    | - Fenster.         |
+--------------------+--------------------+--------------------+--------------------+
| -x                 | --no-update        | Deaktiviere den    | Überschreibt die   |
|                    |                    | internen Updater   | im Einstellungen   |
|                    |                    | dauerhaft          | Dialog gesetzte    |
|                    |                    |                    | Option.            |
+--------------------+--------------------+--------------------+--------------------+
| -q                 | --quiet            | Kein Ausgabe       | Das Programm kehrt |
|                    |                    |                    | nach Aufruf ohne   |
|                    |                    |                    | weitere Meldungen  |
|                    |                    |                    | zum Prompt zurück. |
|                    |                    |                    | Ist gleichzeitig   |
|                    |                    |                    | der Parameter      |
|                    |                    |                    | --log angegeben,   |
|                    |                    |                    | so werden          |
|                    |                    |                    | weiterhin alle     |
|                    |                    |                    | Meldungen in der   |
|                    |                    |                    | Log-Datei          |
|                    |                    |                    | protokolliert.     |
|                    |                    |                    |                    |
|                    |                    |                    | Hinweis: kann      |
|                    |                    |                    | nicht mit          |
|                    |                    |                    | --build=interactiv |
|                    |                    |                    | e                  |
|                    |                    |                    | verwendet werden!  |
+--------------------+--------------------+--------------------+--------------------+
| -l                 | --log              | | Schreibe         | | Wir nur --log    |
|                    |                    |   sämtliche        |   angegeben, so    |
|                    |                    |   Ausgaben in      |   schreibt opsi    |
|                    |                    |   Log-Datei        |   Package Builder  |
|                    |                    | | (auch bei        |   die Datei        |
|                    |                    |   --quiet)         |   standardmäßig in |
|                    |                    |                    |   den              |
|                    |                    |                    | | Ordner           |
|                    |                    |                    |   %AppData%\\opsi  |
|                    |                    |                    |   PackageBuilder.  |
|                    |                    |                    | |                  |
|                    |                    |                    |                    |
|                    |                    |                    | Beispiel um eine   |
|                    |                    |                    | andere Log-Datei   |
|                    |                    |                    | anzulegen:         |
|                    |                    |                    |                    |
|                    |                    |                    | --log=c:\\temp\\op |
|                    |                    |                    | sipackagebuilder.l |
|                    |                    |                    | og                 |
+--------------------+--------------------+--------------------+--------------------+
| -d                 | --debug            | Schreibe           | Hier werden        |
|                    |                    | zusätzliche Debug  | zusätzliche Debug  |
|                    |                    | Informationen      | Ausgaben erzeugt.  |
|                    |                    |                    | Im Regelfall nicht |
|                    |                    |                    | benötigt.          |
|                    |                    |                    |                    |
|                    |                    |                    | Hinweis: kann zu   |
|                    |                    |                    | SEHR viel          |
|                    |                    |                    | Textausgabe        |
|                    |                    |                    | führen.            |
+--------------------+--------------------+--------------------+--------------------+
| -h                 | --help             | Anzeige der Hilfe  | a) --help erzeugt  |
|                    |                    |                    | ein Dialogfenster  |
|                    |                    |                    |                    |
|                    |                    |                    | b) --help --no-gui |
|                    |                    |                    | gibt die Hilfe auf |
|                    |                    |                    | der Kommandozeile  |
|                    |                    |                    | aus                |
+--------------------+--------------------+--------------------+--------------------+

.. raw:: html

   </div>

Verarbeitungsreihenfolge, falls mehrere Prozessparameter angegeben
werden:

1.) Rechte setzen -> 2.) Paketieren -> 3.) Deinstallieren (falls
existent) -> 4.) Installieren

Wichtig:

Sollten die Depotfunktionen für den normalen GUI Betrieb aktiviert sein,
so werden sie bei Verwendung des Schalters --no-gui temporär
deaktiviert. Das

Ziel für sämtliche Aktionen ist dann der im Reiter "Allgemein"
(Einstellungen) angegebene Konfigserver.

Genauso werden in diesem Fall die ursprünglichen Befehle verwendet, die
in den Eingabefeldern des Reiters "opsi Verwaltungsbefehle"
(Einstellungen) hinterlegt wurden. Um diese Parameter trotz aktivierter
Depotfunktionen für den no-GUI Betrieb zu ändern, wie folgt vorgehen:

- die Option "Depotfunktionen aktivieren" ausschalten

- die Befehle in den Eingabefeldern entsprechend abändern

- Einstellungen speichern

- die Option "Depotfunktionen aktivieren" einschalten

- Einstellungen erneut speichern

Hinweis:

Wenn der Parameter --no-gui nicht angegeben ist, öffnet sich zuerst die
normale Fensteroberfläche und danach werden sämtliche Prozessschritte
abgearbeitet.

Beispiel 1:

Langform: opsiPackageBuilder.exe --path=w:\\opsi\\testpak --build=new
--no-gui --log=c:\\temp\\opb.log

Kurzform: opsiPackageBuilder.exe -p=w:\\opsi\\testpak -b=new -n
-l=c:\\temp\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im
Ordner w:\\opsi\\testpak, erzeugt bei Vorhandensein ein neues Paket
inkl. Zeitstempel und schreibt sämtliche Ausgaben in die Datei
C:\\temp\\opb.log.

Beispiel 2:

Langform: OPSIPackageBuilder.exe --path=testpak --build=interactive
--install --no-gui --log

Kurzform: OPSIPackageBuilder.exe -p=testpak -b=interactive -n -l

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im
Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte
Entwicklungsordner ist), fragt bei Vorhandensein des Pakets interaktiv
nach dem weiteren Vorgehen, installiert das Paket nach Erstellung auf
dem Server und schreibt sämtliche Ausgaben in die Datei %AppData%\\opsi
PackageBuilder\\opb-session.log.

Beispiel 3:

Gemischte Form: OPSIPackageBuilder.exe --path=testpak -b=rebuild
--install --uninstall --set-rights -q -l=.\\opb.log

Dieser Befehl startet das Programm ohne Oberfläche, lädt das Paket im
Ordner w:\\opsi\\testpak (sofern w:\\opsi der hinterlegte
Entwicklungsordner ist), setzt die Rechte auf dem Paketordner neu,
überschreibt beim Paketieren ein evtl. vorhandenes Paket gleicher
Version, deinstalliert die bestehende Version (falls vorhanden) und
installiert die gerade neu paketierte Fassung. Auf der Konsole wird
nichts ausgegeben, sämtliche Ausgaben gehen in die Log-Datei .\\opb.log.

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
Hilfeverfassungsumfeld <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Mehrere Konfigurationen
=======================

Mehrere Konfigurationen für opsi Package Builder anlegen

Normalerweise werden sämtliche Konfigurationsoptionen über den
Einstellungsdialog definiert. Diese Einstellungen finden sich in der
Datei "config.ini" in folgenden Pfaden:

-  Windows XP: C:\\Dokumente und
   Einstellungen\\<Benutzer>Anwendungsdaten\\opsiPackageBuilder
-  höhere Windows Versionen:
   C:\\Users\\<Benutzer>\\AppData\\Roaming\\opsiPackageBuilder

Um verschiedene Konfigurationen zu nutzen, können in dem jeweiligen Pfad
einfach mehrere, unterschiedlich benannte INI-Dateien hinterlegt werden.
Beim Start des Programms wird dann nach der zu verwendenden gefragt und
diese in "config.ini" umkopiert.

Beispielhafte Vorgehensweise:

-  beim allerersten Start nach der Installation erzwingt opsi Package
   Builder die Erstellung einer Konfiguration
-  opsi Package Builder schließen, dann die erstellte Datei config.ini
   (bspw.) im selben Ordner in die neue Datei produktiv.ini kopieren
-  beim jetzt folgenden Start fragt opsi Package Builder bereits, welche
   Konfiguration verwendet werden soll, dies einfach mit OK bestätigen
-  mit Hilfe des Einstellungedialogs die gewünschte alternative
   Konfiguration erfassen
-  opsi Package Builder schließen, dann die geänderte Datei config.ini
   (bspw.) im selben Ordner in eine weitere Datei testumgebung.ini
   kopieren

Jetzt liegen zwei getrennte Konfigurationen vor.

Bei jedem nachfolgenden Start wird opsi Package Builder jetzt erst
fragen, welche verwendet werden soll und kopiert diese dann entsprechend
die Datei config.ini um.

ACHTUNG- Wird opsi Package Builder über die Kommandozeile aufgerufen
wird der Auswahldialog ausgeblendet, wenn folgende
\ `Parameter <#Kommandozeilenparameter>`__\  verwendet werden:

Es wird in diesem Fall immer die zuletzt gewählte Konfiguration
verwendet. Wurde also beim letzten Start per GUI bspw. die
"produktiv.ini" ausgewählt, so wird danach beim Start über die
Kommandozeile genau diese Konfiguration verwendet.

.. raw:: html

   <div class="rvps2">

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

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `Funktionsreicher
EPub-Generator <http://www.helpndoc.com/de/epub-ebooks-erstellen>`__

Return Codes
============

Return Codes

opsi Package Builder gibt bei Ausführung über die Kommandozeile folgende
Fehlercodes zurück:

.. raw:: html

   <div class="rvps2">

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

.. raw:: html

   </div>

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis
Hilfeverfassungswerkzeug <http://www.helpndoc.com/de/hilfeentwicklungs-tool>`__

Systemvoraussetzungen
=====================

(Muss noch geschrieben werden...)

Mit dem Personal Edition von HelpNDoc erstellt: \ `iPhone-Dokumentation
einfach
erstellen <http://www.helpndoc.com/de/funktionen-tour/erstellen-sie-iphone-webseiten-und-dokumentationen>`__

Weitere Hilfe...
================

Weitere Hilfe, Anregungen und Tipps finden sich im eigenen Community
Bereich des opsi Forums für den opsi Package Builder.

Jegliche Form von sachlicher Kritik, Verbesserungsvorschlägen und
Anregung sind natürlich herzlich willkommen.

Zum Community Bereich geht es \ `hier
lang <https://forum.opsi.org/viewforum.php?f=22>`__\ !

Mit dem Personal Edition von HelpNDoc erstellt: \ `Gratis EBook und
Dokumentationsgenerator <http://www.helpndoc.com/de>`__

Copyright © 2013-2014 by Holger Pandel. All Rights Reserved.

.. |image0| image:: img/AppLogo.png
.. |image1| image:: img/ProgTop3D.png
.. |image2| image:: img/Start.jpg
.. |image3| image:: img/ReiterPaket.jpg
.. |image4| image:: img/SkriptEdit.png
.. |image5| image:: img/SkriptSuch.png
.. |image6| image:: img/btnChangelog.png
.. |image7| image:: img/btnSkriptbaum.png
.. |image8| image:: img/ReiterAbhngigkeit.jpg
.. |image9| image:: img/btnNew.png
.. |image10| image:: img/btnUpd.png
.. |image11| image:: img/btnDel.png
.. |image12| image:: img/ReiterProduktvariable.jpg
.. |image13| image:: img/btnNew.png
.. |image14| image:: img/btnUpd.png
.. |image15| image:: img/btnSkripteLesen.png
.. |image16| image:: img/btnDel.png
.. |image17| image:: img/Paketfunktionen.jpg
.. |image18| image:: img/btnPacken.png
.. |image19| image:: img/btnInstallieren.png
.. |image20| image:: img/InstSetup.jpg
.. |image21| image:: img/btnEntfernen.png
.. |image22| image:: img/btnOrdner.png
.. |image23| image:: img/btnSpeichern.png
.. |image24| image:: img/btnInstallieren.png
.. |image25| image:: img/btnEntfernen.png
.. |image26| image:: img/ChangelogEdTop.png
.. |image27| image:: img/ChLogSimple.png
.. |image28| image:: img/btnSchliessen.png
.. |image29| image:: img/ChLogExt-Standard.png
.. |image30| image:: img/btnAnlegen.png
.. |image31| image:: img/btnUebernehmen.png
.. |image32| image:: img/btnEntfernen2.png
.. |image33| image:: img/btnSchliessen.png
.. |image34| image:: img/ChLogEdTopStandard.png
.. |image35| image:: img/ChLogEdTopIndividuell.png
.. |image36| image:: img/ChLogSiToEx.png
.. |image37| image:: img/ChLogExToSi.png
.. |image38| image:: img/Skriptbaum.png
.. |image39| image:: img/Zeitplaner.png
.. |image40| image:: img/btnJobsanlegen2.png
.. |image41| image:: img/btnJobslschen.png
.. |image42| image:: img/btnJobsRefresh.png
.. |image43| image:: img/btnJobsallelschen.png
.. |image44| image:: img/btnJobsschliessen.png
.. |image45| image:: img/JobAnlegen.png
.. |image46| image:: img/btnJobsanlegen.png
.. |image47| image:: img/btnAbbruch.png
.. |image48| image:: img/Paketbndel.png
.. |image49| image:: img/Paketbndel-Frage.png
.. |image50| image:: img/DepotManager.jpg
.. |image51| image:: img/btnHoleRepo.png
.. |image52| image:: img/btnHoleRepotBlau.png
.. |image53| image:: img/btnSchließen.png
.. |image54| image:: img/btnVergleichen.png
.. |image55| image:: img/btnVergleichenGrün.png
.. |image56| image:: img/btnAktualisieren2.png
.. |image57| image:: img/btnVergleichsbericht.png
.. |image58| image:: img/btninstall.png
.. |image59| image:: img/btnDeinstallieren.png
.. |image60| image:: img/btnLöschen.png
.. |image61| image:: img/btnUpload.png
.. |image62| image:: img/btnDepotRegAufheben.png
.. |image63| image:: img/btnRechteSetzen2.png
.. |image64| image:: img/btnStartProdUpd2.png
.. |image65| image:: img/btnGeneriereMD5.png
.. |image66| image:: img/btnOnlineCheck2.png
.. |image67| image:: img/btnDepotNeustart2.png
.. |image68| image:: img/btnDepotShutdown.png
.. |image69| image:: img/btnPlinkLog.png
.. |image70| image:: img/DepotBeispielI.png
.. |image71| image:: img/DepotBeispielII.png
.. |image72| image:: img/ReportSelector.jpg
.. |image73| image:: img/DeployAgent.jpg
.. |image74| image:: img/MenuDatei.jpg
.. |image75| image:: img/MenuWerkzeuge.png
.. |image76| image:: img/MenuExtras.jpg
.. |image77| image:: img/MenuHelp.png
.. |image78| image:: img/Einst-Allgemein.jpg
.. |image79| image:: img/Einst-Programm.jpg
.. |image80| image:: img/Einst-opsi.png
.. |image81| image:: img/Einst-Nachrichten.jpg
.. |image82| image:: img/Einst-Update.jpg
.. |image83| image:: img/ScEdit.jpg
