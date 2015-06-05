FORMS += ..\oPB\ui\bundle.ui
FORMS += ..\oPB\ui\changelogeditorextended.ui
FORMS += ..\oPB\ui\changelogeditorsimple.ui
FORMS += ..\oPB\ui\deployagent.ui
FORMS += ..\oPB\ui\depotmanager.ui
FORMS += ..\oPB\ui\jobcreator.ui
FORMS += ..\oPB\ui\joblist.ui
FORMS += ..\oPB\ui\log.ui
FORMS += ..\oPB\ui\mainwindow.ui
FORMS += ..\oPB\ui\quickuninstall.ui
FORMS += ..\oPB\ui\scripttree.ui
FORMS += ..\oPB\ui\settings.ui
FORMS += ..\oPB\ui\startup.ui

SOURCES = ..\opsiPackageBuilder.py

SOURCES += ..\oPB\__init__.py
SOURCES += ..\oPB\runner.py

SOURCES += ..\oPB\controller\__init__.py
SOURCES += ..\oPB\controller\base.py
SOURCES += ..\oPB\controller\console.py
SOURCES += ..\oPB\controller\main.py
SOURCES += ..\oPB\controller\settings.py

SOURCES += ..\oPB\controller\components\__init__.py
SOURCES += ..\oPB\controller\components\bundle.py
SOURCES += ..\oPB\controller\components\changelog.py
SOURCES += ..\oPB\controller\components\deployagent.py
SOURCES += ..\oPB\controller\components\depotmanager.py
SOURCES += ..\oPB\controller\components\quickuninstall.py
SOURCES += ..\oPB\controller\components\scheduler.py

SOURCES += ..\oPB\core\__init__.py
SOURCES += ..\oPB\core\confighandler.py
SOURCES += ..\oPB\core\datadefinition.py
SOURCES += ..\oPB\core\logging.py
SOURCES += ..\oPB\core\mapdrive.py
SOURCES += ..\oPB\core\processing.py
SOURCES += ..\oPB\core\scriptscanner.py
SOURCES += ..\oPB\core\tools.py

SOURCES += ..\oPB\gui\__init__.py
SOURCES += ..\oPB\gui\bundle.py
SOURCES += ..\oPB\gui\changelog.py
SOURCES += ..\oPB\gui\deployagent.py
SOURCES += ..\oPB\gui\depotmanager.py
SOURCES += ..\oPB\gui\helpviewer.py
SOURCES += ..\oPB\gui\logging.py
SOURCES += ..\oPB\gui\mainwindow.py
SOURCES += ..\oPB\gui\quickuninstall.py
SOURCES += ..\oPB\gui\scheduler.py
SOURCES += ..\oPB\gui\scripttree.py
SOURCES += ..\oPB\gui\settings.py
SOURCES += ..\oPB\gui\startup.py
SOURCES += ..\oPB\gui\utilities.py

SOURCES += ..\oPB\ui\__init__.py
SOURCES += ..\oPB\ui\ui.py

TRANSLATIONS = opsiPackageBuilder_de.ts opsiPackageBuilder_en.ts
