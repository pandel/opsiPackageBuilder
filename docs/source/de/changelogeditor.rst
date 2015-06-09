.. index:: ! Changelog Editor

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

Mit Hilfe des Changelog Editors können die in der Control Dateisektion [Changelog] hinterlegten Einträge gepflegt werden. Da der Aufbau dieser Sektion, im Gegensatz zur sonstigen Struktur der Control Datei, nicht fest vorgegeben ist, ist es grundsätzlich möglich, diese Sektion unterschiedlich mit Informationen anzureichern.

**Variante 1:**

Unterhalb der Sektionsüberschrift wird unstrukturierter Freitext hinterlegt. Auch wenn damit eine Dokumentation natürlich grundsätzlich möglich ist, so kann diese Art der Dokumentation mit einigen Einschränkungen verbunden sein. Neben der Tatsache, daß Fließtext nicht zwingend die Lesbarkeit erhöht, so dokumentiert er ggf. auch nicht notwendige Informationen, um die zu dokumentierenden Änderungen zeitlich, bzgl. ihrer Wichtigkeit oder auch bezogen auf den Autor der Änderung einzugliedern.

**Variante 2:**

Die Changelog Einträge werden nach einem festen Schema zeitlich absteigend sortiert in Textblöcken hinterlegt. Sie erhalten eine feststehende Überschrift (=Kopfzeile) und einen Abschlussvermerk (=Fußzeile), der den Eintrag näher beschreibt. Diese Eintragungsart wird auch bei der Paketanlage von opsi-newprod für den ersten Eintrag verwendet.

Um diesen beiden Paradigmen Rechnung zu tragen, enthält opsi Package Builder zwei verschiedene Arten von Editoren für die Changelog Einträge, den :ref:`changelogeditor_simple` (Variante 1) und den :ref:`changelogeditor_extended` (Variante 2) Editor.

Beim Öffnen eines Pakets wird der gesamte Text innerhalb der [Changelog]-Sektion der Control Datei gemäß der in den `Einstellungen gewählten Editorvariante <#Programmeinstellungen>`__ eingelesen. Für den Betrieb des erweiterten Editors spielt dabei zusätzlich der Eintrag im `Feld "Blockerkennung" <#Programmeinstellungen>`__ eine entscheidende Rolle. Findet opsi Package Builder beim Einlesen eine Textzeile, die den dort hinterlegten Eintrag beinhaltet, wird der nachfolgende Text als neuer Changelog Textblock erkannt.

*Achtung:*

Die Changelog Einträge der Control Datei werden nur einmalig beim Öffnen
des Pakets geladen und interpretiert. Sollten in der Zwischenzeit bei
geöffnetem Paket Änderungen an den Einstellungen zur Verwendung des
Editors oder der Blockerkennung durchgeführt werden, so muss das
geöffnete Paket geschlossen und wieder geöffnet werden.

**Hinweise zur Bestandspflege "alter" Pakete**

Soll ein bereits bestehendes Paket mit opsi Package Builder gepflegt werden, so ist es für die weiterführende Pflege der "alten" Changelog Einträge wichtig, ob in der Vergangenheit mit Variante 1 oder 2 gearbeitet wurde.

-  wurde ausschließlich mit Variante 1 gearbeitet:
    In den Einstellungen sollte der Haken bei "Erweiterten Changelog Editor verwenden" entfernt werden. Damit kann die Pflege auf gewohnte Weise fortgesetzt werden. Sollen die alten Einträge in die neue, strukturierte Form überführt werden, ist wie in der Hilfe unter :ref:`conversionhints` beschrieben vorzugehen.

-  wurde ausschließlich mit Variante 2 gearbeitet:
    In den Einstellungen sollte der Haken bei "Erweiterten Changelog Editor verwenden" gesetzt werden. Zusätzlich sollte überprüft werden, ob die verwendete Überschrift (=Kopfzeile) den in den `Einstellungen im Feld "Blockerkennung" <#Programmeinstellungen>`__ hinterlegten Text beinhaltet. Wurde eine eigene, wiederkehrende Textmarkierung verwendet, ist der Wert in den Einstellungen entsprechend anzupassen. Weitere Informationen dazu `hier <#Konvertierungshinweise>`__.

**Beispiele für strukturierte Changelog Einträge in der Control Datei zur Verwendung mit opsi Package Builder**

1. Einträge gem. opsi-newprod Vorgabe und Grundeinstellung in opsi Package Builder::

    [Changelog]

    acroread (11.0.01-2) stable; urgency=low

    * Test abgeschlossen

    * Paket in stable

    -- Holger Pandel <holger.pandel@....de>  Wed, 31 Jan 2013 11:43:01 +0000

    acroread (11.0.01-1) testing; urgency=low

    * Initial package

    -- Holger Pandel <holger.pandel@....de>  Wed, 30 Jan 2013 16:25:01 +0000

Die grün markierte Textstelle kehrt bei jedem Changelog Eintrag wieder und kennzeichnet damit den Beginn eines neuen Textblocks. Sie wird gem. der Standardeinstellung in opsi Package Builder zur Blockerkennung verwendet.

2. Einträge mit selbstgewählter, wiederkehrender Struktur::

    [Changelog]

    Lfd. Nr. der Änderung: 2 am  31 Jan 2013 11:43:01

    Paketversion: 11.0.01-2

    Status: stable

    urgency=low

      * Test abgeschlossen

      * Paket in stable

    -- Holger Pandel <holger.pandel@....de>

    Lfd. Nr. der Änderung: 1 am 15 Jan 2013 13:28:15

    Paketversion: 11.0.01-1

    Status: testing

    urgency=low

      * Initial package

    -- Holger Pandel <holger.pandel@....de>

Die grün markierte Textstelle kehrt bei jedem Changelog Eintrag wieder und kennzeichnet damit den Beginn eines neuen Textblocks. Sie kann somit ebenfalls zur Blockerkennung verwendet werden und muss in den `Einstellungen im Feld "Blockerkennung" <#Programmeinstellungen>`__ hinterlegt werden. Es ist jedoch hierbei darauf zu achten, dass dieser Begriff nicht zusätzlich im Langtext des Changelog Eintrags auftaucht, um Fehler bei der Blockerkennung zu vermeiden.

Vorteile bei der Nutzung des Standardverhaltens

Wird das Standardverhalten von opsi Package Builder beibehalten, können mit den Funktionen und zusätzlichen Auswahlfeldern im erweiterten Editor komfortabel und schnell neue Einträge angelegt werden, die vollständig kompatibel zur Blockerkennung von opsi Package Builder sind. Falls doch eine individuelle Blockgestaltung genutzt werden soll ist sicherzustellen, dass die Blockmarkierung, die im individuellen Eingabefeld eingegeben wird eindeutig ist.

.. |image26| image:: ../img/ChangelogEdTop.png