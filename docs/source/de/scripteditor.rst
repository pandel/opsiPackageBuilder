.. index:: ! Tool "Skript Editor"

.. _scripteditor:

Tool "Skript Editor"
====================

Zusatztool "Skript Editor"

Bei der Installation kann wahlweise ein Skripteditor mitinstalliert werden. Dieser Editor kann, wenn entsprechend konfiguriert, direkt über den Skriptbaum oder über den Link im Startmenü aufgerufen werden.

|image83|

Wesentliche Merkmale:

   -  Farbige Syntaxhervorhebung
   -  "Falten" des Quellcodes (optional: kompakt, mit Kommentaren)
   -  Lexerdefinition anpassbar (dazu muss der Editor per Startmenü Eintrag aufgerufen werden)
   -  Autocomplete für Syntaxelemente und Variablen
   -  Frei definierbare und wiederverwendbare Codeblöcke ("Snippets")

Die Kernkomponente des Editors bildet das Modul `Scintilla <http://www.scintilla.org/>`__, welches auch in andere bekannten Editoren, wie bspw. `Notepad++ <http://notepad-plus-plus.org/>`__, verwendet wird. Die lexikalischen Elemente (Syntaxhervorhebung und Faltung) zur Darstellung der für opsi gültigen Scriptsprache sind allerdings komplett in AutoIt geschrieben, da Scintilla für opsi Skripte kein eigenes Darstellungsmodul mitliefert. Dadurch, dass AutoIt eine Interpretersprache ist, ist er damit langsamer als andere Editoren und eignet sich daher nur bedingt zur Bearbeitung sehr großer Skripte, vor allem bei eingeschalteter Quellcode Faltung. In den :ref:`Einstellungen <settings_program>` lässt sich jedoch vorgeben, ob der Editor mit diesen Funktionen überhaupt aufgerufen wird oder nicht, sofern der Aufruf direkt über den Skriptbaum erfolgt. Bei einem Aufruf über den Link im Startmenü sind Syntaxhervorhebung und Faltung generell beim Start ausgeschaltet und können über das Editormenü "Ansicht" aktiviert werden.

(Der Editor kann auch über die Kommandozeile aufgerufen werden. Weitere Informationen zu den möglichen Kommandozeilenparametern können mit der Option "--help" aufgerufen werden.)

.. |image83| image:: ../img/ScEdit.jpg