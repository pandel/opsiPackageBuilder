#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module is part of the opsi PackageBuilder
see: https://forum.opsi.org/viewforum.php?f=22

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Holger Pandel'
__copyright__ = "Copyright 2013-2015, Holger Pandel"
__license__ = "MIT"
__maintainer__ = "Holger Pandel"
__email__ = "holger.pandel@googlemail.com"
__status__ = "Production"


from copy import copy, deepcopy
import shutil
import json
import re
import platform
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject
import oPB
from oPB.core.tools import Helper, LogMixin
from oPB.core.confighandler import ConfigHandler

translate = QtCore.QCoreApplication.translate

def changelog_footer() ->str:
    """
    Generate footer for standard changelog entries.

    :return: footer sring
    """
    return "\n\n" + " -- " + ConfigHandler.cfg.packagemaintainer + " <" + ConfigHandler.cfg.mailaddress + ">  " + Helper.timestamp_changelog() + "\n"


class ChangelogEntry(object):
    """Holds a single changelog entry in extended mode"""
    def __init__(self, productId):
        """
        Constructor of ChangelogEntry

        :param productId: product id of entry
        """
        self._version = ""
        self._status = ""
        self._urgency = ""
        self._text = ""
        self._individual = "" # if an individual block marker is used, then this will contain the whole line
        self._productId = productId

    @property
    def productId(self):
        return self._productId

    @productId.setter
    def productId(self, value):
        # create new exception handling vor changelog
        #if (value != "True") and (value != "False"):
        #    raise ValueError("describe exception")
        self._productId = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if str(value).strip() not in oPB.CHLOG_STATI:
            raise ValueError(translate("ChangelogEntry", "Status must be testing or stable: ") + str(value).strip())
        self._status = value

    @property
    def urgency(self):
        return self._urgency

    @urgency.setter
    def urgency(self, value):
        if ConfigHandler.cfg.chlog_block_marker.lower() not in str(value).strip().lower():
            raise ValueError(translate("ChangelogEntry", "Urgency doesn't contain block marker for extended mode: ") + str(value).strip()
                             + " (Marker: " + ConfigHandler.cfg.chlog_block_marker + ")")
        self._urgency = value

    @property
    def individual(self):
        return self._individual

    @individual.setter
    def individual(self, value):
        self._individual = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

class ProductProperty(object):
    """Holds a single product property"""
    def __init__(self, name = "new"):
        """
        Constructor of ProductProperty

        :param name: property name
        """
        self._name = name           # name of the property
        self._type = ""           # type of value: unicode / boolean
        self._multivalue = ""     # is multivalue str "True" / "False"
        self._editable = ""       # is editable in configed "True" / "False"
        self._description = ""    # tool tip
        self._values = ""         # multi-value list
        self._default = ""        # default value(s)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if str(value).strip() == "":
            raise ValueError(translate("ProductProperty", "Name cannot be an empty string."))
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if str(value).strip() not in ["unicode", "bool"]:
            raise ValueError(translate("ProductProperty", "Type must be unicode or bool: ") + str(value).strip())
        self._type = str(value).strip()

    @property
    def multivalue(self):
        return self._multivalue

    @multivalue.setter
    def multivalue(self, value):
        if self.type == 'bool':
            self._multivalue = ""
            return
        if (str(value).strip() not in ["True", "False"]):
            raise ValueError(translate("ProductProperty", "Multivalue must be True or False: ") + str(value).strip())
        self._multivalue = str(value).strip()

    @property
    def editable(self):
        return self._editable

    @editable.setter
    def editable(self, value):
        if self.type == 'bool':
            self._editable = ""
            return
        if (str(value).strip() not in ["True", "False"]) and self.type != 'bool':
            raise ValueError(translate("ProductProperty", "Editable must be True or False: ") + str(value).strip())
        self._editable = str(value).strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        if self.type == 'bool':
            self._values = ""
            return
        self._values = value

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if self.type == 'bool' and str(value).strip() == "":
            self._default = "False"
            return
        if self.type == 'bool' and (str(value).strip() not in ["True", "False"]):
            raise ValueError(translate("ProductProperty", "Default must be True or False, if type=bool: ") + str(value).strip())
        self._default = value

