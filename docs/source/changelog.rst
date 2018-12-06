=========
Changelog
=========

* :release:`8.4.1 <2018-12-06>`
* :bug:`-` Qt translation not loading correctly
* :bug:`-` Documenting modules creates errors, typos corrected
* :release:`8.4.0 <2018-12-05>`
* :feature:`- backported` Packaging, installation and uninstallation can be canceled finally
* :support:`-` Product dependencies: requirementType not mandatory, action request can also be "uninstall"
* :release:`8.3.3 <2018-11-08>`
* :bug:`-` Bug in path handling when development folder vlue is only a drive letter under windows
* :bug:`-` Bug in pre-8.2.5 config-new.ini conversion
* :bug:`-` Bug in client list evaluation of scheduler window
* :release:`8.3.2 <2018-08-02>`
* :bug:`-` Clients not assigned to any individual clientgroup where not shown in scheduler
* :feature:`- backported` Added NO_REPO selection in depot query dialog to prevent package to be copied to repository folder (only depot mode)
* :release:`8.3.1 <2018-06-08>`
* :bug:`-` Unlocking of locked product did not work anymore
* :release:`8.3.0 <2018-04-24>`
* :bug:`-` Delete opsi client agent temporary deploy script for security reason
* :bug:`-` opsi client agent deploy: Smbclient 4.3.11 in opsiVM doesn't like escaped backslashes in DOMAIN\username anymore, removed
* :bug:`-` Depot Manager: running opsi-package(product)-updater not always recognized when initiated twice on the same repository server
* :support:`-` opsi 4.1 compatibility: set workbench folder / opsi Server Version pre 4.1 or newer
* :feature:`- backported` Report Generator: Get current depot/repo content on single server
* :release:`8.2.5 <2018-04-13>`
* :support:`-` Pyinstaller 3.3.1 now working with Python 3.6 - spec file modified
* :bug:`-` Nasty warnings about helpviewer being instantiated over and over again
* :bug:`-` Incorrect program version information in global excepthook
* :bug:`-` Translator files for Qt Base, WebEngine, etc. not loaded
* :bug:`-` opsi-makeproductfile "Permission denied" error not detected
* :release:`8.2.4 <2018-03-01>`
* :bug:`8` Update notifier not working when used without proxy server
* :bug:`-` Added missing imports re+os in tools.py
* :release:`8.2.3 <2018-02-22>`
* :support:`-` Visual C++ 2010 x64 Redistributable included
* :bug:`-` ScriptTree not updated when opened again
* :bug:`-` "ALL" depot option removed before opening locked product dialog
* :release:`8.2.2 <2017-10-25>`
* :bug:`-` Application icon now correct in every window
* :bug:`-` Create process running marker ONLY when building a package, otherwise not necessary
* :release:`8.2.1 <2017-09-29>`
* :bug:`-` Some pyqtSlot declarations corrected
* :bug:`-` Change from pycrypto (depricated) to the more recent, drop-in compatible pycryptodome
* :bug:`-` QtWebKit not working anymore in Qt 5.9 - transition to QtWebEngine
* :bug:`6` Change use of md5deep to more generally available md5sum in depot manager
* :support:`- backported` Porting to Python 3.6 and Qt 5.9
* :release:`8.2.0 <2017-09-15>`
* :support:`7` opsi client groups in job scheduler
* :support:`-` Make use of virtualenv, see README for details
* :release:`8.1.7 <2017-08-03>`
* :bug:`-` Further comments in Debug mode
* :bug:`-` Sometimes \*.opsi files could not be found right after creation - VERY OLD nasty problem with DirectoryCacheLifetime - hopefully resolved by creating a process running marker
* :bug:`-` Configuration was saved erroneously when program was called via command line and no gui
* :bug:`-` Command line parameter --no-netdrv had no effect
* :support:`- backported` Additional command line option: --dev-dir - overwrite development folder from config
* :release:`8.1.6 <2017-06-13>`
* :bug:`-` Unsaved changes haven't been checked while loading a new project
* :support:`- backported` Accept additional changelog entry status "experimental"
* :release:`8.1.5 <2017-03-02>`
* :support:`-` Change download/ update check to Amazon AWS S3
* :support:`-` Update to spur 0.3.20
* :bug:`-` Error in depot manager when generating MD5 only for the right side of the dialog
* :release:`8.1.4 <2017-02-24>`
* :feature:`- backported` Qt About dialog
* :support:`- backported` More messages for the status bar
* :bug:`-` Internal changes regarding message signaling
* :bug:`-` Multiline text in Advice field wasn't handled correctly during load of control file
* :bug:`-` Ctrl-S didn't update fields in backend before saving
* :bug:`-` Product property input fields not reset properly when loading a new product
* :release:`8.1.3 <2016-10-19>`
* :bug:`-` Some file names produce false positive error messages (i.e. Windows 10 setup: setuperror.exe.mui)
* :release:`8.1.2 <2016-09-06>`
* :support:`- backported` Update to spur 0.3.19
* :bug:`-` Individual SSH port wasn't used
* :bug:`-` Bug in depot manager
* :release:`8.1.1 <2016-08-15>`
* :bug:`-` Internal changes and fixes
* :bug:`-` Long execution time for fetching products and clients from server
* :feature:`- backported` Unlock products from start window
* :release:`8.1.0 <2016-05-13>`
* :support:`-` Update to spur 0.3.17
* :release:`8.0.7 <2016-05-13>`
* :bug:`-` Error introduced in 8.0.5b regarding SSH processing, rendering depot manager unusable, corrected
* :release:`8.0.6 <2016-05-12>`
* :bug:`-` Error checking: false positives while fetching product list, corrected
* :support:`- backported` Online updater can be disabled again via command line
* :support:`- backported` Too many Qt translation files included, corrected
* :release:`8.0.5 <2016-05-11>`
* :feature:`- backported` New dialog "Locked products" - allows to lists and unlock opsi products on depots
* :feature:`- backported` Enable program update on startup or via Help menu again, see Settings
* :support:`- backported` Update to spur 0.3.16
* :bug:`-` Error message handling from subprocess changed to avoid misinterpretation
* :support:`- backported` Update to spur 0.3.15
* :feature:`- backported` Helper function in Tools menu: show MSI ProductCode for MSI file
* :support:`- backported` Update to Python 3.4.4rc1
* :bug:`-` Better check for existing \*.opsi file on project load
* :bug:`-` Erroneous tooltips removed
* :feature:`- backported` Mac OS X DMG install image
* :support:`- backported` Better table handling, edit properties/dependencies via F2 or button
* :bug:`-` Errors in package bundle creation
* :bug:`5` Sometimes old project data was not correctly reset when loading a new one
* :bug:`4` After package file creation the ui wasn't updated correctly sometimes
* :bug:`-` Exception in depot manager when generating repository reports
* :bug:`-` Exception in depot manager, when SSH connection error occurred while fetching depot server list
* :release:`8.0.4 <2015-11-11>`
* :support:`- backported` Code is now compatible with PyQt 5.5
* :feature:`- backported` Show project logo, if exists under %ScriptPath% with name <project id>.(png|gif|jpg|jpeg), refresh with F6
* :bug:`-` No setup script set in package bundle ("meta" package)
* :bug:`-` Backend data should have been updated before opening changelog editor
* :support:`- backported` Sortable description column in scheduler/job creator/client list
* :release:`8.0.3 <2015-08-12>`
* :feature:`- backported` Upload function in main menu
* :bug:`3` Error in package upload
* :bug:`2` File not found -> /home/opsiproducts is /var/lib/opsi/workbench on SLES
* :bug:`-` Error in log output - class names refer to wrong package
* :release:`8.0.2 <2015-07-24>`
* :support:`- backported` Control file field ``licenseRequired`` can be empty, defaults to ``False`` then
* :bug:`-` Client agent deploy not working
* :release:`8.0.1 <2015-07-16>`
* :bug:`-` Different problems under OS X resolved
* :support:`- backported` New program icon ;-)
* :bug:`-` Parameter --quiet had no effect, corrected
* :bug:`-` Return code corrections
* :bug:`-` Refreshing DepotManager content did not finish correctly
* :bug:`-` Settings parameter: "always reload products and clients in scheduler" had no effect
* :bug:`-` Product dependency: required product id combobox was empty
* :bug:`-` Corrected "jumping" of main ui to tab 0 when saving
* :bug:`-` Call to ScriptEditor incorrect from menu, return code handling from internal editor changed
* :bug:`-` Set package rights not working correctly
* :release:`8.0.0 <2015-06-26>`
* :feature:`-` Changed from AutoIt as main development environment to Python 3 / PyQt5
  and ported the complete application.
* :feature:`-` Direct import function for \*.opsi files

