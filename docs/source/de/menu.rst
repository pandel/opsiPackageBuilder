.. index:: ! Menü

Menü
====

Genauere Erläuterungen zum Menü erfolgen in den einzelnen Kapiteln, falls notwendig.

.. index:: ! Menü; Datei

Datei
-----

|image74|

.. index:: ! Menü; Werkzeuge

Werkzeuge
---------

|image75|

   -  Skripte neu scannen
      Wenn Änderungen an den Installationsskripten durchgeführt und insbesondere weitere Include- oder Sub-Anweisungen eingebaut wurden, so kann die Paketstruktur hiermit für eine korrekte Darstellung im Skriptbaum neu eingelesen werden.
   -  Paketrechte setzen
      Die Linux-seitig bestehenden Verzeichnisrechte auf den opsi Standard korrigieren. Dazu ist ggf. in den :ref:`allgemeinen Einstellungen <settings_general>` die Hinterlegung des root Kennworts des opsi Servers notwendig.
   -  Start opsi-winst
      Starten der opsi-winst Entwicklungsoberfläche zum Starten/ Überwachen und Debuggen von opsi-winst Skripten. Der Menüpunkt setzte eine bestehende opsi-winst-client Installation voraus, bzw sucht die winst32.exe in folgendem Pfad:
      %ProgramFiles%\\opsi.org\\opsi-client-agent\\opsi-winst\\winst32.exe
   -  Skripteditor
      Startet den in den Einstellungen hinterlegten Editor.

.. index:: ! Menü; Extras

Extras
------

|image76|

   -  Zeige Logbuch

|image77|

   -  Nach Updates suchen
      Manuellen Aktualisierung der installierten Version von opsi PackageBuilder durchführen, falls eine neuere Version verfügbar ist.
   -  Zeige Changelog
      Das opsi PackageBuilder Versions-Changelog anzeigen (im Gegensatz zum Paket-Changelog!)

.. |image74| image:: ../img/MenuDatei.jpg
.. |image75| image:: ../img/MenuWerkzeuge.png
.. |image76| image:: ../img/MenuExtras.jpg
.. |image77| image:: ../img/MenuHelp.png