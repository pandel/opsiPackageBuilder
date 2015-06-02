Skriptbaum
==========

|image38|

Im Skriptbaum werden die einzelnen möglichen Steuerskripte für opsi-winst dargestellt, inklusive der verwendeten Include-Dateien.

Mit einem Doppelklick kann ein vorhandenes Skript direkt aus der Baumdarstellung heraus mit dem in den \ `Einstellungen <#Programmeinstellungen>`__\  verknüpften Editor (\ `intern <#ToolSkriptEditor>`__\  oder extern) geöffnet werden.

opsi-winst bietet die Möglichkeit, immer wiederkehrende Funktionen in separate Dateien auszulagern, die dann per Include-Anweisung eingebunden werden. Diese Include-Dateien werden dabei in der Regel von mehreren Paketen referenziert.

Um zu verhindern, dass diese Skripte unbeabsichtigt oder aus Unwissenheit heraus fehlerhaft geändert werden und diese Änderung sich automatisch auf sämtliche Pakete auswirkt, die diese Skripte verwenden, können daher aus der Baumdarstellung heraus nur Dateien geöffnet werden, die sich im CLIENT\_DATA Ordner des aktuell geöffneten Pakets befinden.

Skripte, die nicht geändert werden können, werden in Klammern "( .. )" dargestellt. Zusätzlich erhält der Anwender beim Versuch ein solches Skript zu öffnen, eine Warnmeldung.

.. |image38| image:: ../img/Skriptbaum.png