class ProductDependency(object):
    """ProductDependency class: holds a single product dependency"""
    def __init__(self):
        self._dependencyForAction = ""
        self._requiredProductId = ""
        self._requiredAction = ""
        self._requiredInstallationStatus = ""
        self._requirementType = ""

    @property
    def dependencyForAction(self):
        return self._dependencyForAction

    @dependencyForAction.setter
    def dependencyForAction(self, value):
        # create new exception handling vor depdencies
        if str(value).strip() not in ["setup", "update", "uninstall"]:
            raise ValueError(translate("ProductDependency", "Incorrect value for dependencyForAction: " + str(value).strip()))
        self._dependencyForAction = str(value).strip()

    @property
    def requiredProductId(self):
        return self._requiredProductId

    @requiredProductId.setter
    def requiredProductId(self, value):
        # create new exception handling vor depdencies
        if str(value).strip() == "":
            raise ValueError(translate("ProductDependency", "requiredProductId cannot be empty"))
        self._requiredProductId = str(value).strip()

    @property
    def requiredAction(self):
        return self._requiredAction

    @requiredAction.setter
    def requiredAction(self, value):
        # create new exception handling vor depdencies
        if not str(value).strip() in ["", "setup", "uninstall", "update", "custom", "once"]:
            raise ValueError(translate("ProductDependency", "Incorrect value for requiredAction: " + str(value).strip()))
        self._requiredAction = str(value).strip()

    @property
    def requiredInstallationStatus(self):
        return self._requiredInstallationStatus

    @requiredInstallationStatus.setter
    def requiredInstallationStatus(self, value):
        # create new exception handling vor depdencies
        if not str(value).strip() in ["", "installed", "not_installed"]:
            raise ValueError(translate("ProductDependency", "Incorrect value for requiredInstallationStatus: " + str(value).strip()))
        self._requiredInstallationStatus = str(value).strip()

    @property
    def requirementType(self):
        return self._requirementType

    @requirementType.setter
    def requirementType(self, value):
        # create new exception handling vor depdencies
        if not str(value).strip() in ["", "before", "after"]:
            raise ValueError(translate("ProductDependency", "Incorrect value for requirementType: " + str(value).strip()))
        self._requirementType = str(value).strip()

