import json
import os
import sys
import xml.etree.ElementTree as ET

#   GUI INCLUDES
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

#    Get designer screens in.
from EditWindow import Ui_Dialog
from MainWindow import Ui_MainWindow
from Prefs import Ui_PrefsEditor
from About import Ui_About


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

VersionNumber = "0.5"
VersionInformation = "Release 1/4/21 - Carl Beech"

# SongDataList - main Data structure
# 0 - full file and path name
# 1 - lyrics text
# 2 - Base key
# 3 - Offset
# 4 - Basename (just the file name)

SongDataList = []
SongKeys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SongKeys_Alt = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# V0.2: switch to use dictionary so can use a key:value pair.
SongPreferences = {'DUMMY': 'DUMMY'}


#   Initialisation of Edit Window
class AboutWindow(QDialog):

    def __init__(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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

#   Initialisation of Edit Window
class EditWindow(QDialog):
    FullSongPath=''
    def __init__(self,SongData):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #   Copy variable values for single song into on-screen fields.
        self.FullSongPath=SongData[0]
        self.ui.FName.setText(SongData[4])

        SongText=SongData[1]
        SongKey=SongData[2]
        SongOffset = SongData[3]
        if SongPreferences['EDIT_USE_ORIGINALKEY'] == 'ORIGINALKEY':
            self.ui.SongText.setPlainText(SongText)
            self.ui.SongKey.setCurrentText(SongKey)
        else:
            ModifiedSongText=Derive_Song_Text( "NO", SongText, SongKey, SongOffset)
            ActualSongKey = Derive_Actual_Song_Key(SongKey, SongOffset)
            self.ui.SongText.setPlainText(ModifiedSongText)
            self.ui.SongKey.setCurrentText(SongKeys_Alt[ActualSongKey])

        #   Set the window up.
        self.show()

#   Initialisation of Preferences Window
class Prefs(QDialog):
    def __init__(self):
        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        super().__init__()
        self.ui = Ui_PrefsEditor()
        self.ui.setupUi(self)

        #   Set up browse button
        self.ui.pushBrowse.clicked.connect(self.BrowseSelected)

        #   Copy variable values into on-screen fields
        self.ui.SongDirectory.setText(SongPreferences['SONGDIR'])

        self.ui.DefaultFontSize.setCurrentText(SongPreferences['DEFAULTFONTSIZE'])

        self.ui.PageSize.setCurrentText(SongPreferences['DEFAULTPAGESIZE'])

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


        #   Set the window up
        self.show()

    #   Browse to locate song directory.
    def BrowseSelected(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        try:

            CurrentDir = self.ui.SongDirectory.text()
            DirLoc=QFileDialog.getExistingDirectory(self, "Select Directory", CurrentDir)

            if len(DirLoc) > 1:
                self.ui.SongDirectory.setText(DirLoc)
        except:
            print('Error in selecting preferences?')



#   *****************************************************************************
#   Support routines - used by multiple windows.

#   Given a base key, and an offset, work out the actual key and return that number
def Derive_Actual_Song_Key(SongBaseKey, SongOffset):
    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

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

    return ActualSongKey


#   Given a string which holds a chord, e.g. 'Gbm' , 'C' , 'C#' etc
#   and an offset - return the updated chord string
def ConvertChord(ChordString, Offset):

    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

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





#   Given the song text, and offset data, work out the updated song text with key change
#   also, have the option to output in HTML format or non HTML
#   HTML format is used to display a song on-screen, but non-HTML is used
#   if we want to edit, but use the transposed key (as we need to use plain text)
def Derive_Song_Text( HTML_Needed, SongText, SongKey, SongOffset):
    global SongDataList
    global SongKeys
    global SongKeys_Alt
    global SongPreferences

    ReturnString=""

    #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
    #   First, split the string on newlines.

    SongTextLines = SongText.split('\n')

    #   Now, go through the lines...

    Ptr2 = 0

    SongTextLineNumber = 0

    # Work through all the lines of text
    while Ptr2 < (len(SongTextLines) - 1):

        # Put the line we're working with into a working variable
        TextLine = SongTextLines[Ptr2]

        # If its not a blank line
        if len(TextLine) > 0:

            # is it a command line?
            if TextLine[0] == '.':

                #   Line begins with '.' - it contains chords - need to work through letter by letter

                Ptr3 = 0  # pointer into the text line
                OutputLine = ''  # converted line

                # Create a temp line with extra spaces at the end - so we don't read past the end of line.
                TempLine = TextLine + "   "

                while Ptr3 < len(TextLine):

                    NewValue = ord(TextLine[Ptr3])

                    if 65 <= NewValue <= 71:
                        # This is a key value

                        # Get the chord
                        NewString = TextLine[Ptr3]

                        # Check: is this a minor or sharp?
                        if (TempLine[Ptr3 + 1] == 'M') or (TempLine[Ptr3 + 1] == '#') or (TempLine[Ptr3 + 1] == 'b'):
                            NewString = NewString + TextLine[Ptr3 + 1]
                            Ptr3 = Ptr3 + 1
                            # Check: is this a minor or sharp?
                            if (TempLine[Ptr3 + 1] == 'M') or (TempLine[Ptr3 + 1] == '#') or (TempLine[Ptr3 + 1] == 'b'):
                                NewString = NewString + TextLine[Ptr3 + 1]
                                Ptr3 = Ptr3 + 1

                        # NewString now contains the chord - convert it...
                        UpdatedChord = ConvertChord(NewString, SongOffset)

                        OutputLine = OutputLine + UpdatedChord

                    else:
                        OutputLine = OutputLine + TextLine[Ptr3]

                    Ptr3 = Ptr3 + 1

                if HTML_Needed=="YES":
                    # Now put bold around it..
                    OutputLine = "<b>" + OutputLine + "</b>"
            else:
                OutputLine = TextLine
        else:
            # its a blank line
            OutputLine = '\n '

        if HTML_Needed=="YES":
            # If we're too far down, go to another display column
            if SongTextLineNumber > int(SongPreferences['DEFAULTPAGESIZE']) or "===" in TextLine:
                SongTextLineNumber = 1
                OutputLine = OutputLine + '</td><td>'
                # print("NewLine")

        if HTML_Needed=="YES":
            TextLine = "<p>" + OutputLine + "&nbsp;&nbsp;&nbsp;&nbsp;</p>"
        else:
            TextLine = OutputLine

        ReturnString = ReturnString + '\n' + TextLine

        Ptr2 = Ptr2 + 1
        SongTextLineNumber = SongTextLineNumber + 1

    return ReturnString

#   *****************************************************************************
#   Main UI window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    CurrentSong = ''
    CurrentSongKey = ''
    CurrentOffset = 0

    # Directory that holds the song files - picked up from preferences
    SongLocation = ''

    # Directory holding this program
    HomeDirectory=''
    # Location and name of preferences file - this is held in the same directory as the program
    SongPreferencesFileName = ''

    #   Default songlist file name - we save after change (transpose etc)
    SaveFileName = 'SongData.json'

    def __init__(self, parent=None):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        #   Set up song list (left hand side of screen)
        self.SongListModel = QStandardItemModel()
        self.SongList.setModel(self.SongListModel)

        # Work out the directory where the python/executable lives - preferences are within this dir.
        self.HomeDirectory = os.getcwd()
        self.SongPreferencesFileName = self.HomeDirectory+'\\OpenSongViewerPrefs.json'

        IntroText="Hello there<br><br>"
        IntroText=IntroText+"<i>OpenSongViewer version "+VersionNumber+"   "
        IntroText = IntroText +VersionInformation+"</i><br><br>"

        IntroText = IntroText +"Remember to set the location of your OpenSong songs in the preferences<br><br>"

        IntroText = IntroText +"Click on <br>"
        IntroText = IntroText +" * Add - to add a song to the song list<br>"
        IntroText = IntroText +" * Rem - to remove the current selected song to the song list<br>"
        IntroText = IntroText +" * Edit - to edit the current selected song to the song list<br><br>"

        IntroText = IntroText +"Remember to save your song list using 'Song List' -> 'Save As...' - it'll retain order and keys<br>"
        IntroText = IntroText +"Remember to check your current preferences under the file menu<br>"
        IntroText = IntroText +"<br>"

        IntroText = IntroText +"Changelog:<br>"
        IntroText = IntroText +"0.5 - bugfix - when transposing and base key was 'B' the value key didn't update<br>"
        IntroText = IntroText +" * Improvement - when you select a song in the songlist, you can now use right and left cursor or arrows under the songlist to move up and down the list<br>"
        IntroText = IntroText +" * Improvement - new preference setting - when editing, you can choose to always edit in the original base key, or edit in the current transposed value<br>"
        IntroText = IntroText +" - NOTE - if you edit in the current transposed value, this will overwrite the original base key<br>"
        IntroText = IntroText +" - this means that chord characters can move slightly when the base key switches from a single to a double character  - e.g. 'C' to 'Db'<br>"


        self.SongText.setText(IntroText)

        # try to pull in the preferences
        try:
            with open(self.SongPreferencesFileName) as f:
                SongPreferences = json.load(f)

        except:
            # none found - set default prefs.
            SongPreferences['PREFSVER'] = '0.5'
            SongPreferences['SONGDIR'] = self.HomeDirectory
            SongPreferences['DEFAULTFONTSIZE'] = '25'
            SongPreferences['DEFAULTPAGESIZE'] = '38'
            SongPreferences['SHARPFLAT_C'] = 'C#'
            SongPreferences['SHARPFLAT_D'] = 'D#'
            SongPreferences['SHARPFLAT_F'] = 'F#'
            SongPreferences['SHARPFLAT_G'] = 'G#'
            SongPreferences['SHARPFLAT_A'] = 'A#'
            SongPreferences['EDIT_USE_ORIGINALKEY'] = 'ORIGINALKEY'

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

        self.InterpretPreferences()

        #   Wire up the buttons
        self.AddSong.clicked.connect(self.AddNewSong)
        self.DeleteSong.clicked.connect(self.DelSelectedSong)
        self.EditSong.clicked.connect(self.EditCurrentSong)

        self.SongList.clicked.connect(self.SongListSelected)

        self.TransposeMinus.clicked.connect(self.TransposeMinusSelected)
        self.TransposePlus.clicked.connect(self.TransposePlusSelected)
        self.actionClear_List.triggered.connect(self.ClearAll)
        self.actionEdit.triggered.connect(self.EditCurrentSong)
        self.actionNew.triggered.connect(self.NewSong)

        self.actionSave_Song_List.triggered.connect(self.SaveSongList)
        self.actionLoad_Song_List.triggered.connect(self.LoadSongList)
        self.actionSave_Song_List_As.triggered.connect(self.SaveSongListAs)

        self.actionPreferences.triggered.connect(self.UpdatePrefs)
        self.actionAbout.triggered.connect(self.AboutWindow)

        self.NextSong.clicked.connect(self.MoveNextSong)
        self.PrevSong.clicked.connect(self.MovePrevSong)


    #   Do anything based on preferences settings - copy values to variables etc.
    def InterpretPreferences(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        # Go through the preferences and set variables.

        self.SongLocation = SongPreferences['SONGDIR']

    #   General routine to ask a query on screen
    def AskQuery(self,QueryTitle,QueryText):

        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if resp == 16384:
            return "YES"
        else:
            return "NO"

    #   General routine to ask a query on screen
    def OkMessage(self,QueryTitle,QueryText):

        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Ok, QMessageBox.Ok)


    #   Save the current song list, but specify a location.
    def SaveSongListAs(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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


    def NavigateSong(self,Direction):
        #   Improvement 20210401
        #   Click in the Main SongList - you can then use right and left keys to
        #   move through the songs instead of having to click on specific songs
        #   its slightly more efficient when playing live...

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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

        self.NavigateSong("DOWN")

    def MovePrevSong(self):
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

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        SaveFileName = self.SaveFileName
        with open(SaveFileName,'w') as f:
            json.dump(SongDataList,f)

        print("Saved updated song list "+SaveFileName)


    #   Load a song list
    def LoadSongList(self):
        # Identify and load songdata, then update the screen.

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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
                    item = QStandardItem(FName)
                    self.SongListModel.appendRow(item)
                    Ptr = Ptr+1
            except:
                self.OkMessage('Load error','Song list file is not compatible with this version - sorry')

    #   Given a song name, find the location within the main song array and return the number
    def LocateSong(self,SongName):

        #   Locate the song...

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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

        #   Locate the song...
        Ptr = self.LocateSong(SongName)

        if Ptr > -1:

            #   Located the song information...

            SongText = SongDataList[Ptr][1]
            SongKey = SongDataList[Ptr][2]
            SongOffset = SongDataList[Ptr][3]

            ActualSongKey = Derive_Actual_Song_Key( SongKey, SongOffset)

            self.CurrentSong = SongName
            self.CurrentSongKey = SongKey
            self.CurrentOffset = SongOffset

            #  In order to have the display in columns and have different colours for particular items etc
            #  we use a HTML viewer to display the song text.
            #  This means we can apply style sheets - however, it appears the HTML viewer doesn't
            #  fully implement HTML?
            SongTextHeader = "<html><head>"
            SongTextHeader = SongTextHeader + "<style>"
            SongTextHeader = SongTextHeader + "body { background-color: #555555;} "
            SongTextHeader = SongTextHeader + "p { font-size: "+SongPreferences['DEFAULTFONTSIZE']+"px; margin: 0px;} "
            SongTextHeader = SongTextHeader + "table { width: 100%; border: 2px solid black; padding 20px;} "
            SongTextHeader = SongTextHeader + "tr { width: 100%; border: 2px solid black; padding 20px;} "
            SongTextHeader = SongTextHeader + "td { border: 2px solid black; padding 5px; background-color: #eeeeee;} "
            SongTextHeader = SongTextHeader + "</style>"
            SongTextHeader = SongTextHeader + "</head>"
            SongTextHeader = SongTextHeader + "<body>"


            OutputSongText = "<table><tr><td>"

            OutputSongText = OutputSongText + Derive_Song_Text( "YES", SongText, SongKey, SongOffset)

            #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
            #   First, split the string on newlines.

            #SongTextLines = SongText.split('\n')


            #   Now, go through the lines...

            #Ptr2 = 0

            #SongTextLineNumber = 0

            # Work through all the lines of text
            #while Ptr2 < (len(SongTextLines)-1):

                # Put the line we're working with into a working variable
            #    TextLine = SongTextLines[Ptr2]

                # If its not a blank line
            #    if len(TextLine) > 0:

                    # is it a command line?
            #        if TextLine[0] == '.':

                        #   Line begins with '.' - it contains chords - need to work through letter by letter

            #            Ptr3 = 0    # pointer into the text line
            #            OutputLine = ''   # converted line

                        # Create a temp line with extra spaces at the end - so we don't read past the end of line.
            #            TempLine = TextLine + "   "

            #            while Ptr3 < len( TextLine ):

            #                NewValue = ord(TextLine[Ptr3])

            #                if 65 <= NewValue <= 71:
                                # This is a key value

                                # Get the chord
            #                    NewString = TextLine[Ptr3]

                                # Check: is this a minor or sharp?
            #                    if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
            #                        NewString = NewString+TextLine[Ptr3+1]
            #                        Ptr3 = Ptr3+1
                                    # Check: is this a minor or sharp?
            #                        if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
            #                            NewString = NewString+TextLine[Ptr3+1]
            #                            Ptr3 = Ptr3+1

                                # NewString now contains the chord - convert it...
            #                    UpdatedChord = self.ConvertChord(NewString,SongOffset)

            #                    OutputLine = OutputLine+UpdatedChord

            #                else:
            #                    OutputLine = OutputLine+TextLine[Ptr3]

            #                Ptr3 = Ptr3+1

                        # Now put bold around it..
            #            OutputLine = "<b>"+OutputLine+"</b>"
            #        else:
            #            OutputLine = TextLine
            #    else:
                    # its a blank line
            #        OutputLine = '\n '

                # If we're too far down, go to another display column
            #    if SongTextLineNumber > int(self.SongPreferences['DEFAULTPAGESIZE']) or "===" in TextLine:
            #        SongTextLineNumber = 1
            #        OutputLine = OutputLine+'</td><td>'
                    # print("NewLine")

            #    TextLine = "<p>"+OutputLine+"&nbsp;&nbsp;&nbsp;&nbsp;</p>"

            #    SongText = SongText+'\n'+TextLine

            #    Ptr2 = Ptr2+1
            #    SongTextLineNumber = SongTextLineNumber+1


            SongLyricsDisplay = OutputSongText.replace('\n.','<b> ').replace('\n ','</b> ').replace(' ','&nbsp;')

            SongLyricsDisplay = SongLyricsDisplay.replace('SUS','sus')

            SongLyricsDisplay = SongLyricsDisplay.replace('[','<b><font color=''red''>[').replace(']',']</font></b>')

            SongLyricsDisplay = SongTextHeader + SongLyricsDisplay + '</td></tr></table></body></html>'

            # print(SongLyricsDisplay)

            self.SongText.setText(SongLyricsDisplay)
            self.CurrentKey.setText(SongKeys_Alt[ActualSongKey])


    #   User has clicked on a song on the on-screen list - display the song.
    def SongListSelected(self, index):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        #   This is the selected song...
        SelectedString = index.data()

        self.DisplaySong(SelectedString)


    #   Remove a song from the song list on screen
    def DelSelectedSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        # del the currently selected song - i.e. 'self.CurrentSong'

        Result = self.AskQuery("Remove Song from list?", "Delete "+self.CurrentSong)

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

        Result = self.AskQuery("Clear Songlist?", "Clear Songlist?")

        if Result == "YES":
            self.SongListModel.clear()
            SongDataList = []

            print("Cleared")

    #   Save a specific song name from the data structure to a song file
    #   Save the file in 'OpenSong' format (xml)
    def SaveSong(self,SongName):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

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

                    # overwrite the original file with the updated values
                    tree.write(Fname)

                except:

                    self.OkMessage("Problem overwriting file...",sys.exc_info()[0])

            else:

                # the file doesn't exist - so we need to create a new file from scratch

                #   Work out the text to save.
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
                New_SongText = New_SongText + '<user1></user1>\n'
                New_SongText = New_SongText + '<user2></user2>\n'
                New_SongText = New_SongText + '<user3></user3>\n'
                New_SongText = New_SongText + '<theme></theme>\n'
                New_SongText = New_SongText + '<linked_songs></linked_songs>\n'
                New_SongText = New_SongText + '<tempo></tempo>\n'
                New_SongText = New_SongText + '<time_sig></time_sig>\n'
                New_SongText = New_SongText + '<backgrounds resize="body" keep_aspect="false" link="false" background_as_text="false"/>\n'
                New_SongText = New_SongText + '</song>\n'

                #   and write out the file
                with open(New_FileName, 'w') as myfile:
                    myfile.write(New_SongText)


    #   User has clicked on 'Edit'
    def EditCurrentSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        #   Locate the song
        Ptr = self.LocateSong(self.CurrentSong)

        if Ptr > -1:
            SingleSongData = SongDataList[Ptr]

            #   Initialise and show the song
            dlg = EditWindow(SingleSongData)

            #   Activate the window on screen
            if dlg.exec_():
                print("Success!")
                #   Copy the song data to the main data structure
                SongDataList[Ptr][0] = self.SongLocation+'/'+dlg.ui.FName.text()
                SongDataList[Ptr][1] = dlg.ui.SongText.toPlainText()
                SongDataList[Ptr][2] = dlg.ui.SongKey.currentText()
                SongDataList[Ptr][3] = 0
                SongDataList[Ptr][4] = dlg.ui.FName.text()
                self.DisplaySong(self.CurrentSong)
                self.SaveSong(self.CurrentSong)
                print('Edited song saved')
            else:
                print("Cancel!")

    #   User has selected to add a new song
    def NewSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        # Create a blank song
        SingleSongData = ['a','a','a',0,'a']
        SingleSongData[0] = self.SongLocation+'/New Song'
        SingleSongData[1] = '.C\n Words'
        SingleSongData[2] = 'C'
        SingleSongData[3] = 0
        SingleSongData[4] = 'New Song'

        # Initialise the edit window
        dlg = EditWindow(SingleSongData)

        # Activate the edit window
        if dlg.exec_():
            print("Success!")
            SingleSongData[0] = self.SongLocation+'/'+dlg.ui.FName.text()
            SingleSongData[1] = dlg.ui.SongText.toPlainText()
            SingleSongData[2] = dlg.ui.SongKey.currentText()
            SingleSongData[3] = 0
            SingleSongData[4] = dlg.ui.FName.text()

            #   Up to this point its the same as edit - however, now we need to add the
            #   new song to the on-screen list, and display.
            SongDataList.append(SingleSongData)
            self.CurrentSong = SingleSongData[4]
            item = QStandardItem(self.CurrentSong)
            self.SongListModel.appendRow(item)
            self.DisplaySong(self.CurrentSong)
            self.SaveSong(self.CurrentSong)
        else:
            print("Cancel!")


    #   User has selected to add a song to the list
    def AddNewSong(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        #   get the user to select a song.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        if fileName and len(fileName[0]) > 0:

            #   If Windows, change the separator
            FName = fileName[0]
            #   windows/linux
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

            print("create list element")
            # Create list element, SongName, LyricsText, Key, OffsetToKey
            print("Filename:" + FName)
            print("Lyrics:" + SongLyrics[0].text)
            print("Key:" + SongKeyValue)

            # Data structure
            # 0 - full file and path name
            # 1 - lyrics text
            # 2 - Base key
            # 3 - Offset
            # 4 - Basename (just the file name)
            NewSongData = [FName, SongLyrics[0].text, SongKeyValue, 0, os.path.basename(FName)]

            print("append into songdata")
            SongDataList.append(NewSongData)
            print("added")

            self.SaveSongList()


    def CleanString(self,InputString):

        OutputString = ""
        for Ptr in range(0,len(InputString)):
            if InputString[Ptr] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ()[]=:-":
                OutputString += InputString[Ptr]

        return OutputString

    #   User has selected to edit prefs
    def UpdatePrefs(self):

        global SongDataList
        global SongKeys
        global SongKeys_Alt
        global SongPreferences

        #   Initialise window
        dlg = Prefs()

        #   Activate preferences screen
        if dlg.exec_():
            print("Success!")

            #   Pick up the values from screen
            SongPreferences['PREFSVER'] = '0.5'
            SongPreferences['SONGDIR'] = dlg.ui.SongDirectory.text()

            SongPreferences['DEFAULTFONTSIZE'] = dlg.ui.DefaultFontSize.currentText()
            SongPreferences['DEFAULTPAGESIZE'] = dlg.ui.PageSize.currentText()

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

            with open(self.SongPreferencesFileName, 'w') as f:
                json.dump(SongPreferences, f)

            # Set up preference variables.
            self.InterpretPreferences()

        else:
            print("Cancel!")

    def AboutWindow(self):
        #   Initialise window
        dlg = AboutWindow()

        #   Activate preferences screen - user just has to click on OK
        dlg.exec_()



#   MAIN CODE   =================================================================================

ProgramName = sys.argv[0]
ProgramName = ProgramName.upper()


#   If we're running in the GUI then set up and open the GUI...
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
