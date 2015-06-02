Tool "Skript Editor"
====================

Zusatztool "Skript Editor"

Ab opsi Package Builder Version 5.3 wird ein kleiner Skripteditor mitinstalliert. Dieser Skripteditor kann, wenn entsprechend konfiguriert, direkt über den Skriptbaum oder über den Link im Startmenü aufgerufen werden.

|image83|

Wesentliche Merkmale:

   -  Farbige Syntaxhervorhebung
   -  "Falten" des Quellcodes (optional: kompakt, mit Kommentaren)
   -  Lexerdefinition anpassbar (dazu muss der Editor per Startmenü Eintrag aufgerufen werden)
   -  Autocomplete für Syntaxelemente und Variablen
   -  Frei definierbare und wiederverwendbare Codeblöcke ("Snippets")

Die Kernkomponente des Editors bildet das Modul "\ `Scintilla <http://www.scintilla.org/>`__\ ", welches auch in bekannten Editoren, wie bspw. \ `Notepad++ <http://notepad-plus-plus.org/>`__\ , verwendet wird. Die lexikalischen Elemente (Syntaxhervorhebung und Faltung) sind allerdings komplett in AutoIt geschrieben ist, da Scintilla für opsi Skripte kein eigenes Modul zur Darstellung mitliefert. Dadurch, dass AutoIt eine Interpretersprache ist, ist er damit langsamer als andere Editoren und eignet sich daher nur bedingt zur Bearbeitung sehr großer Skripte, vor allem bei eingeschalteter Syntaxhervorhebung und/oder Faltung. In den \ `Einstellungen <#Programmeinstellungen>`__\  von opsi Package Builder lässt sich jedoch vorgeben, ob der Editor mit diesen Funktionen überhaupt aufgerufen wird oder nicht, sofern der Aufruf direkt über den Skriptbaum erfolgt. Bei einem Aufruf über den Link im Startmenü sind Syntaxhervorhebung und Faltung generell beim Start ausgeschaltet und können über das Editormenü "Ansicht" aktiviert werden.

Alle weiteren Menüfunktionen entsprechen denen gängiger Editoren und werden nicht weiter beschrieben.

(Der Editor kann auch über die Kommandozeile aufgerufen werden. Weitere Informationen zu den möglichen Kommandozeilenparametern können mit der Option "--help" aufgerufen werden.)

.. |image83| image:: ../img/ScEdit.jpg