class ControlFileData(QObject, LogMixin):
    """ Defines data structure of a complete opsi control file"""

    dataLoaded = pyqtSignal(bool)
    """Signal, true, when data is successfully load from file / false, if not"""
    dataSaved = pyqtSignal(bool)
    """Signal, true, when data is successfully saved to file / false, if not"""

    def __init__(self, productId = "new_product"):
        """
        Constructor of ControlFileData

        :param productId: Create dataset for this product id
        """
        super().__init__()

        self._depends = ""
        self._incremental = "False"
        self._id = ""                   # product id
        self._name = ""                 # product name
        self._description = ""          # description
        self._advice = ""               # hint
        self._type = "localboot"        # product type: netboot, localboot
        self._productversion = "1.0"    # version software product
        self._packageversion = "1"      # version opsi package
        self._priority = 0              # priority -100 <-> 100
        self._licenseRequired = "False" # True / False (only important for netboot products
        self._productClasses = ""       # not used: has to be empty at last
        self._setupScript = ""          # setup script name
        self._uninstallScript = ""      # uninstall script name
        self._updateScript = ""         # update script name
        self._alwaysScript = ""         # always script name
        self._onceScript = ""           # once script name
        self._customScript = ""         # custom script name
        self._userLoginScript = ""      # userLogin script name
        self._properties = []           # product properties
        self._dependencies = []         # product dependencies
        self._raw_changelog = ""        # raw text changelog entries
        self._changelog_converted = False  # mark if changelog entries have been converted from simple to extended
        self._changelog_style = "extended"  # style: extended, single=free text block
        self._projectfolder = ""        # current project folder
        self._ignoredConfigs = {}       # all ignored lines seperated by blocks

        self.init_data(productId)

    def init_data(self, productId = "new_product"):
        """
        Re-Init current ControlFileData object

        :param productId: product id
        :return:
        """
        self.depends = ""
        self.incremental = "False"
        self.id = productId
        self.name = productId
        self.description = "Please ad a valuable description."
        self.advice = ""
        self.type = "localboot"
        self.productversion = "1.0"
        self.packageversion = "1"
        self.priority = 0
        self.licenseRequired = False
        self.productClasses = ""
        self.setupScript = ""
        self.uninstallScript = ""
        self.updateScript = ""
        self.alwaysScript = ""
        self.onceScript = ""
        self.customScript = ""
        self.userLoginScript = ""
        self.properties = []
        self.dependencies = []
        self._raw_changelog = ""
        self.changelog_converted = False
        self.changelog_style = "extended"
        self.projectfolder = ""
        self.ignoredConfigs = {}
        self.logger.debug("Emit dataLoaded(True)")

        self.dataLoaded.emit(True)

    @property
    def ignoredConfigs(self):
        return self._ignoredConfigs

    @ignoredConfigs.setter
    def ignoredConfigs(self, value):
        self._ignoredConfigs = value

    @property
    def projectfolder(self):
        return self._projectfolder

    @projectfolder.setter
    def projectfolder(self, value):
        self._projectfolder = value

    @property
    def depends(self):
        return self._depends

    @depends.setter
    def depends(self, value):
        self._depends = value

    @property
    def incremental(self):
        return self._incremental

    @incremental.setter
    def incremental(self, value):
        self._incremental = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        # create new exception handling vor properties
        if str(value).strip() not in oPB.PRODTYPES:
            raise ValueError(translate("ControlFileData", "type must be netboot or localboot"))
        self._type = str(value).strip()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if str(value).strip() == "":
            raise ValueError(translate("ControlFileData","id cannot be empty"))
        self._id = str(value).strip()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # create new exception handling vor properties
        if str(value).strip() == "":
            raise ValueError(translate("ControlFileData","name cannot be empty"))
        self._name = str(value).strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def advice(self):
        return self._advice

    @advice.setter
    def advice(self, value):
        self._advice = value

    @property
    def productversion(self):
        return str(self._productversion)

    @productversion.setter
    def productversion(self, value):
        # create new exception handling vor properties
        if str(value).strip() == "":
            raise ValueError(translate("ControlFileData","product version cannot be empty"))
        self._productversion = str(value).strip()

    @property
    def packageversion(self):
        return str(self._packageversion).lower()

    @packageversion.setter
    def packageversion(self, value):
        # create new exception handling vor properties
        if str(value).strip() == "":
            raise ValueError(translate("ControlFileData","package version cannot be empty"))
        self._packageversion = str(value).strip().lower()

    def inc_packageversion(self):
        """
        Increment current package version

        Creates automatic increment and embeds it between to strings, like

            ".corr"<version>"corr"

        """
        match = re.compile(r"^(\d*)\.?((\d*)|(corr\d*corr))$")
        m = match.search(self.packageversion)
        #print(m.group(0))
        #print(m.group(1)[4:-4])
        #print(m.group(2))
        if m:
            if "corr" in m.group(2):
                pre_inc = int(m.group(2)[4:-4]) + 1
            elif m.group(2) == "":
                pre_inc = 1
            else:
                pre_inc = int(m.group(2)) + 1
            self.packageversion = m.group(1) + ".corr" + str(pre_inc) + "corr"
        else:
            self.packageversion = "99999error"

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if isinstance(value, "".__class__): # "".__class__ is the easiest way, to check if it's a string in Python 3
            raise ValueError(translate("ControlFileData", "priority must be integer between -100 and 100"))
        if value < -100:
            self._priority = -100
        elif value > 100:
            self._priority = -100
        else:
            self._priority = value

    @property
    def licenseRequired(self):
        return self._licenseRequired

    @licenseRequired.setter
    def licenseRequired(self, value):
        if str(value).strip() == "":
            value = "False"
        # create new exception handling vor properties
        if str(value).strip() not in ["True", "False"]:
            raise ValueError(translate("ControlFileData", "licenseRequired must be True or False"))
        self._licenseRequired = str(value).strip()

    @property
    def productClasses(self):
        return self._productClasses

    @productClasses.setter
    def productClasses(self, value):
        # not used now, so return always the same value
        self._productClasses = ""

    @property
    def setupScript(self):
        return self._setupScript

    @setupScript.setter
    def setupScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "setup script has invalid file extension"))
        self._setupScript = value

    @property
    def uninstallScript(self):
        return self._uninstallScript

    @uninstallScript.setter
    def uninstallScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "uninstall script has invalid file extension"))
        self._uninstallScript = value

    @property
    def updateScript(self):
        return self._updateScript

    @updateScript.setter
    def updateScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "update script has invalid file extension"))
        self._updateScript = value

    @property
    def alwaysScript(self):
        return self._alwaysScript

    @alwaysScript.setter
    def alwaysScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "always script has invalid file extension"))
        self._alwaysScript = value

    @property
    def onceScript(self):
        return self._onceScript

    @onceScript.setter
    def onceScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "once script has invalid file extension"))
        self._onceScript = value

    @property
    def customScript(self):
        return self._customScript

    @customScript.setter
    def customScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "custom script has invalid file extension"))
        self._customScript = value

    @property
    def userLoginScript(self):
        return self._userLoginScript

    @userLoginScript.setter
    def userLoginScript(self, value):
        if not Helper.extCheck(value):
            raise ValueError(translate("ControlFileData", "userLogin script has invalid file extension"))
        self._userLoginScript = value

    @property
    def properties(self):
        if self._properties == []:
            # return [["empty", "", "", "", "", "", ""]]
            return []
        else:
            tmp = []
            for item in self._properties:
                item[0] = item[0].lower()
                tmp.append(item) if item not in tmp else None
            self._properties = tmp
            return self._properties

    @properties.setter
    def properties(self, value):
        # create new exception handling vor properties
        # if (value != "True") and (value != "False"):
        #    raise ValueError("describe exception")
        self._properties = value

    def properties_append(self, prop: ProductProperty):
        """
        Add product property object to list.

        :param prop: Object of class ProductProperty
        """
        if not type(prop) == ProductProperty:
            raise TypeError(translate("ControlFileData", "Wrong type for property data"))
        else:
            self._properties.append([prop.name, prop.type, prop.multivalue, prop.editable,
                                     prop.description, prop.values, prop.default])

    def del_property(self, prop: ProductProperty):
        """
        Remove product property object from list.

        :param prop: Object of class ProductProperty
        """
        if not type(prop) == ProductProperty:
            raise TypeError(translate("ControlFileData", "Wrong type for property data"))
        else:
            if [prop.name, prop.type, prop.multivalue, prop.editable, prop.description, prop.values, prop.default] in self._properties:
                self._properties.remove([prop.name, prop.type, prop.multivalue, prop.editable, prop.description, prop.values, prop.default])

    def properties_getnames(self):
        """
        List of property names
        :return: list
        """
        if self._properties == []:
            return []
        else:
            tmp = []
            for item in self._properties:
                item[0] = item[0].lower()
                tmp.append(item[0]) if item not in tmp else None
            return tmp

    @property
    def dependencies(self):
        if self._dependencies == []:
            #return [["empty", "", "", "", ""]]
            return []
        else:
            tmp = []
            for item in self._dependencies:
                item[0] = item[0].lower()
                tmp.append(item) if item not in tmp else None
            return self._dependencies
    
    @dependencies.setter
    def dependencies(self, value):
        # create new exception handling vor dependencies
        #if (value != "True") and (value != "False"):
        #    raise ValueError("describe exception")
        self._dependencies = value

    def dependencies_append(self, dep: ProductDependency):
        """
        Add product dependency object to list.

        :param dep: Object of class ProductDependency
        """
        if not type(dep) == ProductDependency:
            raise TypeError(translate("ControlFileData", "Wrong type for dependency data"))
        else:
            self._dependencies.append([dep.dependencyForAction, dep.requiredProductId, dep.requiredAction,
                                       dep.requiredInstallationStatus, dep.requirementType])

    def del_dependency(self, dep: ProductDependency):
        """
        Remove product dependency object from list.

        :param dep: Object of class ProductDependency
        """
        if not type(dep) == ProductDependency:
            raise TypeError(translate("ControlFileData", "Wrong type for dependency data"))
        else:
            if [dep.dependencyForAction, dep.requiredProductId, dep.requiredAction, dep.requiredInstallationStatus, dep.requirementType] \
                    in self._dependencies:
                self._dependencies.remove([dep.dependencyForAction, dep.requiredProductId, dep.requiredAction,
                                           dep.requiredInstallationStatus, dep.requirementType])

    @property
    def changelog(self):
            return self._raw_changelog

    @changelog.setter
    def changelog(self, value):
        if ConfigHandler.cfg.use_extended_changelog == "True":
            self.changelog_style = "extended"
            self._raw_changelog = self._changelog_setfromlist(value)
        else:
            self.changelog_style = "simple"
            self._raw_changelog = value

    @property
    def changelog_style(self):
        return self._changelog_style

    @changelog_style.setter
    def changelog_style(self, value):
        if str(value).strip() not in ["simple", "extended"]:
            raise ValueError(translate("ControlFileData", "changelog_style must be 'simple' or 'extended'"))
        self._changelog_style = str(value).strip()

    @property
    def changelog_converted(self):
        return self._changelog_converted

    @changelog_converted.setter
    def changelog_converted(self, value: bool):
        if value not in [True, False]:
            raise ValueError(translate("ControlFileData", "changelog_converted must be True or False"))
        self._changelog_converted = value

    def changelog_gettable(self):
        """
        Returns flat table of extended changelog data:

        single row: ["prod id", "version string", "status", "urgency", "details"]

        :return: list of lists of changelog entries
        """

        # Entry format:  ' -- MaintainerName <EMail>  Timestamp'
        dummy_added = None

        if (ConfigHandler.cfg.use_extended_changelog == "True") and (ConfigHandler.cfg.chlog_block_marker.upper() == oPB.CHLOG_BLOCKMARKER.upper()):
            if self._raw_changelog.strip() == "":
                init = [self.id, "(" + self.productversion + "-" + self.packageversion + ")",
                        oPB.CHLOG_STATI[0], oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0],
                        "\n" + translate("ControlFileData", " * Initial entry") + changelog_footer()]
                return([init])
            else:
                entries = []
                text = ""
                for line in self._raw_changelog.splitlines():
                    if ConfigHandler.cfg.chlog_block_marker.upper() in line.upper():  # block marker found
                        text = ""
                        elems = line.strip().split()
                        if len(elems) > 2: elems[2] = elems[2].strip(";")
                        elems.append(text)
                        entries.append(elems)
                    else:
                        text += line + "\n"

                    # check, if we have text BUT NO new entry -> free text, so create dummy entry
                    if not entries:
                        entries = [
                            [translate("ControlFileData", "Converted"), "(" + self.productversion + "-" + self.packageversion + ")",
                             oPB.CHLOG_STATI[0], oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0],
                            text]
                            ]
                        dummy_added = len(entries) - 1
                    else:
                        # take last (entries) list element and append text to its (last entry) last element ;-)
                        entries[len(entries) - 1][len(entries[len(entries) - 1]) - 1] = text.rstrip() + "\n"  # remove unnecessary right \n

                # IF we had a dummy entry because of free text, and special marker and complete it now
                if dummy_added != None:
                    header = "\n"  + translate("ControlFileData", "Converted freetext changelog entries:") + "\n\n"
                    stripped = entries[dummy_added][len(entries[dummy_added]) - 1].rstrip()
                    marked = ""
                    spacer = 5 * " "
                    snipline = spacer + 50 * "-" + "\n"
                    for line in stripped.splitlines():
                        marked += spacer  + " > " + line + "\n"
                    entries[dummy_added][len(entries[dummy_added]) - 1] = header + snipline + marked + snipline + changelog_footer()

                return entries
        elif (ConfigHandler.cfg.use_extended_changelog == "True") and (ConfigHandler.cfg.chlog_block_marker.upper() != oPB.CHLOG_BLOCKMARKER.upper()):
            pass
        else:
            raise ValueError(translate("ControlFileData", "changelog_gettable cannot be used for simple changelog format"))

    def changelog_getobjects(self):
        """
        Returns list of ChangelogEntry objects of extended changelog data:

        :return: list of ChangelogEntry Objects
        """

        # entry format:  ' -- MaintainerName <EMail>  Timestamp'
        dummy_added = None

        if (ConfigHandler.cfg.use_extended_changelog == "True") and (ConfigHandler.cfg.chlog_block_marker.upper() == oPB.CHLOG_BLOCKMARKER.upper()):
            if self._raw_changelog.strip() == "":
                init = ChangelogEntry(self.id)
                init.version = "(" + self.productversion + "-" + self.packageversion + ")"
                init.status = oPB.CHLOG_STATI[0]
                init.urgency = oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0]
                init.text = "\n" + translate("ControlFileData", " * Initial entry") + changelog_footer()
                return([init])
            else:
                entries = []
                text = ""
                for line in self._raw_changelog.splitlines():
                    if ConfigHandler.cfg.chlog_block_marker.upper() in line.upper():  # block marker found
                        text = ""
                        elems = line.strip().split()
                        elems[2] = elems[2].strip(";")
                        entry = ChangelogEntry(elems[0])
                        entry.version = elems[1]
                        entry.status = elems[2]
                        entry.urgency = elems[3]
                        entries.append(entry)
                    else:
                        text += line + "\n"

                    # check, if we have text BUT NO new entry -> free text, so create dummy entry
                    if not entries:
                        entry = ChangelogEntry(translate("ControlFileData", "Converted"))
                        entry.version = "(" + self.productversion + "-" + self.packageversion + ")"
                        entry.status = oPB.CHLOG_STATI[0]
                        entry.urgency = oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0]
                        entry.text = text
                        entries.append(entry)
                        dummy_added = len(entries) - 1
                    else:
                        entries[len(entries) - 1].text = text.rstrip() + "\n"  # remove unnecessary right \n

                # IF we had a dummy entry for free text, complete it now
                if dummy_added != None:
                    header = "\n"  + translate("ControlFileData", "Converted freetext changelog entries:") + "\n\n"
                    stripped = entries[dummy_added].text.rstrip()
                    marked = ""
                    for line in stripped.splitlines():
                        marked += " > " + line + "\n"
                    entries[dummy_added].text = header + marked + changelog_footer()

                return entries

        elif (ConfigHandler.cfg.use_extended_changelog == "True") and (ConfigHandler.cfg.chlog_block_marker.upper() != oPB.CHLOG_BLOCKMARKER.upper()):
            pass
        else:
            raise ValueError(translate("ControlFileData", "changelog_getlist cannot be used for simple changelog format"))

    def changelog_append(self, entry: ChangelogEntry):
        """
        Add changelog entry object to list.

        :param dep: Object of class ChangelogEntry
        """
        if type(entry) is not ChangelogEntry:
            raise ValueError(translate("ControlFileData", "Parameter elements in list must be of type ChangelogEntry"))
        else:
            if self._raw_changelog.strip() != "":
                entries = self.changelog_getobjects()
                entries.insert(0, entry)
            else:
                entries = [entry]
            self.changelog = entries

    def _changelog_setfromlist(self, values: list):
        """
        Set changelog attribute from list of ChangelogEntry objects

        :param values: list[ChanglogEntry]
        :return:
        """
        text = ""
        if type(values) is not list:
            raise ValueError(translate("ControlFileData", "Parameter value must be of type list"))
            return
        for elem in values:
            if type(elem) is not ChangelogEntry:
                raise ValueError(translate("ControlFileData", "Parameter elements in list must be of type ChangelogEntry"))
                return
            if ConfigHandler.cfg.chlog_block_marker.upper() == oPB.CHLOG_BLOCKMARKER.upper():
                text += "\n" + elem.productId + " " + elem.version + " " + elem.status + "; " + elem.urgency + "\n" + elem.text
            else:
                text += "\n" + elem.individual + "\n" + elem.text

        return text.strip()

    @property
    def packagename(self):
        return self.id + "_" + self.productversion + "-" + self.packageversion + ".opsi"

    @property
    def local_package_path(self):
        return self.projectfolder.replace("\\","/") + "/" + self.packagename

    @property
    def path_on_server(self):
        """
        Derive project path on server from local project folder path

        :return: project path on server
        """

        # change dev_base if necessary
        if ConfigHandler.cfg.wb_new == "True":
            oPB.DEV_BASE = oPB.DEV_BASE_OPSI41
        else:
            oPB.DEV_BASE = oPB.DEV_BASE_OPSI40

        # if on Linux, we have to subtract local share base from development folder
        # -> the local share base acts like the drive letter on windows
        if platform.system() == 'Linux':
            tmp = self.projectfolder.replace(ConfigHandler.cfg.local_share_base, "")
        else:
            tmp = self.projectfolder

        if platform.system() == "Windows":
            # remove drive letter
            return oPB.DEV_BASE + tmp[2:].replace("\\", "/")
        else:
            # replace possible double '/' with single '/'
            return (oPB.DEV_BASE + "/" + tmp).replace("//", "/")

            """
            if tmp.startswith(repo_base):
                return tmp
            else:
                if tmp.strip() != "":
                    ret = (repo_base + "/" + tmp + "/" + self.id).replace("//", "/")
                    print("a", ret)
                    return ret
                else:
                    ret = (repo_base + "/" + self.id).replace("//", "/")
                    print("b", ret)
                    return ret
            """

    def load_data(self, projectfolder):
        """
        Load control file data

        :param projectfolder: name of project
        :return:
        """
        matchSection = re.compile('^\s*\[([^\]]+)\]\s*$')
        # valueContinuationRegex = re.compile('^\s(.*)$')
        matchOption = re.compile('^([^\:]+)\s*\:\s*(.*)$')

        self.projectfolder = projectfolder
        self.logger.debug("Backend project to load: " + projectfolder)

        try:
            with open(projectfolder + "/OPSI/control", "r", encoding="utf-8", newline="\n") as file:
                self.logger.debug("Control file opened: " + projectfolder + "/OPSI/control")
                lines = file.readlines()
        except:
            self.logger.error("Error reading control file")
            self.logger.debug("Emit dataLoaded(False)")
            self.dataLoaded.emit(False)
            return

        self.logger.debug("----- Raw control file data: -----")
        for line in lines:
            self.logger.debug(line.strip())
        self.logger.debug("----- End of File -----")

        self.logger.debug("Parsing control data")

        lines_count = 0
        currentline = 1
        for line in lines: lines_count += 1
        lines_count -= 1 # -1, because we count from 0

        self.logger.debug("Lines count: "+ str(lines_count))

        while currentline <= lines_count:
            # separate control blocks
            lastparam = None
            block = lines[currentline - 1].strip().upper()
            if block in ['[PRODUCT]', '[PACKAGE]']:
                self.logger.debug("Block: " + block)
                while (currentline <= lines_count) and (lines[currentline].strip()[:1] != "["):
                    # separate parameter from values
                    paramline = matchOption.search(lines[currentline])
                    if paramline:
                        param = paramline.group(1).upper()
                        value = paramline.group(2).strip()
                        lastparam = param
                        self.logger.debug("Param: " + paramline.group(1) + " /// Value: (" + paramline.group(2).strip() +")")

                        if param == "VERSION":
                            if block == "[PACKAGE]":
                                self.packageversion = value
                            else:
                                self.productversion = value
                        elif param == "DEPENDS":
                            self.depends = value
                        elif param == "INCREMENTAL":
                            self.incremental = value
                        elif param == "TYPE":
                            self.type = value
                        elif param == "ID":
                            self.id = value
                        elif param == "NAME":
                            self.name = value
                        elif param == "DESCRIPTION":
                            self.description = value
                        elif param == "ADVICE":
                            self.advice = value
                        elif param == "PRIORITY":
                            self.priority = int(value)
                        elif param == "LICENSEREQUIRED":
                            self.licenseRequired = value
                        elif param == "PRODUCTCLASSES":
                            pass
                        elif param == "SETUPSCRIPT":
                            self.setupScript = value
                        elif param == "UNINSTALLSCRIPT":
                            self.uninstallScript = value
                        elif param == "UPDATESCRIPT":
                            self.updateScript = value
                        elif param == "ALWAYSSCRIPT":
                            self.alwaysScript = value
                        elif param == "ONCESCRIPT":
                            self.onceScript = value
                        elif param == "CUSTOMSCRIPT":
                            self.customScript = value
                        elif param == "USERLOGINSCRIPT":
                            self.userLoginScript = value
                        else:
                            if not block in self.ignoredConfigs:
                                self.ignoredConfigs[block] = {}
                            self.ignoredConfigs[block][param] = [paramline.group(1), value]
                    else:
                        if lastparam == "DESCRIPTION":
                            self.description += "\n"+lines[currentline][:-1]
                        elif lastparam == "ADVICE":
                            self.advice += "\n"+lines[currentline][:-1]
                        elif lines[currentline].strip(): # add only non empty lines
                            self.ignoredConfigs[block][lastparam][1] += "\n"+lines[currentline][:-1]

                    currentline += 1
                    if currentline > lines_count: break

            if block == '[PRODUCTDEPENDENCY]':
                self.logger.debug("Block: " + block)
                dep = ProductDependency()
                while (currentline <= lines_count) and (lines[currentline].strip()[:1] != "["):
                    # ignore empty lines
                    if lines[currentline].strip()[:1] == '':
                        currentline += 1
                        continue
                    # separate parameter from values
                    paramline = lines[currentline].strip().split(":", 1)
                    if len(paramline) == 2:
                        param = paramline[0].strip().upper()
                        value = paramline[1].strip()
                        self.logger.debug("Param: " + paramline[0].strip() + " /// Value: " + paramline[1].strip())

                        if param == "ACTION":
                            dep.dependencyForAction = value
                        elif param == "REQUIREDPRODUCT":
                            dep.requiredProductId = value
                        elif param == "REQUIREDACTION":
                            dep.requiredAction = value
                        elif param == "REQUIREDSTATUS":
                            dep.requiredInstallationStatus = value
                        elif param == "REQUIREMENTTYPE":
                            dep.requirementType = value

                    currentline += 1
                    if currentline > lines_count: break

                self.dependencies_append(dep)

            if block == '[PRODUCTPROPERTY]':
                self.logger.debug("Block: " + block)
                prop = ProductProperty()
                lasttype = ''
                while (currentline <= lines_count) and (lines[currentline].strip()[:1] != "["):
                    # ignore empty lines
                    if lines[currentline].strip()[:1] == '':
                        currentline += 1
                        continue
                    # separate parameter from values
                    paramline = lines[currentline].strip().split(":", 1)
                    if len(paramline) == 2:
                        param = paramline[0].strip().upper()
                        value = paramline[1].strip()
                        self.logger.debug("Param: " + paramline[0].strip() + " /// Value: " + paramline[1].strip())

                        if param == 'NAME':
                            prop.name = value
                        elif param == 'TYPE':
                            prop.type = value
                            lasttype = value
                        elif param == 'MULTIVALUE':
                            prop.multivalue = value
                        elif param == 'EDITABLE':
                            prop.editable = value
                        elif param == 'DESCRIPTION':
                            prop.description = value
                        elif param == 'VALUES':
                            # tmp = value[2:len(value)-2]
                            # tmp = tmp.replace('\\"', '_$%&%DUMMY%&%$_')
                            # tmp = tmp.replace('"', '')
                            # tmp = tmp.replace('_$%&%DUMMY%&%$_', '"')
                            # tmp = tmp.replace('\\\\', '\\')
                            # prop.values = tmp
                            if value != "": prop.values = json.loads(value)
                        elif param == 'DEFAULT':
                            if lasttype == 'bool':
                                prop.default = value
                            else:
                                # tmp = value[2:len(value)-2]
                                # tmp = tmp.replace('\\"', '_$%&%DUMMY%&%$_')
                                # tmp = tmp.replace('"', '')
                                # tmp = tmp.replace('_$%&%DUMMY%&%$_', '"')
                                # tmp = tmp.replace('\\\\', '\\')
                                # prop.default = tmp
                                if value != "": prop.default = json.loads(value)

                    currentline += 1
                    if currentline > lines_count: break

                self.properties_append(prop)

            if block == '[CHANGELOG]':
                self.logger.debug("Block: " + block)
                while (currentline <= lines_count) and (lines[currentline].strip()[:1] != "["):
                    # remove empty line after [Changelog], if present
                    if (lines[currentline-1].strip() == block) and lines[currentline].strip() == '':
                        currentline +=1
                        continue
                    # get each line unmodified
                    paramline = lines[currentline]
                    self._raw_changelog += paramline
                    self.logger.debug("Param: " + paramline.strip("\r\n"))

                    currentline += 1
                    if currentline > lines_count: break
                self._raw_changelog = self._raw_changelog.strip()

            currentline += 1
            if currentline > lines_count: break

        self.logger.info("Control file read successfully")
        self.logger.debug("Emit dataLoaded(True)")
        self.dataLoaded.emit(True)

    def save_data(self):
        """Save control file data of current project"""
        controlfile = self._projectfolder + "/OPSI/control"

        def get_ignored_configs(block):
            res = ""
            if block in self.ignoredConfigs:
                for key in self.ignoredConfigs[block]:
                    name, value = self.ignoredConfigs[block][key]
                    res += "{0}: {1}\n".format(name, value)
            return res

        if Path(controlfile).exists():
            try:
                shutil.move(controlfile, controlfile + "-" + Helper.timestamp() + ".bak")

            except IOError:
                self.logger.error("Existing control file could not be renamed")
                self.logger.debug("Emit dataLoaded(False)")
                self.dataSaved.emit(False)
                return

        try:
            with open(self._projectfolder + "/OPSI/control", "x", encoding="utf-8", newline="\n") as file:
                self.logger.debug("Control file opened: " + self._projectfolder + "/OPSI/control")

                file.write("[Package]\n")
                file.write("version: " + self.packageversion + "\n")
                file.write("depends: " + self.depends + "\n")
                file.write("incremental: " + self.incremental + "\n")
                file.write(get_ignored_configs("[PACKAGE]"))
                file.write("\n")
                file.write("[Product]\n")
                file.write("type: " + self.type + "\n")
                file.write("id: " + self.id + "\n")
                file.write("name: " + self.name + "\n")
                file.write("description: " + self.description + "\n")
                file.write("advice: " + self.advice + "\n")
                file.write("version: " + self.productversion + "\n")
                file.write("priority: " + str(self.priority) + "\n")
                file.write("licenseRequired: " + self.licenseRequired + "\n")
                file.write("productClasses: " + self.productClasses + "\n")
                file.write("setupScript: " + self.setupScript + "\n")
                file.write("uninstallScript: " + self.uninstallScript + "\n")
                file.write("updateScript: " + self.updateScript + "\n")
                file.write("alwaysScript: " + self.alwaysScript + "\n")
                file.write("onceScript: " + self.onceScript + "\n")
                file.write("customScript: " + self.customScript + "\n")
                file.write("userLoginScript: " + self.userLoginScript + "\n")
                file.write(get_ignored_configs("[PRODUCT]"))

                if self.dependencies:
                    for elem in self.dependencies:
                        file.write("\n")
                        file.write("[ProductDependency]\n")
                        file.write("action: " + elem[0] + "\n")
                        file.write("requiredProduct: " + elem[1] + "\n")
                        if elem[2] not in ["", "none"]:
                            file.write("requiredAction: " + elem[2] + "\n")
                        else:
                            file.write("requiredStatus: " + elem[3] + "\n")
                        file.write("requirementType: " + elem[4] + "\n")

                if self.properties:
                    for elem in self.properties:
                        file.write("\n")
                        file.write("[ProductProperty]\n")
                        file.write("type: " + elem[1] + "\n")
                        file.write("name: " + elem[0] + "\n")
                        if elem[1] == "unicode":
                            file.write("multivalue: " + elem[2] + "\n")
                            file.write("editable: " + elem[3] + "\n")
                        file.write("description: " + elem[4] + "\n")
                        if elem[1] == "unicode":
                            v = json.dumps(elem[5], ensure_ascii=False)
                            d = json.dumps(elem[6], ensure_ascii=False)
                            if v == '""':  # empty string returned by json.dumps
                                file.write("values: \n")
                            else:
                                file.write("values: " + v + "\n")
                            if d == '""':  # empty string returned by json.dumps
                                file.write("default: \n")
                            else:
                                file.write("default: " + d + "\n")
                        else:
                            file.write("default: " + elem[6] + "\n")

                file.write("\n")
                file.write("[Changelog]\n")
                file.write(self.changelog)

                file.close()
                self.logger.debug("Emit dataSaved(True)")
                self.dataSaved.emit(True)  # on success

        except:
            self.logger.error("Error writing control file")
            self.logger.exception("Error writing control file")
            self.logger.debug("Emit dataSaved(False)")
            self.dataSaved.emit(False)

    def create_script_stub(self, scriptname):
        """Create script file stub in current project folder"""
        scriptfile = self._projectfolder + "/CLIENT_DATA/" + scriptname

        if Path(scriptfile).exists():
            self.logger.warn("Script already exists.")
            return

        try:
            with open(scriptfile, "x", encoding="utf-8", newline="\n") as file:
                self.logger.debug("Script stub opened: " + scriptfile)

                file.write("; ----------------------------------------------------------------\n")
                file.write(";    Script stub created via opsi PackageBuilder\n")
                file.write("; ----------------------------------------------------------------\n")
                file.write("\n")
                file.write("[Actions]\n")
                file.write("\n")
                file.write('comment "Script stub: ' + scriptname + '"\n')
                file.write("\n")
                file.close()
                self.logger.debug("Script stub created.")

        except:
            self.logger.error("Error creating script stub")
            self.logger.exception("Error creating script stub")


    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__init__(self.id)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__init__(self.id)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
