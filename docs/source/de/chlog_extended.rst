.. index:: ! Changelog Editor; Erweiterter Editor

.. _changelogeditor_extended:

Erweiterter Editor
==================

|image29|

Ist in den :ref:`settings` die Nutzung des erweiterten Changelog Editors aktiviert, erscheint beim Klick auf die Schaltfläche "Changelog" im :ref:`tabpacket` das erweiterte Editorfenster. Damit können die einzelnen Changelog Einträge komfortabel verwaltet werden.

+-------------------------+-------------------------+-------------------------+
| Feld / Funktion         | Beschreibung            | Hinweise                |
+=========================+=========================+=========================+
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
| Feld 3                  | Dringlichkeit der       | Mögliche Werte:         |
|                         | Änderung                | urgency=low /           |
|                         |                         | urgency=middle /        |
|                         |                         | urgency=high            |
|                         |                         |                         |
+-------------------------+-------------------------+-------------------------+
| Feld 4                  | (weggefallen)           |                         |
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

.. |image29| image:: ../img/ChLogExt-Standard.png
.. |image30| image:: ../img/btnAnlegen.png
.. |image31| image:: ../img/btnUebernehmen.png
.. |image32| image:: ../img/btnEntfernen2.png
.. |image33| image:: ../img/btnSchliessen.png
