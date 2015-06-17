.. index:: ! Changelog Editor

.. _changelogeditor:

Changelog Editor
================

.. toctree::
   :maxdepth: 2

   chlog_simple
   chlog_extended
   chlog_conversionhints

|image26|

.. index:: ! Changelog Editor; Funktionalität

Beschreibung zur Changelog Editor Funktionalität
------------------------------------------------

Mit Hilfe des Changelog Editors können die in der Control Dateisektion [Changelog] hinterlegten Einträge gepflegt werden. Da der Aufbau dieser Sektion im Gegensatz zur sonstigen Struktur der Control Datei nicht fest vorgegeben ist, ist es grundsätzlich möglich, diese Sektion auf unterschiedliche Arten mit Informationen anzureichern.

**Variante 1:**

Unterhalb der Sektionsüberschrift wird unstrukturierter Freitext hinterlegt. Auch wenn damit eine Dokumentation natürlich grundsätzlich möglich ist, so kann diese Vorgehensweise mit einigen Einschränkungen verbunden sein. Ein Hauptargument gegen Fließtext dürfte sein, dass er die Übersichtlichkeit stark einschränkt und dadurch wichtige Informationen in der Fülle untergehen.

**Variante 2:**

Die Changelog Einträge werden nach einem festen Schema zeitlich absteigend sortiert in Textblöcken hinterlegt. Sie erhalten eine feststehende Überschrift (=Kopfzeile) und einen Abschlussvermerk (=Fußzeile), der den Eintrag näher beschreibt. Diese Eintragungsart wird auch bei der Paketanlage von opsi-newprod für den ersten Eintrag verwendet und sollte die bevorzugte Variante sein.

Um diesen beiden Paradigmen Rechnung zu tragen, enthält opsi PackageBuilder zwei verschiedene Arten von Editoren für die Changelog Einträge:
    - :ref:`changelogeditor_simple` (Variante 1)
    - :ref:`changelogeditor_extended` (Variante 2)

Beim Öffnen eines Pakets wird der gesamte Text innerhalb der [Changelog]-Sektion der Control Datei gemäß der Vorgaben in den :ref:`Programmeinstellungen <settings_program>` eingelesen.

**Hinweise zur Bestandspflege "alter" Pakete**

Soll ein bereits bestehendes Paket mit opsi PackageBuilder gepflegt werden, so ist es für die weiterführende Pflege der "alten" Changelog Einträge wichtig, ob in der Vergangenheit mit Variante 1 oder 2 gearbeitet wurde.

-  wurde ausschließlich mit Variante 1 gearbeitet:
    In den Einstellungen sollte der Haken bei "Erweiterten Changelog Editor verwenden" entfernt werden. Damit kann die Pflege auf gewohnte Weise fortgesetzt werden. Sollen die alten Einträge in die neue, strukturierte Form überführt werden, ist wie in der Hilfe unter :ref:`conversionhints` beschrieben, vorzugehen.

-  wurde ausschließlich mit Variante 2 gearbeitet:
    In den Einstellungen sollte der Haken bei "Erweiterten Changelog Editor verwenden" gesetzt werden. Weitere Informationen dazu unter :ref:`conversionhints`.

**Beispiel für strukturierte Changelog Einträge in der Control Datei zur Verwendung mit opsi PackageBuilder**

Einträge gem. opsi-newprod Vorgabe und Grundeinstellung in opsi PackageBuilder::

    [Changelog]

    acroread (11.0.01-2) stable; urgency=low

    * Test abgeschlossen

    * Paket in stable

    -- Holger Pandel <holger.pandel@....de>  Wed, 31 Jan 2013 11:43:01 +0000

    acroread (11.0.01-1) testing; urgency=low

    * Initial package

    -- Holger Pandel <holger.pandel@....de>  Wed, 30 Jan 2013 16:25:01 +0000

Die Textmarke "urgency=" kehrt bei jedem Changelog Eintrag wieder und kennzeichnet damit den Beginn eines neuen Textblocks. Sie wird in opsi PackageBuilder zur Blockerkennung verwendet.

.. |image26| image:: ../img/ChangelogEdTop.png