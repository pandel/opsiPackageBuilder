Reiter "Abhängigkeit"
=====================

|image8|

Auf diesem Reiter können Paketabhängigkeiten (product dependencies)
definiert und bearbeitet werden.

Der obere Teil des Fensters beinhaltet eine tabellarische Aufstellung
der derzeit im Paket definierten Abhängigkeiten. Sollte in der Liste nur
ein einziger Eintrag in der Spalte "Aktion" mit dem Inhalt "empty"
angezeigt werden, so weißt das daraufhin, dass noch keinerlei
Abhängigkeiten definiert worden sind.

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
|                         |                         | *Werden "setup" oder    |
|                         |                         | "update" gewählt, wird  |
|                         |                         | der "Notw.              |
|                         |                         | Installationsstatus"    |
|                         |                         | autom. auf "none"       |
|                         |                         | gesetzt.*               |
+-------------------------+-------------------------+-------------------------+
| Notw.                   | Installationsstatus,    | Mögliche Werte: none /  |
| Installationsstatus     | den das abhängige       | installed               |
|                         | Produkt besitzen muss   |                         |
|                         |                         | *Wird "installed"       |
|                         |                         | gewählt, wird die       |
|                         |                         | "Geford. Aktion" autom. |
|                         |                         | auf "none" gesetzt.*    |
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
| |image10|               | Eine bestehende         | *Wenn der Reiter        |
|                         | Abhängigkeit ändern und | gewechselt wird, ohne   |
|                         | aktualisieren.          | die Änderung zu         |
|                         |                         | übernehmen, gehen diese |
|                         | Um eine bestehende      | i d. R. verloren.*      |
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
| |image11|               | Eine bestehende         | *Solange das Paket nicht|
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
|                         |    anklicken            | zurückgesichert werden.*|
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

.. |image8| image:: ../img/ReiterAbhngigkeit.jpg
.. |image9| image:: ../img/btnNew.png
.. |image10| image:: ../img/btnUpd.png
.. |image11| image:: ../img/btnDel.png
