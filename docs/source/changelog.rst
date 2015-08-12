=========
Changelog
=========

* :release:`8.0.3b <2015-08-12>`
* :support:`- backported` Upload function in main menu
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

