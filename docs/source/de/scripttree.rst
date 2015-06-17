.. index:: ! Skriptbaum

.. _scripttree:

Skriptbaum
==========

|image38|

Im Skriptbaum werden die im aktuell geöffneten Paket vorhandenen Steuerskripte für opsi-winst dargestellt, inklusive der verwendeten Include-Dateien.

Mit einem Doppelklick kann ein vorhandenes Skript direkt aus der Baumdarstellung heraus mit dem in den :ref:`Einstellungen <settings_program>` verknüpften :ref:`Editor <scripteditor>` (intern oder extern) geöffnet werden.

opsi-winst bietet die Möglichkeit, immer wiederkehrende Funktionen in separate Dateien auszulagern, die dann per Include-Anweisung eingebunden werden. Diese Include-Dateien können zusätzlich in einen Bibliotheksordner ausgelagert werden, der außerhalb des aktuell zu bearbeitenden Pakets liegt.

Um zu verhindern, dass solche globalen Skriptbibliotheken unbeabsichtigt oder aus Unwissenheit heraus (fehlerhaft) verändert werden und diese Änderung sich somit automatisch auf sämtliche Pakete auswirkt, die diese Skripte während der Verarbeitung einbinden, können aus der Baumdarstellung heraus nur Dateien geöffnet werden, die sich im CLIENT\_DATA Ordner des aktuell geöffneten Pakets befinden.

Skripte, die nicht geändert werden können, werden mit **(Extern)** markiert dargestellt. Zusätzlich erhält der Anwender beim Versuch ein solches Skript zu öffnen, eine Warnmeldung.

.. |image38| image:: ../img/Skriptbaum.png