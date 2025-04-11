
import json
import os
from pickle import TRUE
import sys
from tkinter import Text
import xml.etree.ElementTree as ET
import datetime
import io

try:
    import pyi_splash
except:
    print("Not imported")

#   GUI INCLUDES
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QAbstractItemModel, QModelIndex

# file open / search includes
from typing import Any, List, Union
import os.path as osp
import posixpath, mimetypes
import time

#    Get designer screens in.
from EditWindow import Ui_Dialog
from MainWindow import Ui_MainWindow
from Prefs import Ui_PrefsEditor
from About import Ui_About
from OpenFile import Ui_OpenDialog


#   OpenSongViewer
#
#   Open, view, edit and create songs created by OpenSong
#   To be used as an electronic Songbook

#   Carl Beech 2020

#   History

#   0.1 -   Initial release
#   0.2 -   Added browse button to preferences dialog.
#           Start of code cleanup
#           Initial conversion to allow for linux filesystems.
#           Switch to use 'dictionary' (key/value pairs) to hold preferences.
#   0.3 -   Improvements to preferences
#           *   Default font size
#           *   Sharps/Flats preferences.
#           *   About window
#   0.4 -   Added page size to preferences window
#           When saving, Copy all data within the existing song forward
#           so no details are lost.
#   0.5 -   Bugfix: if base key is 'B' then transposing doesn't update the
#                   key displayed on screen.
#           Improvement: you can now use cursor right/left to move through the
#                   song list (up/down appear to be caught by the system before
#                   they are captured by the program, so are not reliable.
#           Improvement: additional, via preferences - when editing you can
#                   keep the 'normal' edit using the original base key, or
#                   you can edit using the current transposed key - this is useful
#                   if you want to adjust a song that you've transposed - you
#                   don't have to manually transpose the ammendment back to the
#                   original key. NOTE: if you edit using the transposed key
#                   this will _overwrite_ the original base key.
#                   As part of this, to factor out code main data structures are
#                   made global.
#   0.6 -   Improvement - remove leading spaces on text.
#           Improvement - can set font size for a given song, or select 'Default'
#           Improvement - re-configures when switching from landscape to portrait
#           Improvement - can use different fonts for landscape and portrait.

#  0.8 -    Noted issue - all song information is saved in a song list file - 
#               this includes the song text itself
#               this can create an issue if you load in an old song list, and 
#               then edit a song... it won't use song data from a song file
#               it'll use the song data from the song list - as such, you can
#               effectively overwrite updated songs with old song information
#               that has been reloaded from a song list.
#           Noted issue - occasionally an extra line break was added- fixed
#           Noted issue - Removal of line break stopped font size setting
#               for song-set font sizes - fixed.

# 0.9 -  Updated file open dialog so that when typing, the file list
#        is restricted - applies to the file name and also the file contents
#        similar to windows start menu.

# 0.9a - Updated to be able to use up and down keys in the search screen as well as
#        press return to select the current song.

# 0.91 - Use of CSS black-magic so that the chord appears above the text
#        so switch to use of QWebEngine for main screen, as this understands 
#        real CSS.. this means proportional fonts can be used to display
#        and less wasted space
#        This has meant a requirement for logic to merge the chord and lyric lines
#        Also updated prefs to be able to switch off/on logging

VersionNumber = "0.91"
VersionInformation = "Release 10/4/25 - Carl Beech"

# SongDataList - main Data structure
# 0 - full file and path name
# 1 - lyrics text
# 2 - Base key
# 3 - Offset
# 4 - Basename (just the file name)
# 5 - Font Size    ( Default or a font size - Landscape)
# 6 - Font Size    ( Default or a font size - Portrait)
# 7 - Line count before column break (Default or a line count) - Landscape
# 8 - Line count before column break (Default or a line count) - Portrait

SongDataList = []
SongKeys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SongKeys_Alt = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# V0.2: switch to use dictionary so can use a key:value pair.
SongPreferences = {'DUMMY': 'DUMMY'}

LogFileName=datetime.datetime.now().strftime("OpenSongViewer-%Y-%m-%d_%H_%M_%S.log")

def logmessage( MessageText ):
    global SongPreferences

    try:
        if SongPreferences['PRODUCE_LOG_FILES']==1:
            MessageTime=datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

            with open(LogFileName, 'a') as fd:
                fd.write( MessageTime+": "+MessageText+'\n')
    except:
        return

def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

