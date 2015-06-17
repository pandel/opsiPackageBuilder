.. index:: ! Changelog Editor; Konvertierungshinweise

.. _conversionhints:

Konvertierungshinweise
======================

**Konvertierung von einfacher in erweiterte Darstellung und Funktionalität**

Alte Changelog Einträge, die nicht einer festen strukturierten Form entsprechen, können in die strukturierte Form überführt werden, ohne dass die Inhalte verloren gehen.

Dazu ist folgende Reihenfolge in der Vorgehensweise einzuhalten:

#. opsi PackageBuilder starten
#. unter "Einstellungen" - "Programmeinstellungen" den Haken bei "Erweiterten Changelog Editor verwenden" entfernen
#. das Paket mit den zu konvertierenden Changelog Einträgen öffnen
#. unter "Einstellungen" - "Programmeinstellungen" den Haken bei "Erweiterten Changelog Editor verwenden" setzen es erfolgt folgende Meldung:
#. das Paket speichern

Jetzt liegt das Changelog inkl. der alten Einträge im neuen Format vor und kann mit dem erweiterten Editor bearbeitet werden.

Beispiel für umgestellte Einträge

Einträge vor der Konvertierung::

    [Changelog]

    Das ist freier Changelog Text ohne besonderen Marker.

    Er hörte leise Schritte hinter sich.

    Das bedeutete nichts Gutes.

    Wer würde ihm schon folgen, spät in der Nacht und dazu noch in dieser engen Gasse mitten im übel beleumundeten Hafenviertel?

    Gerade jetzt.

Einträge nach der Konvertierung::

    [Changelog]
    Umgewandelt (2.5-1.corr185412corr) stable; urgency=low

    Umgewandelte Freitexteinträge:

         --------------------------------------------------
          > Das ist freier Changelog Text ohne besonderen Marker.
          >
          > Er hörte leise Schritte hinter sich.
          >
          > Das bedeutete nichts Gutes.
          >
          > Wer würde ihm schon folgen, spät in der Nacht und dazu noch in dieser engen Gasse mitten im übel beleumundeten Hafenviertel?
          >
          > Gerade jetzt.
         --------------------------------------------------


     -- Holger Pandel <holger.pandel@googlemail.de>  Tue, 16 Jun 2015 16:56:48 +0000

Konvertierung von erweiterter in einfache Darstellung und Funktionalität

In diese Richtung findet keine Konvertierung statt. Es reicht, unter "Einstellungen" - "Programmeinstellungen" den Haken bei "Erweiterten Changelog Editor verwenden" zu entfernen.

