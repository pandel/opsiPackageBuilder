=========
Changelog
=========

* :release:`8.1.0 <2016-05-13>`
* :support:`-` Update to spur 0.3.17
* :release:`8.0.7b <2016-05-13>`
* :bug:`-` Error introduced in 8.0.5b regarding SSH processing, rendering depot manager unusable, corrected
* :release:`8.0.6b <2016-05-12>`
* :bug:`-` Error checking: false positives while fetching product list, corrected
* :support:`- backported` Online updater can be disabled again via command line
* :support:`- backported` Too many Qt translation files included, corrected
* :release:`8.0.5b <2016-05-11>`
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
* :release:`8.0.4b <2015-11-11>`
* :support:`- backported` Code is now compatible with PyQt 5.5
* :feature:`- backported` Show project logo, if exists under %ScriptPath% with name <project id>.(png|gif|jpg|jpeg), refresh with F6
* :bug:`-` No setup script set in package bundle ("meta" package)
* :bug:`-` Backend data should have been updated before opening changelog editor
* :support:`- backported` Sortable description column in scheduler/job creator/client list
* :release:`8.0.3b <2015-08-12>`
* :feature:`- backported` Upload function in main menu
* :bug:`3` Error in package upload
* :bug:`2` File not found -> /home/opsiproducts is /var/lib/opsi/workbench on SLES
* :bug:`-` Error in log output - class names refer to wrong package
* :release:`8.0.2b <2015-07-24>`
* :support:`- backported` Control file field ``licenseRequired`` can be empty, defaults to ``False`` then
* :bug:`-` Client agent deploy not working
* :release:`8.0.1b <2015-07-16>`
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
* :release:`8.0.0b <2015-06-26>`
* :feature:`-` Changed from AutoIt as main development environment to Python 3 / PyQt5
  and ported the complete application.
* :feature:`-` Direct import function for \*.opsi files