#   Initialisation of Edit Window
class AboutWindow(QDialog):

    def __init__(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("AboutWindow:")

        super().__init__()
        self.ui = Ui_About()
        self.ui.setupUi(self)

        #   Copy variable values for single song into on-screen fields.
        AboutText=              "<html><head>"
        AboutText = AboutText + "<style>"
        AboutText = AboutText + "body { background-color: #FFFFFF;} "
        AboutText = AboutText + "p { font-size: 25px; margin: 0px; align=center;} "
        AboutText = AboutText + "</style>"
        AboutText = AboutText + "</head>"
        AboutText = AboutText + "<body>"
        AboutText = AboutText + "<h4>Open Song Viewer</h4><br>"
        AboutText = AboutText + "<p>Version "+VersionNumber+"</p>"
        AboutText = AboutText + "<p>Carl Beech 2020</p>"
        AboutText = AboutText + "<p><a href='https://github.com/carlbeech/OpenSongViewer'>https://github.com/carlbeech/OpenSongViewer</a></p>"
        AboutText = AboutText + "</body>"
        AboutText = AboutText + "</html>"

        self.ui.aboutMessage.setHtml( AboutText )

        #   Set the window up.
        self.show()


#============================================================================================

# Classes to deal with open file / file search

def grep(filename, searchString):
    # Perform a search in a file for a given string (note not case sensitive)

    # print("Checking: "+filename)
    try:
        with open(filename, 'r', encoding="utf8") as myfile:
            LoadSongData = myfile.read()
    except:
        try:
            with open(filename, 'r') as myfile:
                LoadSongData = myfile.read()
        except:
            print(filename+" error")
            LoadSongData=""

    if ( searchString.upper() in LoadSongData.upper() ):
        return True
    else:  
        return False



FSMItemOrNone = Union["_FileSystemModelLiteItem", None]


def sizeof_fmt(num, suffix="B"):
    """Creates a human readable string from a file size"""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def grep(filename, searchString):
    # Perform a search in a file for a given string (note not case sensitive)

    # print("Checking: "+filename)
    try:
        with open(filename, 'r', encoding="utf8") as myfile:
            LoadSongData = myfile.read()
    except:
        try:
            with open(filename, 'r') as myfile:
                LoadSongData = myfile.read()
        except:
            print(filename+" error")
            LoadSongData=""

    if ( searchString.upper() in LoadSongData.upper() ):
        return True
    else:  
        return False


class _FileSystemModelLiteItem(object):
    """Represents a single node (drive, folder or file) in the tree"""

    def __init__(
                self,
                data: List[Any],
                parent: FSMItemOrNone = None,
                fullpath = "",
                ):
        self._data: List[Any] = data
        self._parent: _FileSystemModelLiteItem = parent
        self.child_items: List[_FileSystemModelLiteItem] = []
        self.fullpath: fullpath

    def append_child(self, child: "_FileSystemModelLiteItem"):
        self.child_items.append(child)

    def child(self, row: int) -> FSMItemOrNone:
        try:
            return self.child_items[row]
        except IndexError:
            return None

    def child_count(self) -> int:
        return len(self.child_items)

    def column_count(self) -> int:
        return len(self._data)

    def data(self, column: int) -> Any:
        try:
            return self._data[column]
        except IndexError:
            return None

    def row(self) -> int:
        if self._parent:
            return self._parent.child_items.index(self)
        return 0

    def parent_item(self) -> FSMItemOrNone:
        return self._parent



class FileSystemModelLite(QAbstractItemModel):
    def __init__(self, file_list: List[str], FileStartLocation, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._root_item = _FileSystemModelLiteItem(["Name", "Size", "Modification Date"])  #,"FileLoc"
        self._setup_model_data(file_list, self._root_item, FileStartLocation)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        item: _FileSystemModelLiteItem = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(index.column())
        elif index.column() == 0 and role == Qt.DecorationRole:
            return 0
        return None

    def fullpath(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        item: _FileSystemModelLiteItem = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(3)
        elif index.column() == 0 and role == Qt.DecorationRole:
            return 0
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root_item.data(section)
        return None

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: _FileSystemModelLiteItem = index.internalPointer()
        parent_item: FSMItemOrNone = child_item.parent_item()

        if parent_item == self._root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self._root_item.column_count()

    def _setup_model_data(self, file_list: List[str], parent: "_FileSystemModelLiteItem", FileStartLocation):
        def _add_to_tree(_file_record, _parent: "_FileSystemModelLiteItem", root=False, FullFileLocation=""):
            item_name = _file_record["bits"].pop(0)

            for child in _parent.child_items:
                if item_name == child.data(0):
                    item = child
                    break
            else:
                data = [item_name, "", "",FullFileLocation]
                if root:
                    dummy=1
                elif len(_file_record["bits"]) == 0:
                    data = [
                            item_name,
                            _file_record["size"],
                            _file_record["modified_at"],
                            FullFileLocation,
                            ]
                else:
                    dummy=1

                item = _FileSystemModelLiteItem(data,parent=_parent)
                _parent.append_child(item)

            if len(_file_record["bits"]):
                _add_to_tree(_file_record, item, False, FullFileLocation)

        for file in file_list:
            file_record = {
                            "size": sizeof_fmt(osp.getsize(file)),
                            "modified_at": time.strftime("%Y-%b-%d %H:%M:%S", time.localtime(osp.getmtime(file))),
                            "fullfilelocation":file
                            }

            drive = True
            if "\\" in file:
                file = posixpath.join(*file.split("\\"))
            
            shortfile=file.replace(FileStartLocation,"")

            bits = shortfile.split("/")
            if len(bits) > 1 and bits[0] == "":
                bits[0] = "/"
                drive = False

            file_record["bits"] = bits
            _add_to_tree(file_record, parent, drive, file)


#============================================================================================

class StandardItem(QStandardItem):

    def __init__(self,txt='',font_size=12,set_bold=False,color=QColor(0,0,0)):
        super().__init__()

        fnt=QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class OpenFile(QDialog):

    def __init__(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("OpenFile:Init")

        super().__init__()
        self.ui = Ui_OpenDialog()
        self.ui.setupUi(self)
        self.InitUI()

        #   Set the window up
        self.show()


    def InitUI(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("OpenFile:InitUI")

        self.setWindowTitle('Select song...')
        self.ui.lineEdit.setText('Start typing')

        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        self.resize(self.width-50,self.height-80)


        #self.model = QFileSystemModel()
        #self.model.setRootPath('')
        #self.model.setNameFilters(['*.xml']) 
        #self.model.setNameFilterDisables(False) 
        #self.ui.treeView.setModel(self.model)
        #self.ui.treeView.setRootIndex(self.model.index(SongPreferences['SONGDIR']))
        
        #self.ui.treeView.setAnimated(False)
        #self.ui.treeView.setIndentation(20)
        #self.ui.treeView.setSortingEnabled(True)
        #self.ui.treeView.setColumnWidth(0,500)

        #self.ui.treeView.clicked.connect(self.clickedTree)
        #self.ui.treeView.doubleClicked.connect(self.DoubleClickedTree)

        self.ui.treeView.installEventFilter(self)

        #self.ui.treeView.setHeaderHidden(False)

        #treemodel=QStandardItemModel()
        #rootNode=treemodel.invisibleRootItem()

        #   Go through all the files, but dont follow links
        #for root, subdirs, files in os.walk(SongPreferences['SONGDIR'], followlinks=False):

        #    FolderNode=StandardItem(root.split(os.path.sep)[-1])

        #    print( "New folder: "+root.split(os.path.sep)[-1])

        #    for filename in files:

        #        print( "  File: "+filename)

        #        file_path = os.path.join(root, filename)

        #        FileNode=StandardItem(filename)

        #        FolderNode.appendRow(FileNode)

        #    rootNode.appendRow(FolderNode)


        #self.FilesArray={}

        self.ScanFolder(SongPreferences['SONGDIR']+"/")

        self.ui.treeView.clicked.connect(self.clickedTree)
        self.ui.treeView.doubleClicked.connect(self.DoubleClickedTree)


        #a=StandardItem('first')
        #aa=StandardItem('firstfirst')

        #a.appendRow(aa)

        #b=StandardItem('second')

        #rootNode.appendRow(a)
        #rootNode.appendRow(b)

        #self.ui.treeView.setModel(treemodel)
        #self.ui.treeView.expandAll()


        self.ui.lineEdit.textChanged.connect(self.lineEditTextChanged)

        self.ui.lineEdit.setFocus()

    def ScanFolder(self,startpath):
        file_list=[]
        for root, subdirs, files in os.walk(startpath, followlinks=False):

            for file in files:

                if ( ".xml" in file):
                    file_list.append(root+os.path.sep+file)

        self._fileSystemModel = FileSystemModelLite(file_list, startpath, self)

        self.ui.treeView.setModel(self._fileSystemModel)

        self.ui.treeView.setColumnWidth(0,999)

        self.ui.treeView.expandAll()


    def ScanFolder2(self,startpath):
        for root, dirs, files in os.walk(startpath):

            self.FilesArray[root]=1

            level = root.replace(startpath, '').count(os.sep)
            subindent = ' ' * 4 * (level + 1)
            for subdir in dirs:
                print (subindent+subdir)

        print( self.FilesArray )

    def ScanFolder1(self,startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

    def ScanFolderold(self,FolderName):

        print( " ScanFolder: "+FolderName)

        for root, subdirs, files in os.walk(FolderName, followlinks=False):

            #FolderNode=StandardItem(root.split(os.path.sep)[-1])

            #print( "New folder: "+root.split(os.path.sep)[-1])

            #for filename in files:

                #print( "  File: "+filename)

                #file_path = os.path.join(root, filename)

                #FileNode=StandardItem(filename)

                #FolderNode.appendRow(FileNode)

            for subdir in subdirs:

                print( "Processing subdir: "+subdir)

                self.ScanFolder( FolderName +os.path.sep+ subdir )



            #ObjectNode.appendRow(FolderNode)

        print( " Finished Scanfolder")


    def lineEditTextChanged_OLD(self):
        logmessage("OpenFile:lineEdit TextChanged")
        newvalue=self.ui.lineEdit.text()
        logmessage(newvalue)

    def lineEditTextChanged(self):
        #print("OpenFile:lineEdit TextChanged")
        newvalue=self.ui.lineEdit.text()

        startpath=SongPreferences['SONGDIR']+"/"

        file_list=[]
        for root, subdirs, files in os.walk(startpath, followlinks=False):

            for file in files:

                if ( ".xml" in file):
                    if (newvalue.upper() in file.upper() or grep(startpath+file,newvalue) ): 
                        file_list.append(root+os.path.sep+file)

        self._fileSystemModel = FileSystemModelLite(file_list, startpath, self)

        self.ui.treeView.setModel(self._fileSystemModel)

        
    def eventFilter(self, obj, event):

        logmessage("OpenFile:eventFilter")

        if obj == self.ui.treeView:
            if  event.type() == QtCore.QEvent.KeyPress:
                # print("Keypress: "+str(event.key()))
                if event.key() == QtCore.Qt.Key_Up:
                    logmessage("OpenFile:KeyUp")
                    print("Up")
                    SelectedFile=FileSystemModelLite.fullpath(self,self.ui.treeView.indexAbove(self.ui.treeView.selectedIndexes()[0]))
                    #SelectedFile=self.model.filePath(self.ui.treeView.indexAbove(self.ui.treeView.selectedIndexes()[0]))
                    self.SelectFile(SelectedFile)
                if event.key() == QtCore.Qt.Key_Down:
                    logmessage("OpenFile:KeyDown")
                    print("Down")
                    SelectedFile=FileSystemModelLite.fullpath(self,self.ui.treeView.indexBelow(self.ui.treeView.selectedIndexes()[0]))
                    #SelectedFile=self.model.filePath(self.ui.treeView.indexBelow(self.ui.treeView.selectedIndexes()[0]))
                    self.SelectFile(SelectedFile)
                if event.key() == QtCore.Qt.Key_Return:
                    logmessage("OpenFile:KeyEnter")
                    print("enter pressed")
                    file_path=FileSystemModelLite.fullpath(self,self.ui.treeView.currentIndex())
                    short_path=file_path.replace(SongPreferences['SONGDIR']+"/",'')
                    self.ui.lineEdit.setText(short_path)
                    self.accept()

        return super(OpenFile, self).eventFilter(obj, event)


    def DoubleClickedTree(self, signal):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("OpenFile:DoubleClickTree")

        print('Double click')

        file_path=''
        # file_path=self.ui.treeView.model().filePath(signal)
        file_path=FileSystemModelLite.fullpath(self,self.ui.treeView.currentIndex())

        short_path=file_path.replace(SongPreferences['SONGDIR']+"/",'')

        self.ui.lineEdit.setText(short_path)

        self.accept()

    def clickedTree(self, signal):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("OpenFile:ClickTree")

        file_path=''
        # file_path=self.ui.treeView.model().filePath(signal)
        #file_path=FileSystemModelLite.data(self,self.ui.treeView.currentIndex())
        file_path=FileSystemModelLite.fullpath(self,self.ui.treeView.currentIndex())

        self.SelectFile(file_path)
        # self.SelectFile(SongPreferences['SONGDIR']+"/"+file_path)


    def SelectFile(self,FilePath):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("OpenFile:SelectFile")

        try:

            short_path=FilePath.replace(SongPreferences['SONGDIR']+"/",'')

            #self.ui.lineEdit.setText(short_path)
            print(FilePath)

            print("reading file...")

            with open(FilePath, 'r') as myfile:
                    LoadSongData = myfile.read()

            print("getting data")

            Datatree = ET.ElementTree(ET.fromstring(LoadSongData))

            #   Interpret the XML into the main data structure
            print("getting lyrics")

            LoadSongLyrics = list(Datatree.iter('lyrics'))

            SongTextHeader = """<html>
                <head>
                <style>
                body { 
                    background-color: #FFFFFF;
                    padding-top : 1em;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 30px; margin: 0px; 
                    } 
                p {
                  padding-top : 1em; 
                  font-family: Arial, Helvetica, sans-serif;  
                  font-size: 30px; margin: 0px; 
                }
                p.heading {
                  padding-top : 0; 
                  font-family: Arial, Helvetica, sans-serif;
                  color: red;
                  margin: 0px;
                  font-size: 30px;
                }
                p.nochords {
                  padding-top : 0;  
                  font-family: Arial, Helvetica, sans-serif; 
                  margin: 0px;
                  font-size: 30px; 
                }
                p.onlychords {
                  padding-top : 0;  
                  font-family: Arial, Helvetica, sans-serif; 
                  margin: 0px;
                  font-weight: bold;
                  font-style: italic;
                  color: blue;
                  font-size: 30px; 
                }

                em {
                    font-style: normal;
                }

                em[data-chord]:before {
                    position: relative;
                    top: -1em;
                    display: inline-block;
                    content: attr(data-chord);
                    width: 0;
                    font-weight: bold;
                    font-style: italic;
                    color: blue;
                    font-family: Arial, Helvetica, sans-serif;
                    speak: literal-punctuation;
                    pause: 1s;
                    /* pause between chord and text */
                }

                table {
                    padding: 0;
                    border: 1px solid black;
                }
                tr {
                    padding: 0;
                }
                td {
                    vertical-align: top;
                }

                </style>
                </head>
                <body>"""

            #SongTextHeader = "<html><head>"
            #SongTextHeader = SongTextHeader + "<style>"
            #SongTextHeader = SongTextHeader + "body { background-color: #555555;font-size: 32px;} "

            #SongTextHeader = SongTextHeader + "p { font-size: 25px; margin: 0px;} "
            #SongTextHeader = SongTextHeader + "table { width: 100%; border: 2px solid black; padding 20px;} "
            #SongTextHeader = SongTextHeader + "tr { width: 100%; border: 2px solid black; padding 20px;} "
            #SongTextHeader = SongTextHeader + "td { border: 2px solid black; padding 5px; background-color: #eeeeee;} "
            #SongTextHeader = SongTextHeader + "</style>"
            #SongTextHeader = SongTextHeader + "</head>"
            #SongTextHeader = SongTextHeader + "<body>"


            OutputSongText = "<table><tr><td style='padding:10px'>"

            LoadSongText=LoadSongLyrics[0].text

            KeyData = Datatree.find('key')

            if KeyData is None:
                SongKeyValue = 'C'
            else:
                SongKey = KeyData.text
                if SongKey == '':
                    SongKeyValue = 'C'
                else:
                    SongKeyValue = SongKey

            OutputText=Derive_Song_Text( "YES", LoadSongText, SongKeyValue, 0,SongPreferences['DEFAULTPAGESIZE'],'L')

            #LoadSongText = LoadSongText.replace('\n.','<br> ').replace('\n ','</br> ').replace(' ','&nbsp;')
            # space in the TD STYLE has been mucked up by the global replace - undo it.
            #LoadSongText = LoadSongText.replace('<td&nbsp;style','<td style')
            #LoadSongText = LoadSongText.replace('[','<b><font color=''red''>[').replace(']',']</font></b>')

            SongLyricsDisplay = OutputSongText + OutputText

            SongLyricsDisplay = SongTextHeader + SongLyricsDisplay + '</td></tr></table></body></html>'

            #print("SONGTEXT---------------------------------------------------------")
            #print(SongLyricsDisplay)
            #print("SONGTEXT---------------------------------------------------------")

            # self.ui.textBrowser.setText(SongLyricsDisplay)
            self.ui.textBrowser.setHtml(SongLyricsDisplay)

        except:

            # self.ui.textBrowser.setText("<html><body>Error interpreting file</body></html>")
            self.ui.textBrowser.setHtml("<html><body>Error interpreting file</body></html>")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            outstring=print_to_string(exc_type, fname, exc_tb.tb_lineno)
            logmessage(outstring)

#   Initialisation of Edit Window
class EditWindow(QDialog):
    FullSongPath=''
    def __init__(self,SongData):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        LocalSongText=SongData[1]
        print("LocalSongText")
        print(LocalSongText)

        logmessage("EditWindow:Init")

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #   Copy variable values for single song into on-screen fields.
        self.FullSongPath=SongData[0]
        self.ui.FName.setText(SongData[4])

        SongText=SongData[1]
        SongKey=SongData[2]
        SongOffset = SongData[3]
        logmessage("EditWindow:Init:SongText")
        logmessage(LocalSongText)

        if SongPreferences['EDIT_USE_ORIGINALKEY'] == 'ORIGINALKEY':
            logmessage("EditWindow:Init:UseOriginalKey")
            print("Use original key")
            print(LocalSongText)
            #SongText.replace("/n","<br>")
            self.ui.EditingSongText.setPlainText(LocalSongText)
            self.ui.SongKey.setCurrentText(SongKey)
        else:
            logmessage("EditWindow:Init:DontUseOriginalKey")
            ModifiedSongText=Derive_Song_Text( "NO", LocalSongText, SongKey, SongOffset,SongPreferences['DEFAULTPAGESIZE'],'L')
            #ModifiedSongText.replace("/n","<br>")
            ActualSongKey = Derive_Actual_Song_Key(SongKey, SongOffset)
            logmessage("EditWindow:Init:ModifiedSongText")
            logmessage(ModifiedSongText)
            print(ModifiedSongText)
            self.ui.EditingSongText.setPlainText(ModifiedSongText)
            self.ui.SongKey.setCurrentText(SongKeys_Alt[ActualSongKey])

        SongFontSize=SongData[5]
        SongFontSize_Portrait=SongData[6]
        SongPageSize=SongData[7]
        SongPageSize_Portrait=SongData[8]
        self.ui.DefaultFontSize.setCurrentText(SongFontSize)
        self.ui.DefaultFontSize_Portrait.setCurrentText(SongFontSize_Portrait)
        self.ui.PageSize.setCurrentText(SongPageSize)
        self.ui.PageSize_Portrait.setCurrentText(SongPageSize_Portrait)

        logmessage("showing edit window")
        #   Set the window up.
        self.show()

#   Initialisation of Preferences Window
class Prefs(QDialog):
    def __init__(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("Prefs:Init")

        super().__init__()
        self.ui = Ui_PrefsEditor()
        self.ui.setupUi(self)

        #   Set up browse button
        self.ui.pushBrowse.clicked.connect(self.BrowseSelected)

        #   Copy variable values into on-screen fields
        self.ui.SongDirectory.setText(SongPreferences['SONGDIR'])

        self.ui.DefaultFontSize.setCurrentText(SongPreferences['DEFAULTFONTSIZE'])
        self.ui.DefaultFontSize_Portrait.setCurrentText(SongPreferences['DEFAULTFONTSIZE_PORTRAIT'])

        self.ui.PageSize.setCurrentText(SongPreferences['DEFAULTPAGESIZE'])
        self.ui.PageSize_Portrait.setCurrentText(SongPreferences['DEFAULTPAGESIZE_PORTRAIT'])

        if SongPreferences['SHARPFLAT_C'] == 'C#':
            self.ui.radioButton_Cs.setChecked(True)
        else:
            self.ui.radioButton_Db.setChecked(True)

        if SongPreferences['SHARPFLAT_D'] == 'D#':
            self.ui.radioButton_Ds.setChecked(True)
        else:
            self.ui.radioButton_Eb.setChecked(True)

        if SongPreferences['SHARPFLAT_F'] == 'F#':
            self.ui.radioButton_Fs.setChecked(True)
        else:
            self.ui.radioButton_Gb.setChecked(True)

        if SongPreferences['SHARPFLAT_G'] == 'G#':
            self.ui.radioButton_Gs.setChecked(True)
        else:
            self.ui.radioButton_Ab.setChecked(True)

        if SongPreferences['SHARPFLAT_A'] == 'A#':
            self.ui.radioButton_As.setChecked(True)
        else:
            self.ui.radioButton_Bb.setChecked(True)

        #   0.5 - 20210402 - add edit using original key or transposed...
        if SongPreferences['EDIT_USE_ORIGINALKEY'] == 'ORIGINALKEY':
            self.ui.EditOriginalKey.setChecked(True)
        else:
            self.ui.EditTransposedKey.setChecked(True)

        if SongPreferences['PRODUCE_LOG_FILES']==1 :
            self.ui.ProduceLogFiles.setChecked(True)
        else:
            self.ui.ProduceLogFiles.setChecked(False)
            
        #   Set the window up
        self.show()

    #   Browse to locate song directory.
    def BrowseSelected(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("Prefs:BrowseSelected")

        try:

            CurrentDir = self.ui.SongDirectory.text()
            DirLoc=QFileDialog.getExistingDirectory(self, "Select Directory", CurrentDir)

            if len(DirLoc) > 1:
                self.ui.SongDirectory.setText(DirLoc)
        except:
            print('Error in selecting preferences?')
            logmessage("Error in selecting preferences?")



#   *****************************************************************************
#   Support routines - used by multiple windows.

#   Given a base key, and an offset, work out the actual key and return that number
def Derive_Actual_Song_Key(SongBaseKey, SongOffset):
    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

    logmessage("Derive_ActualSongKey")

    # Work out the actual key
    # i.e. the original key + the offset
    Ptr3 = 0

    ActualSongKey = -1

    # Bugfix: 20210401: When 'B' wasn't locating the songkey. - updated from 11 to 12...
    while Ptr3 < 12 and ActualSongKey == -1:
        if SongKeys[Ptr3] == SongBaseKey or SongKeys_Alt[Ptr3] == SongBaseKey:
            ActualSongKey = Ptr3
        Ptr3 += 1

    if ActualSongKey > -1:
        # i.e. the key was found...
        # now add the offset...

        ActualSongKey = ActualSongKey + SongOffset

        # wrap around if necessary...
        if ActualSongKey > 11:
            ActualSongKey = ActualSongKey - 12

    logmessage("Derive_ActualSongKey:Input:"+SongBaseKey+" Output:"+str(ActualSongKey))
    return ActualSongKey


#   Given a string which holds a chord, e.g. 'Gbm' , 'C' , 'C#' etc
#   and an offset - return the updated chord string
def ConvertChord(ChordString, Offset):

    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

    logmessage("ConvertChord")
    
    Ptr1 = 0
    TempString = ''
    IsMinor = 0
    while Ptr1 < len(ChordString):
        if ChordString[Ptr1] == 'M':
            IsMinor = 1
        else:
            TempString = TempString+ChordString[Ptr1]
        Ptr1 = Ptr1+1

    if len(TempString) > 2:
        print("Weird?")

    Ptr3 = 0

    ActualSongKey = -1

    while Ptr3 < 11 and ActualSongKey == -1:
        if SongKeys[Ptr3] == TempString or SongKeys_Alt[Ptr3] == TempString:
            ActualSongKey = Ptr3
        Ptr3 += 1

    ActualSongKey = ActualSongKey+Offset

    if ActualSongKey > 11:
        ActualSongKey = ActualSongKey-12
        # print("Chordstring:" + ChordString + " Offset:" + str(Offset) + " Final:" + self.SongKeys[ActualSongKey])

    OutputString = SongKeys_Alt[ActualSongKey]
    if IsMinor == 1:
        OutputString = OutputString+"m"

    if SongPreferences['SHARPFLAT_C'] == 'C#':
        OutputString = OutputString.replace('Db', 'C#')
    if SongPreferences['SHARPFLAT_C'] == 'Db':
        OutputString = OutputString.replace('C#', 'Db')

    if SongPreferences['SHARPFLAT_D'] == 'D#':
        OutputString = OutputString.replace('Eb', 'D#')
    if SongPreferences['SHARPFLAT_D'] == 'Eb':
        OutputString = OutputString.replace('D#', 'Eb')

    if SongPreferences['SHARPFLAT_F'] == 'F#':
        OutputString = OutputString.replace('Gb', 'F#')
    if SongPreferences['SHARPFLAT_F'] == 'Gb':
        OutputString = OutputString.replace('F#', 'Gb')

    if SongPreferences['SHARPFLAT_G'] == 'G#':
        OutputString = OutputString.replace('Ab', 'G#')
    if SongPreferences['SHARPFLAT_G'] == 'Ab':
        OutputString = OutputString.replace('G#', 'Ab')

    if SongPreferences['SHARPFLAT_A'] == 'A#':
        OutputString = OutputString.replace('Bb', 'A#')
    if SongPreferences['SHARPFLAT_A'] == 'Bb':
        OutputString = OutputString.replace('A#', 'Bb')


    return OutputString



#   Process an individual line of music chords - i.e. must begin with '.'

def ProcessMusicLine(InputText,SongOffset):

    logmessage("ProcessMusicLine")

    #   Line begins with '.' - it contains chords - need to work through letter by letter

    Ptr3 = 0  # pointer into the text line
    OutputLine = ''  # converted line

    # Create a temp line with extra spaces at the end - so we don't read past the end of line.
    TempLine = InputText + "   "

    while Ptr3 < len(InputText):

        NewValue = ord(InputText[Ptr3])

        if 65 <= NewValue <= 71:
            # This is a key value

            # Get the chord
            NewString = InputText[Ptr3]

            # Check: is this a minor or sharp?
            if (TempLine[Ptr3 + 1] == 'M') or (TempLine[Ptr3 + 1] == '#') or (TempLine[Ptr3 + 1] == 'b'):
                NewString = NewString + InputText[Ptr3 + 1]
                Ptr3 = Ptr3 + 1
                # Check: is this a minor or sharp?
                if (TempLine[Ptr3 + 1] == 'M') or (TempLine[Ptr3 + 1] == '#') or (TempLine[Ptr3 + 1] == 'b'):
                    NewString = NewString + InputText[Ptr3 + 1]
                    Ptr3 = Ptr3 + 1

            # NewString now contains the chord - convert it...
            UpdatedChord = ConvertChord(NewString, SongOffset)

            OutputLine = OutputLine + UpdatedChord

        else:
            OutputLine = OutputLine + InputText[Ptr3]

        Ptr3 = Ptr3 + 1

    logmessage("ProcessMusicLine:Output:"+OutputLine)
    return OutputLine





#   Given the song text, and offset data, work out the updated song text with key change
#   also, have the option to output in HTML format or non HTML
#   HTML format is used to display a song on-screen, but non-HTML is used
#   if we want to edit, but use the transposed key (as we need to use plain text)

def Derive_Song_Text( HTML_Needed, SongText, SongKey, SongOffset, PageSize, Orientation):
    if (HTML_Needed=="YES"):
        ReturnString=Derive_Song_Text_HTML( HTML_Needed, SongText, SongKey, SongOffset, PageSize, Orientation)
    else:
        ReturnString=Derive_Song_Text_Plain( HTML_Needed, SongText, SongKey, SongOffset, PageSize, Orientation)

    return ReturnString



def Derive_Song_Text_Plain( HTML_Needed, SongText, SongKey, SongOffset, PageSize, Orientation):
    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

    try:

        logmessage("Derive_Song_Text_Plain")

        ReturnString=""

        #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
        #   First, split the string on newlines.

        SongTextLines = SongText.split('\n')

        #   Now, go through the lines...

        Ptr2 = 0

        SongTextLineNumber = 0
        MusicChordsLine=""

        # Work through all the lines of text
        while Ptr2 < (len(SongTextLines)):

            # Put the line we're working with into a working variable
            TextLine = SongTextLines[Ptr2]

            print( SongTextLines[Ptr2])

            # If its not a blank line
            if len(TextLine) > 0:

                # is it a command line?
                if TextLine[0] == '.':

                    OutputLine=ProcessMusicLine(TextLine,SongOffset)

                else:
                    OutputLine = TextLine
            else:
                # its a blank line
                OutputLine = ''

            TextLine = OutputLine

            if (ReturnString==""):
                ReturnString = TextLine
            else:
                ReturnString = ReturnString +"\n"+ TextLine

            Ptr2 = Ptr2 + 1
            SongTextLineNumber = SongTextLineNumber + 1

        logmessage("Derive_Song_Text_Plain:Return:")
        logmessage(ReturnString)

        return ReturnString

    except:

        print("Error interpeting file")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        outstring=print_to_string(exc_type, fname, exc_tb.tb_lineno)
        logmessage(outstring)


def Derive_Song_Text_HTML( HTML_Needed, SongText, SongKey, SongOffset, PageSize, Orientation):
    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

    try:

        logmessage("Derive_Song_Text")

        ReturnString=""

        #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
        #   First, split the string on newlines.

        SongTextLinesRaw = SongText.split('\n')
        SongTextLines=[]

        # Pre-process - we'll go through the SongTextLinesRaw array, and merge 
        # chord lines with the lyric lines

        OuputLineNumber=0
        Ptr2=0

        while (Ptr2 < len(SongTextLinesRaw)):

            TextLine = SongTextLinesRaw[Ptr2]+" "
            if (Ptr2+1 < len(SongTextLinesRaw)):
                TextLine2= SongTextLinesRaw[Ptr2+1]
            else:
                TextLine2=""

            # is this a music line and there's a lyric line next 
            if len(TextLine2)>0 :
                if ( TextLine[0] == "." and TextLine2[0] == " " ):
                    # ok we've got a chord line followed by a lyric line

                    # Before we merge - we need to do any transposing...
                    TextLine=ProcessMusicLine(TextLine,SongOffset)

                    # Now, merge the two lines:
                    # e.g.
                    # .    G      Asus
                    #   Hello there how are you
                    # becomes
                    #   Hel<em>G</e>lo ther<em>Asus</em>e how are you

                    # we'll need to work right to left to preserve the positioning in both strings.

                    # Create string 1 and string2, each same length, padded with spaces.
                    String1=TextLine + ( " " *500 )
                    String2=TextLine2 + ( " " *500 )

                    # Make the same length
                    String1=String1[:490]
                    String2=String2[:490]

                    # now work backward through string 1 (chords), locating text

                    Ptr3=len(String1)-1

                    while (Ptr3 > 0):
                        
                        if ( String1[Ptr3] != " "):
                            # got a non-space - i.e. a chord - however, it can be multiple characters
                            # start to work backward from here...
                            Ptr4=Ptr3
                            while ( String1 [Ptr4] != " " and Ptr4 > 0):
                                Ptr4=Ptr4-1

                            # Ptr3 is the end of the string, Ptr4 is the start
                            # also Ptr4 is the location in String2 to perform the merge

                            Chord=String1[Ptr4+1:Ptr3+1]

                            # Now do the insert into String2

                            String2=String2[:Ptr4+1]+"<em data-chord='"+Chord+"'></em>"+String2[Ptr4+1:]

                            # Now carry on from Ptr4

                            Ptr3=Ptr4

                        Ptr3 = Ptr3 -1

                    # Finish - String2 now contains the merged lines
                    TextLine="<p>"+String2.strip()+"</p>"
                    # As we've dealt with the next line in the input text, bump that pointer too..
                    Ptr2 = Ptr2 +1

                else:
                    if ( TextLine[0] == "." ):
                        # ok - we've got a chord line, but the next line isn't for merging
                        # so make it a 'p.onlychords' line
                        # do any transposing first..
                        TextLine=ProcessMusicLine(TextLine,SongOffset)
                        TextLine="<p class='onlychords'>"+TextLine[1:]+"</p>"
                    else:
                        if ( len(TextLine.strip()) == 0):
                            # its a blank line
                            TextLine="<br>"
                        else:
                            if ( TextLine.strip()[0] == "["):
                                # its a command
                                # if (TextLine.strip()=="[===]") or (TextLine.strip()=="[=L=]" and Orientation=='L') or (TextLine.strip()=="[=P=]" and Orientation=='P'):
                                if (TextLine.strip()=="[===]") or TextLine.strip()=="[=L=]"  or TextLine.strip()=="[=P=]":
                                    # Page break requested - check if we're landscape or portrait:
                                    if (TextLine.strip()=="[===]") or (TextLine.strip()=="[=L=]" and Orientation=='L') or (TextLine.strip()=="[=P=]" and Orientation=='P'):
                                        TextLine = "</td><td>"
                                    else:
                                        TextLine =""
                                else:
                                    TextLine = "<p class='heading'>"+TextLine+"</p>"
                            else:
                                # so this is a basic line - no merging - use p.nochords

                                TextLine="<p class='nochords'>"+TextLine[1:]+"</p>"
            else:
                # Ok - we've got a line, but with nothing following
                if ( TextLine[0] == "." ):
                    # ok - we've got a chord line, but the next line isn't for merging
                    # so make it a 'p.onlychords' line
                    # do any transposing first..
                    TextLine=ProcessMusicLine(TextLine,SongOffset)
                    TextLine="<p class='onlychords'>"+TextLine[1:]+"</p>"
                else:
                    if ( len(TextLine.strip()) == 0):
                        # its a blank line
                        TextLine="<br>"
                    else:
                        if ( TextLine.strip()[0] == "["):
                            # its a command
                            if TextLine.strip()=="[===]" or TextLine.strip()=="[=L=]" or TextLine.strip()=="[=P=]":
                                # Page break requested
                                if (TextLine.strip()=="[===]") or (TextLine.strip()=="[=L=]" and Orientation=='L') or (TextLine.strip()=="[=P=]" and Orientation=='P'):
                                    TextLine = "</td><td>"
                                else:
                                    TextLine =""
                            else:
                                TextLine = "<p class='heading'>"+TextLine+"</p>"
                        else:
                            # so this is a basic line - no merging - use p.nochords

                            TextLine="<p class='nochords'>"+TextLine[1:]+"</p>"                    

            # Last stage
            # Its possible that there's spaces in the text, however, we can't just replace
            # all spaces with &nbsp; 's - it'll break html tags - we'll have to work our way through it.

            TextLine=TextLine.strip()
            OutputText=""

            OutPtr=0
            InsideTag=0
            while ( OutPtr < len(TextLine)):
                if (TextLine[OutPtr]=="<"):
                    InsideTag=1
                if (TextLine[OutPtr]==">"):
                    InsideTag=0

                if (TextLine[OutPtr]==" " and InsideTag==0):
                    OutputText=OutputText+"&nbsp;"
                else:
                    OutputText=OutputText+TextLine[OutPtr]

                OutPtr=OutPtr+1


            # Add the finished lines to the output array...
            SongTextLines.append(OutputText)
            ReturnString=ReturnString+OutputText
            OuputLineNumber=OuputLineNumber+1

            if (OuputLineNumber>int(PageSize)):
                SongTextLines.append("</td><td>")

            Ptr2=Ptr2+1

        #   Now, go through the lines...

        logmessage("Derive_Song_Text_HTML:Return:")
        logmessage(ReturnString)

        return ReturnString

    except:

        print("Error interpeting file")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        outstring=print_to_string(exc_type, fname, exc_tb.tb_lineno)
        logmessage(outstring)
        

def oldcode(self):
        Ptr2 = 0

        SongTextLineNumber = 0

        # Work through all the lines of text
        while Ptr2 < (len(SongTextLines)):

            # Put the line we're working with into a working variable
            TextLine = SongTextLines[Ptr2]

            print( SongTextLines[Ptr2])

            # If its not a blank line
            if len(TextLine) > 0:

                OutputLine = TextLine.strip()
            else:
                # its a blank line
                OutputLine = ' '

            # Finally, remove any column break markers
            if (OutputLine.strip()=="[===]") or (OutputLine.strip()=="[=L=]" and Orientation=='L') or (OutputLine.strip()=="[=P=]" and Orientation=='P'):
                # Page break requested
                SongTextLineNumber = 1
                TextLine = "</td><td style='padding:10px'>"
            else:
                if (OutputLine.strip()=="[=L=]") or (OutputLine.strip()=="[=P=]"):
                    # Skip this line - its a Landscape/Portrait page break that hasn't been actioned.
                    TextLine=""
                else:
                    # If we're too far down, go to another display column
                    if SongTextLineNumber >= int(PageSize):
                        SongTextLineNumber = 1
                        # TextLine = "</td><td style='padding:10px'><p>" + OutputLine + "</p>"
                        TextLine = "</td><td style='padding:10px'>" + OutputLine # + "<br>"
                    else:
                        # Ok - its text to output...
                        # is it a heading e.g. [Intro] etc (begins with [)
                        if ( len (OutputLine.strip()) > 0):
                            if (OutputLine.strip()[0] =="["):
                                TextLine = "<p class='heading'>" + OutputLine + "</p>"
                            else:
                                # TextLine = "<p>" + OutputLine + "&nbsp;</p>"
                                TextLine = "<p>"+OutputLine+"</p>"  # + "<br>"

            ReturnString = ReturnString + TextLine

            Ptr2 = Ptr2 + 1
            SongTextLineNumber = SongTextLineNumber + 1


        # Final check: if its got [ ] set it to red
        #              replace newlines with breaks and spaces with nbsp
        ReturnString = ReturnString.replace('\n','<br>')   # .replace(' ','&nbsp;')
        #ReturnString = ReturnString.replace('\n.','<br> ').replace('\n ','</br> ').replace(' ','&nbsp;')
        # space in the TD STYLE has been mucked up by the global replace - undo it.
        ReturnString = ReturnString.replace('<td&nbsp;style','<td style')
        ReturnString = ReturnString.replace('[','<b><font color=''red''>[').replace(']',']</font></b>')



#   *****************************************************************************
#   Main UI window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    CurrentSong = ''
    CurrentSongKey = ''
    CurrentOffset = 0
    CurrentFontSize = ''

    # Directory that holds the song files - picked up from preferences
    SongLocation = ''

    # Directory holding this program
    HomeDirectory=''
    # Location and name of preferences file - this is held in the same directory as the program
    SongPreferencesFileName = ''

    #   Default songlist file name - we save after change (transpose etc)
    SaveFileName = 'SongData.json'

    #   Window Orientation - (L)andscape or (P)ortrait
    WindowOrientation='L'

    def __init__(self, parent=None):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:Init")

        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        self.resize(self.width-50,self.height-50)

        self.frame_8.setMaximumHeight(0)

        # self.WindowResized

        #   Set up song list (left hand side of screen)
        self.SongListModel = QStandardItemModel()
        self.SongList.setModel(self.SongListModel)

        # Work out the directory where the python/executable lives - preferences are within this dir.
        self.HomeDirectory = os.getcwd()
        self.SongPreferencesFileName = self.HomeDirectory+'\\OpenSongViewerPrefs.json'

        IntroText =  """ <html>
        <head>
        <style>
        body { 
            background-color: #FFFFFF;
            font-family: Verdana, Arial, Helvetica, sans-serif;
            font-size: 25pt;
            text-align: justify;
            color: black
            } 
        P {
            font-family: Verdana, Arial, Helvetica, sans-serif;
            font-size: 25pt;
            text-align: justify;
            color: black
            }
        em { 
            font-style  : normal; 
        }
        em[data-chord]:before {
            position    : relative;
            top         : -1em;
            display     : inline-block;
            content     : attr(data-chord);
            width       : 0;
            font-weight : bold;
            font-style  : italic;
            speak       : literal-punctuation;
            pause       : 1s; /* pause between chord and text */
        }
        </style>
        </head>
        <body>

        Hello there<br><br>
        <i>OpenSongViewer version """

        IntroText = IntroText +VersionInformation+"</i><br><br>"

        IntroText = IntroText +"""Remember to set the location of your OpenSong songs in the preferences<br><br>

        Click on <br>
         * Add - to add a song to the song list<br>
         * Rem - to remove the current selected song to the song list<br>
         * Edit - to edit the current selected song to the song list<br><br>

        Remember to save your song list using 'Song List' -> 'Save As...' - it'll retain order and keys<br>
        Remember to check your current preferences under the file menu<br>
        <br>

        Changelog:<br>
        <br>
        0.91 - Use of CSS to use proportional fonts<br>
         * Added 'produce diagnostic log files' to preferences.<br>
        <br>

        0.9a - use up and down keys in the search screen with enter to select<br>
        <br>

        0.9 - Song open and search updates<br>
         * Improved the ability to search for songs when adding songs to the list<br> 
           When the open dialog opens, you can just start typing, and it will filter the<br> 
           list - if the song name, or the contents of the file matches the text <br> 
        <br>

        0.8 - Save songlist structure updates<br>
         * Noted an issue - the song text is saved with the song list so you can potentially overwrite an updated song<br> 
           if you edit an old song list. So, now songlists only save the list of songs, and also the keys - when loading <br> 
           the song text is re-loaded from the song files.<br> 
        <b><font color='red'>WARNING</font></b> - This is NOT compatible with old saved song lists<br>
        <br>

        0.7 - General updates<br>
         * Improvement - more efficient use of song text space (remove leading '.' and ' ', and [===] from output text)<br>
         * Improvement - can now set font size for individual song, or select 'Default'<br>
         * Improvement - viewer can now detect and adjust for portrait screens<br>
        &nbsp;                also, pagebreaks for Landscape [=L=] and Portrait [=P=] <br>
        <b><font color='red'>WARNING</font></b> - This is NOT compatible with old saved song lists<br>
         * Improvement - Load song dialog now shows a preview'<br>
        <br>

        Changelog:<br>
        0.5 - bugfix - when transposing and base key was 'B' the value key didn't update<br>
         * Improvement - when you select a song in the songlist, you can now use right and left cursor or arrows under the songlist to move up and down the list<br>
         * Improvement - new preference setting - when editing, you can choose to always edit in the original base key, or edit in the current transposed value<br>
         - NOTE - if you edit in the current transposed value, this will overwrite the original base key<br>
         - this means that chord characters can move slightly when the base key switches from a single to a double character  - e.g. 'C' to 'Db'<br>

        </body>
        </html>"""


        # self.SongText.setText(IntroText)
        self.SongText.setHtml(IntroText)

        # try to pull in the preferences
        try:
            with open(self.SongPreferencesFileName) as f:
                SongPreferences = json.load(f)

        except:
            # none found - set default prefs.
            SongPreferences['PREFSVER'] = '0.5'
            SongPreferences['SONGDIR'] = self.HomeDirectory
            SongPreferences['DEFAULTFONTSIZE'] = '25'
            SongPreferences['DEFAULTFONTSIZE_PORTRAIT'] = '25'
            SongPreferences['DEFAULTPAGESIZE'] = '38'
            SongPreferences['DEFAULTPAGESIZE_PORTRAIT'] = '50'
            SongPreferences['SHARPFLAT_C'] = 'C#'
            SongPreferences['SHARPFLAT_D'] = 'D#'
            SongPreferences['SHARPFLAT_F'] = 'F#'
            SongPreferences['SHARPFLAT_G'] = 'G#'
            SongPreferences['SHARPFLAT_A'] = 'A#'
            SongPreferences['EDIT_USE_ORIGINALKEY'] = 'ORIGINALKEY'
            SongPreferences['PRODUCE_LOG_FILES']=0

        if type(SongPreferences) is list:
            # V0.1 preferences used lists instead of dict - convert and re-save
            print('Old V0.1 preferences file format - upgraded to v0.2')
            OLDPrefs=SongPreferences
            SongPreferences={}
            SongPreferences['PREFSVER'] = '0.2'
            SongPreferences['SONGDIR'] = OLDPrefs[0][1]

            # Overwrite old file
            with open(self.SongPreferencesFileName, 'w') as f:
                json.dump(SongPreferences, f)

        if SongPreferences['PREFSVER'] == '0.2':
            #   Upgrade preferences values - put in default values.
            SongPreferences['PREFSVER'] = '0.3'
            SongPreferences['DEFAULTFONTSIZE'] = '25'
            SongPreferences['SHARPFLAT_C'] = 'C#'
            SongPreferences['SHARPFLAT_D'] = 'D#'
            SongPreferences['SHARPFLAT_F'] = 'F#'
            SongPreferences['SHARPFLAT_G'] = 'G#'
            SongPreferences['SHARPFLAT_A'] = 'A#'

        if SongPreferences['PREFSVER'] == '0.3':
            SongPreferences['PREFSVER'] = '0.4'
            SongPreferences['DEFAULTPAGESIZE'] = '38'

        if SongPreferences['PREFSVER'] == '0.4':
            #   0.5 brings in edit use original key, or use transposed value
            #       normal is to keep the base key
            SongPreferences['PREFSVER'] = '0.5'
            SongPreferences['EDIT_USE_ORIGINALKEY'] = 'ORIGINALKEY'

        if SongPreferences['PREFSVER'] == '0.5':
            #   0.6 brings in Portrait capability
            SongPreferences['PREFSVER'] = '0.6'
            SongPreferences['DEFAULTPAGESIZE_PORTRAIT'] = '50'
            SongPreferences['DEFAULTFONTSIZE_PORTRAIT'] = '25'

        if SongPreferences['PREFSVER'] == '0.6':
            #   0.7 brings in Portrait capability
            SongPreferences['PREFSVER'] = '0.7'
            SongPreferences['DEFAULTPAGESIZE_PORTRAIT'] = '50'
            SongPreferences['DEFAULTFONTSIZE_PORTRAIT'] = '25'

        if SongPreferences['PREFSVER'] == '0.7':
            #   0.8 has no real change
            SongPreferences['PREFSVER'] = '0.8'

        if SongPreferences['PREFSVER'] == '0.8':
            #   0.9 brings in the ability to turn off logfiles
            SongPreferences['PREFSVER'] = '0.9'
            SongPreferences['PRODUCE_LOG_FILES']=0


        print("Songpreferences in place:")
        print(SongPreferences)

        self.InterpretPreferences()

        #   Wire up the buttons
        self.AddSong.clicked.connect(self.AddNewSong)
        self.DeleteSong.clicked.connect(self.DelSelectedSong)
        self.EditSong.clicked.connect(self.EditCurrentSong)

        self.AddSong2.clicked.connect(self.AddNewSong)
        self.DeleteSong2.clicked.connect(self.DelSelectedSong)
        self.EditSong2.clicked.connect(self.EditCurrentSong)

        self.SongList.clicked.connect(self.SongListSelected)

        self.TransposeMinus.clicked.connect(self.TransposeMinusSelected)
        self.TransposePlus.clicked.connect(self.TransposePlusSelected)
        self.TransposeMinus2.clicked.connect(self.TransposeMinusSelected)
        self.TransposePlus2.clicked.connect(self.TransposePlusSelected)

        self.actionClear_List.triggered.connect(self.ClearAll)
        self.actionEdit.triggered.connect(self.EditCurrentSong)
        self.actionNew.triggered.connect(self.NewSong)

        self.actionSave_Song_List.triggered.connect(self.SaveSongList)
        self.actionLoad_Song_List.triggered.connect(self.LoadSongList)
        self.actionSave_Song_List_As.triggered.connect(self.SaveSongListAs)
        self.actionPortrait.triggered.connect(self.SwitchLandscapePortrait)

        self.actionPreferences.triggered.connect(self.UpdatePrefs)
        self.actionAbout.triggered.connect(self.AboutWindow)

        self.NextSong.clicked.connect(self.MoveNextSong)
        self.PrevSong.clicked.connect(self.MovePrevSong)
        self.NextSong2.clicked.connect(self.MoveNextSong)
        self.PrevSong2.clicked.connect(self.MovePrevSong)

        self.desktop.resized.connect(self.WindowResized)


    def WindowResized(self):

        logmessage("MainWindow:WindowResized")

        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        print (self.height)
        print (self.width)

        if ( self.width > self.height ):
            # Normal landscape orientation
            self.WindowOrientation='L'

            self.SetWindowObjectSizes()

        else:
            self.WindowOrientation='P'

            self.SetWindowObjectSizes()

        # As we've changed screen orientation - we need to re-display the song - to re-work out page breaks...
        self.DisplaySong(self.CurrentSong)



    def SetWindowObjectSizes(self):

        logmessage("MainWindow:SetWindowObjectSizes")

        try:

            if ( self.WindowOrientation == 'L' ):
                #self.frame_2.maximumSize=
                self.frame_2.setMaximumWidth(16777215)
                self.frame_4.setMaximumWidth(16777215)
                self.frame_5.setMaximumWidth(16777215)
                self.frame_7.setMaximumWidth(16777215)
                self.splitter.setSizes([400, 10000])
                self.frame_8.setMaximumHeight(0)
                self.actionPortrait.setChecked(False)

            else:
                self.frame_2.setMaximumWidth(0)
                self.frame_4.setMaximumWidth(0)
                self.frame_5.setMaximumWidth(0)
                self.frame_7.setMaximumWidth(0)
                self.splitter.setSizes([0, 10000])
                self.frame_8.setMaximumHeight(75)
                self.actionPortrait.setChecked(True)
        except Exception as e:
            print( "Error: SetWindowObjectSizes")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    #   Do anything based on preferences settings - copy values to variables etc.
    def InterpretPreferences(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:InterpretPreferences")

        # Go through the preferences and set variables.

        self.SongLocation = SongPreferences['SONGDIR']

    #   General routine to ask a query on screen
    def AskQuery(self,QueryTitle,QueryText):

        logmessage("MainWindow:AskQuery")

        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if resp == 16384:
            return "YES"
        else:
            return "NO"

    #   General routine to ask a query on screen
    def OkMessage(self,QueryTitle,QueryText):

        logmessage("MainWindow:OkMessage")
        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Ok, QMessageBox.Ok)


    #   Save the current song list, but specify a location.
    def SaveSongListAs(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:SaveSongListAs")

        # Set the new default file name for songs.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        SaveFile = QFileDialog.getSaveFileName(self, 'Save Song List As',self.SongLocation)

        # Get the file name
        Fname=SaveFile[0]

        # Linux / windows
        if os.sep == '\\':
            Fname = Fname.replace('/', '\\')

        # set the new default file name for songs
        self.SaveFileName = Fname

        # and save the songlist
        self.SaveSongList()

    def SwitchLandscapePortrait(self):

        logmessage("MainWindow:SwitchLandscapePortrait")

        # Manual switch between landscape and portrait

        if self.actionPortrait.isChecked():
            
            self.WindowOrientation='P'
            self.SetWindowObjectSizes()

        else:

            self.WindowOrientation='L'
            self.SetWindowObjectSizes()

    def NavigateSong(self,Direction):
        #   Improvement 20210401
        #   Click in the Main SongList - you can then use right and left keys to
        #   move through the songs instead of having to click on specific songs
        #   its slightly more efficient when playing live...

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:NavigateSong")

        #   Get the total rows in the list, so we can wrap around
        TotalRows=self.SongListModel.rowCount()
        #   And the current song
        CurrentSelected=self.SongList.currentIndex().row()

        if Direction == "DOWN":
            NewSelected = CurrentSelected + 1
            print("Next song")
        else:
            NewSelected = CurrentSelected - 1
            print("Previous song")

        #   We only want to do stuff if there's a list there...
        if TotalRows>0:

            #   Do we need to wrap around?
            if NewSelected<0:
                NewSelected=TotalRows-1
            if NewSelected>=TotalRows:
                NewSelected=0

            # print("Total:"+str(TotalRows)+" Current:"+str(CurrentSelected)+" New:"+str(NewSelected))

            #   Set the updated selection value
            index = self.SongListModel.index(NewSelected, 0, QModelIndex())
            self.SongList.setCurrentIndex(index)

            #   To display the song, we need the song title, so get it from the list...
            SongTitle=self.SongListModel.index(NewSelected, 0).data()

            #   and display the updated song.
            self.DisplaySong(SongTitle)



    def MoveNextSong(self):

        logmessage("MainWindow:MoveNextSong")
        self.NavigateSong("DOWN")

    def MovePrevSong(self):
        logmessage("MainWindow:MovePrevSong")
        self.NavigateSong("UP")

    def keyPressEvent(self, event):

        #   Improvement 20210401
        #   Click in the Main SongList - you can then use right and left keys to
        #   move through the songs instead of having to click on specific songs
        #   its slightly more efficient when playing live...

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:keyPressEvent")

        #   Get the total rows in the list, so we can wrap around
        TotalRows=self.SongListModel.rowCount()
        #   And the current song
        CurrentSelected=self.SongList.currentIndex().row()
        #   Use -1 as 'no movement'
        NewSelected=-1

        #   If we press right or left, capture it and set NewSelected
        if event.key() == Qt.Key_Right:
            print("Right pressed")
            self.NavigateSong("DOWN")
        if event.key() == Qt.Key_Left:
            print("Left pressed")
            self.NavigateSong("UP")



    #   Save the song list to the current default file name
    def SaveSongList(self):
        # Take the current songdata and save this to a file e.g. 'SongData.json'
        # 16/7/23 - updated - we now save the song list as a separate structure - i.e.
        #                     song name, and song key.
        #                     when we reload a song list, we only have the song file name
        #                     we then need to re-load the song file from disk - which 
        #                     means we get the up to date version.

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:SaveSongList")

        #   we'll create a special data structure to hold the song list, and then we'll do a JSON.DUMP 
        #   of that structure.

        #   Create blank structure
        SaveSongDataList = []

        #   and fill it.

        P1=0

        while P1 < self.SongListModel.rowCount():

            #   get the song title from the list...
            SongTitle=self.SongListModel.index(P1, 0).data()

            SongPtr=self.LocateSong(SongTitle)

            SongFile=SongDataList[SongPtr][0]
            SongKey=SongDataList[SongPtr][3]

            logmessage("MainWindow:SaveSongList:Construct:"+SongFile)

            TmpSongRecord = ['a',0]

            TmpSongRecord[0] = SongFile
            TmpSongRecord[1] = SongKey

            SaveSongDataList.append(TmpSongRecord)

            P1=P1+1

        try:
            SaveFileName = self.SaveFileName
            with open(SaveFileName,'w') as f:
                json.dump(SaveSongDataList,f)
            logmessage("MainWindow:SaveSongList:Saved")
        except:
            self.OkMessage('Save error','Unable to save song list',sys.exc_info()[0])
            logmessage("MainWindow:SaveSongList:Error?")


        print("Saved updated song list "+SaveFileName)



    #   Save the song list to the current default file name
    def SaveSongListOLD(self):
        # Take the current songdata and save this to a file e.g. 'SongData.json'

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:SaveSongListOLD")

        try:
            SaveFileName = self.SaveFileName
            with open(SaveFileName,'w') as f:
                json.dump(SongDataList,f)
        except:
            self.OkMessage('Save error','Unable to save song list',sys.exc_info()[0])


        print("Saved updated song list "+SaveFileName)


    #   Load a song list
    def LoadSongList(self):
        # Identify and load songdata, then update the screen.

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:LoadSongList")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        if fileName and len(fileName[0]) > 0:

            # When loading, clear the previous song list.
            self.SongListModel.clear()
            SongDataList = []

            #   If Windows, change the separator
            FName = fileName[0]
            if os.sep == '\\':
                FName = FName.replace('/', '\\')

            # Set the default from now on...
            self.SaveFileName = FName

            # Now, open then file and read the JSON data.

            with open(FName) as f:
                SaveSongDataList = json.load(f)

            P1=0

            while P1 < len(SaveSongDataList):

                SongFileName=SaveSongDataList[P1][0]
                SongKeyOffset=SaveSongDataList[P1][1]
                logmessage("MainWindow:LoadSongList:Load:"+SongFileName)
                self.LoadSongTitle(SongFileName,SongKeyOffset)

                P1=P1+1

            # now re-display
            self.DisplaySong(SongDataList[0][4])



    #   Load a song list
    def LoadSongListOLD(self):
        # Identify and load songdata, then update the screen.

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:LoadSongListOLD")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        if fileName and len(fileName[0]) > 0:

            #   If Windows, change the separator
            FName = fileName[0]
            if os.sep == '\\':
                FName = FName.replace('/', '\\')

            # Set the default from now on...
            self.SaveFileName = FName

            # Now, open then file and read the JSON data.

            with open(FName) as f:
                SongDataList = json.load(f)

            # Clear out and populate the song list panel.

            self.SongListModel.clear()

            # Add the files to the on-screen list
            Ptr = 0

            try:
                while Ptr < len(SongDataList):
                    FName = SongDataList[Ptr][4]
                    FontSize=SongDataList[Ptr][5]
                    FontSize_Portrait=SongDataList[Ptr][6]
                    PageSize=SongDataList[Ptr][7]
                    PageSize_Portrait=SongDataList[Ptr][8]
                    item = QStandardItem(FName)
                    self.SongListModel.appendRow(item)
                    Ptr = Ptr+1
            except:
                self.OkMessage('Load error','Song list file is not compatible with this version - sorry')
                self.SongListModel.clear()


    #   Given a song name, find the location within the main song array and return the number
    def LocateSong(self,SongName):

        #   Locate the song...

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:LocateSong")

        Ptr = 0
        RetValue = -1

        while Ptr < len(SongDataList) and RetValue == -1:

            if SongDataList[Ptr][4] == SongName:
                # Located the song information...
                RetValue = Ptr

            Ptr = Ptr + 1

        return RetValue

    #   Transpose - go down a key
    def TransposeMinusSelected(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:TransposeMinusSelected")

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")

            # Take it down a key
            SongDataList[SongPtr][3] -= 1

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # Wraparound if necessary
            if SongDataList[SongPtr][3] < 0:
                SongDataList[SongPtr][3] = 11

            # now re-display
            self.DisplaySong(self.CurrentSong)

            # we've made a change to the song set - save the list
            self.SaveSongList()

    #   Transpost - go up a key
    def TransposePlusSelected(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:TransposePlusSelected")

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")

            # take it up a key
            SongDataList[SongPtr][3] += 1

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # too high - wraparound
            if SongDataList[SongPtr][3] > 11:
                SongDataList[SongPtr][3] = 0

            # now re-display
            self.DisplaySong(self.CurrentSong)

            # we've made a change - save the song set.
            self.SaveSongList()


    #   Given a song name, put the song text onto screen
    #   Note - if the song offset is not zero, it transposes to the correct chord
    #          we don't ever overwrite the original chords - we re-work out each time
    #          doing it this way means that the positioning won't change if you keep transposing.
    def DisplaySong(self,SongName):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:DisplaySong")

        try:

            #   Locate the song...
            Ptr = self.LocateSong(SongName)

            if Ptr > -1:

                #   Located the song information...

                SongText = SongDataList[Ptr][1]
                SongKey = SongDataList[Ptr][2]
                SongOffset = SongDataList[Ptr][3]
                CurrentFontSize = SongDataList[Ptr][5]
                CurrentFontSize_Portrait = SongDataList[Ptr][6]
                CurrentPageSize = SongDataList[Ptr][7]
                CurrentPageSize_Portrait = SongDataList[Ptr][8]

                logmessage("MainWindow:DisplaySong:SongText")
                logmessage(SongText)
                ActualSongKey = Derive_Actual_Song_Key( SongKey, SongOffset)

                self.CurrentSong = SongName
                self.CurrentSongKey = SongKey
                self.CurrentOffset = SongOffset
                self.CurrentFontSize = CurrentFontSize
                self.CurrentFontSize_Portrait = CurrentFontSize_Portrait
                self.CurrentPageSize = CurrentPageSize
                self.CurrentPageSize_Portrait = CurrentPageSize_Portrait

                #  In order to have the display in columns and have different colours for particular items etc
                #  we use a HTML viewer to display the song text.
                #  This means we can apply style sheets - however, it appears the HTML viewer doesn't
                #  fully implement HTML?


                if self.WindowOrientation=='L':
                    if self.CurrentFontSize == "Default":
                        DisplayFontSize=SongPreferences['DEFAULTFONTSIZE']
                    else:
                        DisplayFontSize=self.CurrentFontSize
                else:
                    if self.CurrentFontSize == "Default":
                        print(SongPreferences)
                        DisplayFontSize=SongPreferences['DEFAULTFONTSIZE_PORTRAIT']
                    else:
                        DisplayFontSize=self.CurrentFontSize_Portrait

                #SongTextHeader = "<html><head>"
                #SongTextHeader = SongTextHeader + "<style>"
                #SongTextHeader = SongTextHeader + "body { background-color: #555555;font-size: "+DisplayFontSize+"px;} "
                #SongTextHeader = SongTextHeader + "p { font-size: "+DisplayFontSize+"px; margin: 0px;} "
                #SongTextHeader = SongTextHeader + "table { width: 100%; border: 2px solid black; padding 20px;} "
                #SongTextHeader = SongTextHeader + "tr { width: 100%; border: 2px solid black; padding 20px;} "
                #SongTextHeader = SongTextHeader + "td { border: 2px solid black; padding 5px; background-color: #eeeeee;} "
                #SongTextHeader = SongTextHeader + "</style>"
                SongTextHeader = """<html>
                <head>
                <style>
                body { 
                    background-color: #FFFFFF;
                    padding-top : 1em;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: """
                SongTextHeader = SongTextHeader+DisplayFontSize
                SongTextHeader = SongTextHeader+ """px; margin: 0px; 
                    } 
                p {
                  padding-top : 1em; 
                  font-family: Arial, Helvetica, sans-serif;  
                  font-size: """
                SongTextHeader = SongTextHeader+DisplayFontSize
                SongTextHeader = SongTextHeader+ """px; margin: 0px; 
                }
                p.heading {
                  padding-top : 0; 
                  font-family: Arial, Helvetica, sans-serif;
                  color: red;
                  margin: 0px;
                  font-size: """
                SongTextHeader = SongTextHeader+DisplayFontSize
                SongTextHeader = SongTextHeader+ """px;
                }
                p.nochords {
                  padding-top : 0;  
                  font-family: Arial, Helvetica, sans-serif; 
                  margin: 0px;
                  font-size: """
                SongTextHeader = SongTextHeader+DisplayFontSize
                SongTextHeader = SongTextHeader+ """px; 
                }
                p.onlychords {
                  padding-top : 0;  
                  font-family: Arial, Helvetica, sans-serif; 
                  margin: 0px;
                  font-weight: bold;
                  font-style: italic;
                  color: blue;
                  font-size: """
                SongTextHeader = SongTextHeader+DisplayFontSize
                SongTextHeader = SongTextHeader+ """px; 
                }

                em {
                    font-style: normal;
                }

                em[data-chord]:before {
                    position: relative;
                    top: -1em;
                    display: inline-block;
                    content: attr(data-chord);
                    width: 0;
                    font-weight: bold;
                    font-style: italic;
                    color: blue;
                    font-family: Arial, Helvetica, sans-serif;
                    speak: literal-punctuation;
                    pause: 1s;
                    margin-top: 10px;
                    /* pause between chord and text */
                }

                table {
                    padding: 0;
                    border: 1px solid black;
                }
                tr {
                    padding: 0;
                }
                td {
                    vertical-align: top;
                    border: 1px solid black;
                }

                </style>
                </head>
                <body>"""


                OutputSongText = "<table><tr><td style='padding:10px'>"

                if self.WindowOrientation=='L':
                    if self.CurrentPageSize == "Default":
                        Pagesize=SongPreferences['DEFAULTPAGESIZE']
                    else:
                        Pagesize=self.CurrentPageSize
                else:
                    if self.CurrentPageSize_Portrait == "Default":
                        Pagesize=SongPreferences['DEFAULTPAGESIZE_PORTRAIT']
                    else:
                        Pagesize=self.CurrentPageSize_Portrait

                SongLyricsDisplay = OutputSongText + Derive_Song_Text( "YES", SongText, SongKey, SongOffset,Pagesize,self.WindowOrientation)

                SongLyricsDisplay = SongLyricsDisplay.replace('SUS','sus')

                SongLyricsDisplay = SongTextHeader + SongLyricsDisplay + '</td></tr></table></body></html>'


                logmessage("MainWindow:DisplaySong:SongLyricDisplay")
                logmessage(SongLyricsDisplay)

                print("SONGTEXT---------------------------------------------------------")
                print(SongLyricsDisplay)
                print("SONGTEXT---------------------------------------------------------")

                #self.WindowOrientation.setText(self.WindowOrientation)
                self.setWindowTitle("OpenSong viewer - "+self.SaveFileName+" - "+SongName+"  ("+self.WindowOrientation+")")
                # self.SongText.setText(SongLyricsDisplay)
                self.SongText.setHtml(SongLyricsDisplay)
                self.CurrentKey.setText(SongKeys_Alt[ActualSongKey])
                self.CurrentKey2.setText(SongKeys_Alt[ActualSongKey])

        except Exception as e:
            print( "Error: DisplaySong")
            if hasattr(e, 'message'):
                print(e.message)
                logmessage(e.message)
            else:
                print(e)
                logmessage(e)


    #   User has clicked on a song on the on-screen list - display the song.
    def SongListSelected(self, index):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:SongListSelected")

        #   This is the selected song...
        SelectedString = index.data()

        self.DisplaySong(SelectedString)


    #   Remove a song from the song list on screen
    def DelSelectedSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:DelSelectedSong")

        # del the currently selected song - i.e. 'self.CurrentSong'

        Result = self.AskQuery("Remove Song from list?", "Remove "+self.CurrentSong+" from song list?")

        if Result == "YES":
            # Yes - delete the item in the on-screen list
            listItems = self.SongList.selectedIndexes()
            if not listItems:
                return
            for item in listItems:
                self.SongListModel.removeRow(item.row())

            Ptr = self.LocateSong(self.CurrentSong)

            if Ptr >= 0:
                ToRemove = SongDataList[Ptr]
                SongDataList.remove(ToRemove)

            print("Removed: " + self.CurrentSong)

    #   Clear the song list on-screen and data structure
    def ClearAll(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:ClearAll")

        Result = self.AskQuery("Clear Songlist?", "Clear Songlist?")

        if Result == "YES":
            self.SongListModel.clear()
            SongDataList = []
            self.SaveFileName='SongData.json'

            print("Cleared")

    #   Save a specific song name from the data structure to a song file
    #   Save the file in 'OpenSong' format (xml)
    def SaveSong(self,SongName):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:SaveSong")

        #   Locate the given song
        Ptr = self.LocateSong(self.CurrentSong)

        if Ptr >= 0:
            #   Get the data about the song
            SingleSongData = SongDataList[Ptr]

            #   Get the default song location and add the song name
            Fname = self.SongLocation + '/' + SongName

            #   Linux / windows
            if os.sep == '\\':
                Fname = Fname.replace('/', '\\')

            # 0.4: Open the original song we're going to overwrite
            #      and grab the data from it - so that we preserve
            #      the information when we overwrite
            #      if the song is 'brand new' then we'll not be able
            #      to open, and should go through the exception handler
            #      and we can set default values.

            # If the file already exists, read the file in and overwrite
            # individual elements
            # otherwise create a file from scratch.
            if os.path.isfile(Fname):

                try:
                    with open(Fname, 'r') as Originalfile:
                        SongData = Originalfile.read()

                    # tree contains the tree structure
                    tree = ET.ElementTree(ET.fromstring(SongData))

                    # Overwrite the items within the XML...
                    tree.find('title').text = SingleSongData[4]
                    tree.find('lyrics').text = SingleSongData[1]
                    tree.find('key').text = SingleSongData[2]
                    tree.find('user1').text = SingleSongData[5]+'|'+SingleSongData[6]+'|'+SingleSongData[7]+'|'+SingleSongData[8]

                    # overwrite the original file with the updated values
                    tree.write(Fname)

                except:

                    self.OkMessage("Problem overwriting file...",sys.exc_info()[0])

            else:

                # the file doesn't exist - so we need to create a new file from scratch

                #   Work out the text to save.

                FilenameTup=os.path.splitext(Fname)

                if FilenameTup[1] == '':
                    New_FileName = Fname+".xml"
                else:
                    New_FileName = Fname
                New_SongText = '<?xml version="1.0" encoding="UTF-8"?>\n'
                New_SongText = New_SongText + '<song>\n'
                New_SongText = New_SongText + '<title>'+SingleSongData[4]+'</title>\n'
                New_SongText = New_SongText + '  <lyrics>'
                New_SongText = New_SongText + SingleSongData[1]+'\n'
                New_SongText = New_SongText + '  </lyrics>\n'
                New_SongText = New_SongText + '<author></author>\n'
                New_SongText = New_SongText + '<copyright></copyright>\n'
                New_SongText = New_SongText + '<hymn_number></hymn_number>\n'
                New_SongText = New_SongText + '<presentation></presentation>\n'
                New_SongText = New_SongText + '<ccli></ccli>\n'
                New_SongText = New_SongText + '<capo print = "false"></capo>\n'
                New_SongText = New_SongText + '<key>'+SingleSongData[2]+'</key>\n'
                New_SongText = New_SongText + '<aka></aka>\n'
                New_SongText = New_SongText + '<key_line></key_line>\n'
                New_SongText = New_SongText + '<user1>'+SingleSongData[5]+'|'+SingleSongData[6]+'|'+SingleSongData[7]+'|'+SingleSongData[8]+'</user1>\n'
                New_SongText = New_SongText + '<user2></user2>\n'
                New_SongText = New_SongText + '<user3></user3>\n'
                New_SongText = New_SongText + '<theme></theme>\n'
                New_SongText = New_SongText + '<linked_songs></linked_songs>\n'
                New_SongText = New_SongText + '<tempo></tempo>\n'
                New_SongText = New_SongText + '<time_sig></time_sig>\n'
                New_SongText = New_SongText + '<backgrounds resize="body" keep_aspect="false" link="false" background_as_text="false"/>\n'
                New_SongText = New_SongText + '</song>\n'

                logmessage("MainWindow:SaveSong:SongText")
                logmessage(New_SongText)

                #   and write out the file
                with open(New_FileName, 'w') as myfile:
                    myfile.write(New_SongText)

                # we've made a change - save the song set.
                self.SaveSongList()


    #   User has clicked on 'Edit'
    def EditCurrentSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:EditCurrentSong")

        #   Locate the song
        Ptr = self.LocateSong(self.CurrentSong)

        if Ptr > -1:
            SingleSongData = SongDataList[Ptr]

            logmessage("EditCurrentSong:"+SingleSongData[4])
            logmessage("EditCurrentSong:Prior song text:")
            logmessage("EditCurrentSong:"+SingleSongData[1])

            #   Initialise and show the song
            dlg = EditWindow(SingleSongData)

            #   Activate the window on screen
            if dlg.exec_():
                print("Success!")
                logmessage("EditCurrentSong:Post song text:")
                logmessage("EditCurrentSong:"+SingleSongData[1])
                #   Copy the song data to the main data structure
                SongDataList[Ptr][0] = self.SongLocation+'/'+dlg.ui.FName.text()
                SongDataList[Ptr][1] = dlg.ui.EditingSongText.toPlainText()
                SongDataList[Ptr][2] = dlg.ui.SongKey.currentText()
                SongDataList[Ptr][3] = 0
                SongDataList[Ptr][4] = dlg.ui.FName.text()
                SongDataList[Ptr][5] = dlg.ui.DefaultFontSize.currentText()
                SongDataList[Ptr][6] = dlg.ui.DefaultFontSize_Portrait.currentText()
                SongDataList[Ptr][7] = dlg.ui.PageSize.currentText()
                SongDataList[Ptr][8] = dlg.ui.PageSize_Portrait.currentText()
                self.DisplaySong(self.CurrentSong)
                self.SaveSong(self.CurrentSong)
                logmessage("EditCurrentSong: Saved")
                print('Edited song saved')
            else:
                logmessage("EditCurrentSong: Cancel")
                print("Cancel!")

    #   User has selected to add a new song
    def NewSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:NewSong")

        # Create a blank song
        SingleSongData = ['a','a','a',0,'a','a','a','a','a']
        SingleSongData[0] = self.SongLocation+'/New Song'
        SingleSongData[1] = '.C\n Words'
        SingleSongData[2] = 'C'
        SingleSongData[3] = 0
        SingleSongData[4] = 'New Song'
        SingleSongData[5] = 'Default'
        SingleSongData[6] = 'Default'
        SingleSongData[7] = 'Default'
        SingleSongData[8] = 'Default'

        # Initialise the edit window
        dlg = EditWindow(SingleSongData)

        # Activate the edit window
        if dlg.exec_():
            print("Success!")
            SingleSongData[0] = self.SongLocation+'/'+dlg.ui.FName.text()
            SingleSongData[1] = dlg.ui.EditingSongText.toPlainText()
            SingleSongData[2] = dlg.ui.SongKey.currentText()
            SingleSongData[3] = 0
            SingleSongData[4] = dlg.ui.FName.text()
            SingleSongData[5] = dlg.ui.DefaultFontSize.currentText()
            SingleSongData[6] = dlg.ui.DefaultFontSize_Portrait.currentText()
            SingleSongData[7] = dlg.ui.PageSize.currentText()
            SingleSongData[8] = dlg.ui.PageSize_Portrait.currentText()

            #   Up to this point its the same as edit - however, now we need to add the
            #   new song to the on-screen list, and display.
            SongDataList.append(SingleSongData)
            self.CurrentSong = SingleSongData[4]
            item = QStandardItem(self.CurrentSong)
            self.SongListModel.appendRow(item)
            self.DisplaySong(self.CurrentSong)
            self.SaveSong(self.CurrentSong)
            logmessage("MainWindow:SaveSong")
        else:
            print("Cancel!")
            logmessage("MainWindow:Cancel")


    #   User has selected to add a song to the list
    def AddNewSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        #   get the user to select a song.
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        logmessage("MainWindow:AddNewSong")

        dialog = OpenFile()
        if dialog.exec_():

            SongNameToAdd=dialog.ui.lineEdit.text()
            print(SongNameToAdd)

            #   If Windows, change the separator
            FName = SongPreferences['SONGDIR']+"/"+dialog.ui.lineEdit.text()

            # Add a new song, but as this is just 'new' keep the base key as-is i.e. ""
            self.LoadSongTitle(FName,0)

            logmessage("MainWindow:AddNewSong:"+FName)

            self.DisplaySong(SongNameToAdd)




    def LoadSongTitle(self, SongFilename, SetSongOffset):

            logmessage("MainWindow:LoadSongTitle")
            try:

                #   windows/linux
                FName=SongFilename
                if os.sep == '\\':
                    FName = FName.replace('/', '\\')
                FName = FName.replace(self.SongLocation+'\\', '')
                item = QStandardItem(os.path.basename(FName))
                self.SongListModel.appendRow(item)

                #   Read in the song data, to add to the list...

                print("reading file...")

                with open(FName, 'r') as myfile:
                    SongData = myfile.read()

                print("getting data")

                tree = ET.ElementTree(ET.fromstring(SongData))

                #   Interpret the XML into the main data structure
                print("getting lyrics")

                SongLyrics = list(tree.iter('lyrics'))

                print("getting key")

                KeyData = tree.find('key')

                if KeyData is None:
                    SongKeyValue = 'C'
                else:
                    SongKey = list(tree.iter('key'))
                    if SongKey[0].text is None:
                        SongKeyValue = 'C'
                    else:
                        SongKeyValue = SongKey[0].text

                logmessage("MainWindow:LoadSongTitle:KeyData:"+SongKeyValue)
                print("getting fontsize")

                ExtraInfo = tree.find('user1')
                ExtraInfoText=ExtraInfo.text

                try:
                    if "|" in ExtraInfoText:
                    # we have extra font info...

                        ExtraInfoArray=ExtraInfoText.split("|")

                        FontSize = ExtraInfoArray[0]
                        if len(FontSize) == 0:
                            FontSize = "Default"

                        FontSize_Portrait = ExtraInfoArray[1]
                        if len(FontSize_Portrait) == 0:
                            FontSize = "Default"

                        PageSize = ExtraInfoArray[2]
                        if len(PageSize) == 0:
                            PageSize = "Default"

                        PageSize_Portrait = ExtraInfoArray[3]
                        if len(PageSize_Portrait) == 0:
                            PageSize_Portrait = "Default"

                    else:

                        FontSize = "Default"
                        FontSize_Portrait = "Default"
                        PageSize = "Default"
                        PageSize_Portrait = "Default"


                except:
                    FontSize = "Default"
                    FontSize_Portrait = "Default"
                    PageSize = "Default"
                    PageSize_Portrait = "Default"


                logmessage("MainWindow:LoadSongTitle:Fontdata:FontSize_L:"+FontSize+" P:"+FontSize_Portrait+" Pagesize_L:"+PageSize+" P:"+PageSize_Portrait)

                print("create list element")
                # Create list element, SongName, LyricsText, Key, OffsetToKey
                print("Filename:" + FName)
                print("Lyrics:" + SongLyrics[0].text)
                print("Key:" + SongKeyValue)
                print("Font:" + FontSize)
                print("Font_Portrait:" + FontSize_Portrait)
                print("Pagesize:" + PageSize)
                print("Pagesize_Portrait:" + PageSize_Portrait)

                logmessage("MainWindow:LoadSongTitle:Lyrics")
                logmessage(SongLyrics[0].text)

                # Data structure
                # 0 - full file and path name
                # 1 - lyrics text
                # 2 - Base key
                # 3 - Offset
                # 4 - Basename (just the file name)
                # 5 - Font size (Landscape)
                # 6 - Font size_Portrait
                # 7 - Pagesize (Landscape)
                # 8 - Pagesize_Portrait
                NewSongData = [FName, SongLyrics[0].text, SongKeyValue, SetSongOffset, os.path.basename(FName),FontSize,FontSize_Portrait,PageSize,PageSize_Portrait]

                print("append into songdata")
                SongDataList.append(NewSongData)
                print("added")

                logmessage("MainWindow:LoadSongTitle: Added")
                self.SaveSongList()

            except:
                logmessage("MainWindow:LoadSongTitle: Error adding song?")
                print("Error trying to add song - ignoring")


    def CleanString(self,InputString):

        logmessage("MainWindow:CleanString")

        logmessage("MainWindow:CleanString: Input:"+InputString)

        OutputString = ""
        for Ptr in range(0,len(InputString)):
            if InputString[Ptr] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ()[]=:-":
                OutputString += InputString[Ptr]

        logmessage("MainWindow:CleanString: Output:"+OutputString)
        return OutputString

    #   User has selected to edit prefs
    def UpdatePrefs(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        logmessage("MainWindow:UpdatePrefs")

        #   Initialise window
        dlg = Prefs()

        #   Activate preferences screen
        if dlg.exec_():
            print("Success!")

            #   Pick up the values from screen
            SongPreferences['PREFSVER'] = '0.9'
            SongPreferences['SONGDIR'] = dlg.ui.SongDirectory.text()

            SongPreferences['DEFAULTFONTSIZE'] = dlg.ui.DefaultFontSize.currentText()
            SongPreferences['DEFAULTFONTSIZE_PORTRAIT'] = dlg.ui.DefaultFontSize_Portrait.currentText()
            SongPreferences['DEFAULTPAGESIZE'] = dlg.ui.PageSize.currentText()
            SongPreferences['DEFAULTPAGESIZE_PORTRAIT'] = dlg.ui.PageSize_Portrait.currentText()

            if dlg.ui.radioButton_Cs.isChecked():
                SongPreferences['SHARPFLAT_C'] = 'C#'
            else:
                SongPreferences['SHARPFLAT_C'] = 'Db'

            if dlg.ui.radioButton_Ds.isChecked():
                SongPreferences['SHARPFLAT_D'] = 'D#'
            else:
                SongPreferences['SHARPFLAT_D'] = 'Eb'

            if dlg.ui.radioButton_Fs.isChecked():
                SongPreferences['SHARPFLAT_F'] = 'F#'
            else:
                SongPreferences['SHARPFLAT_F'] = 'Gb'

            if dlg.ui.radioButton_Gs.isChecked():
                SongPreferences['SHARPFLAT_G'] = 'G#'
            else:
                SongPreferences['SHARPFLAT_G'] = 'Ab'

            if dlg.ui.radioButton_As.isChecked():
                SongPreferences['SHARPFLAT_A'] = 'A#'
            else:
                SongPreferences['SHARPFLAT_A'] = 'Bb'

            #   0.5 20210402 - edit using original key or transposed key
            if dlg.ui.EditOriginalKey.isChecked():
                SongPreferences['EDIT_USE_ORIGINALKEY'] = 'ORIGINALKEY'
            else:
                SongPreferences['EDIT_USE_ORIGINALKEY'] = 'TRANSPOSEDKEY'

            if dlg.ui.ProduceLogFiles.isChecked():
                SongPreferences['PRODUCE_LOG_FILES']=1
            else:
                SongPreferences['PRODUCE_LOG_FILES']=0

            with open(self.SongPreferencesFileName, 'w') as f:
                json.dump(SongPreferences, f)

            # Set up preference variables.
            self.InterpretPreferences()

        else:
            print("Cancel!")

    def AboutWindow(self):

        logmessage("MainWindow:AboutWindow")

        #   Initialise window
        dlg = AboutWindow()

        #   Activate preferences screen - user just has to click on OK
        dlg.exec_()



#   MAIN CODE   =================================================================================

ProgramName = sys.argv[0]
ProgramName = ProgramName.upper()

try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass

#   If we're running in the GUI then set up and open the GUI...
if __name__ == "__main__":

    logmessage("Start:")
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # Get the icon's filename.
    icon_path = ".\Icons8-Windows-8-Very-Basic-Audio-File.512.ico"
    # Open the icon and set the Window/taskbar icon.
    w.setWindowIcon(QIcon(icon_path))
    logmessage("End:")
    sys.exit(app.exec_())
