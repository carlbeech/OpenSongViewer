import json
import os
import sys
import xml.etree.ElementTree as ET

#   GUI INCLUDES
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

#    Get designer screens in.
from EditWindow import Ui_Dialog
from MainWindow import Ui_MainWindow
from Prefs import Ui_PrefsEditor


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

VersionNumber = "0.2"

#   Initialisation of Edit Window
class EditWindow(QDialog):
    FullSongPath=''
    def __init__(self,SongData):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #   Copy variable values for single song into on-screen fields.
        self.FullSongPath=SongData[0]
        self.ui.FName.setText(SongData[4])
        self.ui.SongText.setPlainText(SongData[1])
        self.ui.SongKey.setCurrentText(SongData[2])

        #   Set the window up.
        self.show()

#   Initialisation of Preferences Window
class Prefs(QDialog):
    def __init__(self,PreferencesData):
        super().__init__()
        self.ui = Ui_PrefsEditor()
        self.ui.setupUi(self)

        #   Set up browse button
        self.ui.pushBrowse.clicked.connect(self.BrowseSelected)

        #   Copy variable values into on-screen fields
        self.ui.SongDirectory.setText(PreferencesData['SONGDIR'])

        #   Set the window up
        self.show()

    #   Browse to locate song directory.
    def BrowseSelected(self):

        try:

            CurrentDir = self.ui.SongDirectory.text()
            DirLoc=QFileDialog.getExistingDirectory(self, "Select Directory", CurrentDir)

            if len(DirLoc) > 1:
                self.ui.SongDirectory.setText(DirLoc)
        except:
            print('Error in selecting preferences?')



#   *****************************************************************************
#   Main UI window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    #   List holding songs

    # SongDataList - main Data structure
    # 0 - full file and path name
    # 1 - lyrics text
    # 2 - Base key
    # 3 - Offset
    # 4 - Basename (just the file name)

    SongDataList = []
    SongKeys =     ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    SongKeys_Alt = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    CurrentSong = ''
    CurrentSongKey = ''
    CurrentOffset = 0

    # Directory that holds the song files - picked up from preferences
    SongLocation = ''

    # Directory holding this program
    HomeDirectory=''
    # Location and name of preferences file - this is held in the same directory as the program
    SongPreferencesFileName = ''

    # V0.2: switch to use dictionary so can use a key:value pair.
    SongPreferences = { 'DUMMY': 'DUMMY'}

    #   Default songlist file name - we save after change (transpose etc)
    SaveFileName = 'SongData.json'

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        #   Set up song list (left hand side of screen)
        self.SongListModel = QStandardItemModel()
        self.SongList.setModel(self.SongListModel)

        # Work out the directory where the python/executable lives - preferences are within this dir.
        self.HomeDirectory = os.getcwd()
        self.SongPreferencesFileName = self.HomeDirectory+'\\OpenSongViewerPrefs.json'

        # try to pull in the preferences
        try:
            with open(self.SongPreferencesFileName) as f:
                self.SongPreferences = json.load(f)

        except:
            # none found - set default prefs.
            self.SongPreferences['PREFSVER'] = '0.2'
            self.SongPreferences['SONGDIR'] = self.HomeDirectory

        if type(self.SongPreferences) is list:
            # V0.1 preferences used lists instead of dict - convert and re-save
            print('Old V0.1 preferences file format - upgraded to v0.2')
            OLDPrefs=self.SongPreferences
            self.SongPreferences={}
            self.SongPreferences['PREFSVER'] = '0.2'
            self.SongPreferences['SONGDIR'] = OLDPrefs[0][1]

            # Overwrite old file
            with open(self.SongPreferencesFileName, 'w') as f:
                json.dump(self.SongPreferences, f)


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


    #   Do anything based on preferences settings - copy values to variables etc.
    def InterpretPreferences(self):

        # Go through the preferences and set variables.

        self.SongLocation = self.SongPreferences['SONGDIR']

    #   General routine to ask a query on screen
    def AskQuery(self,QueryTitle,QueryText):

        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if resp == 16384:
            return "YES"
        else:
            return "NO"


    #   Save the current song list, but specify a location.
    def SaveSongListAs(self):

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


    #   Save the song list to the current default file name
    def SaveSongList(self):
        # Take the current songdata and save this to a file e.g. 'SongData.json'
        SaveFileName = self.SaveFileName
        with open(SaveFileName,'w') as f:
            json.dump(self.SongDataList,f)

        print("Saved updated song list "+SaveFileName)


    #   Load a song list
    def LoadSongList(self):
        # Identify and load songdata, then update the screen.

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
                self.SongDataList = json.load(f)

            # Clear out and populate the song list panel.

            self.SongListModel.clear()

            # Add the files to the on-screen list
            Ptr = 0

            while Ptr < len(self.SongDataList):
                FName = self.SongDataList[Ptr][4]
                item = QStandardItem(FName)
                self.SongListModel.appendRow(item)
                Ptr = Ptr+1


    #   Given a song name, find the location within the main song array and return the number
    def LocateSong(self,SongName):

        #   Locate the song...
        Ptr = 0
        RetValue = -1

        while Ptr < len(self.SongDataList) and RetValue == -1:

            if self.SongDataList[Ptr][4] == SongName:
                # Located the song information...
                RetValue = Ptr

            Ptr = Ptr + 1

        return RetValue

    #   Transpose - go down a key
    def TransposeMinusSelected(self):

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")

            # Take it down a key
            self.SongDataList[SongPtr][3] -= 1

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # Wraparound if necessary
            if self.SongDataList[SongPtr][3] < 0:
                self.SongDataList[SongPtr][3] = 11

            # now re-display
            self.DisplaySong(self.CurrentSong)

            # we've made a change to the song set - save the list
            self.SaveSongList()

    #   Transpost - go up a key
    def TransposePlusSelected(self):

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")

            # take it up a key
            self.SongDataList[SongPtr][3] += 1

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # too high - wraparound
            if self.SongDataList[SongPtr][3] > 11:
                self.SongDataList[SongPtr][3] = 0

            # now re-display
            self.DisplaySong(self.CurrentSong)

            # we've made a change - save the song set.
            self.SaveSongList()


    #   Given a string which holds a chord, e.g. 'Gbm' , 'C' , 'C#' etc
    #   and an offset - return the updated chord string
    def ConvertChord(self, ChordString, Offset):

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
            if self.SongKeys[Ptr3] == TempString or self.SongKeys_Alt[Ptr3] == TempString:
                ActualSongKey = Ptr3
            Ptr3 += 1

        ActualSongKey = ActualSongKey+Offset

        if ActualSongKey > 11:
            ActualSongKey = ActualSongKey-12
            # print("Chordstring:" + ChordString + " Offset:" + str(Offset) + " Final:" + self.SongKeys[ActualSongKey])

        OutputString = self.SongKeys_Alt[ActualSongKey]
        if IsMinor == 1:
            OutputString = OutputString+"m"

        OutputString = OutputString.replace('G#','Ab')
        OutputString = OutputString.replace('A#','Bb')
        OutputString = OutputString.replace('D#','Eb')

        return OutputString


    #   Given a song name, put the song text onto screen
    #   Note - if the song offset is not zero, it transposes to the correct chord
    #          we don't ever overwrite the original chords - we re-work out each time
    #          doing it this way means that the positioning won't change if you keep transposing.
    def DisplaySong(self,SongName):

        #   Locate the song...
        Ptr = self.LocateSong(SongName)

        if Ptr > -1:

            #   Located the song information...

            SongText = self.SongDataList[Ptr][1]
            SongKey = self.SongDataList[Ptr][2]
            SongOffset = self.SongDataList[Ptr][3]

            # Work out the actual key
            # i.e. the original key + the offset
            Ptr3 = 0

            ActualSongKey = -1

            while Ptr3 < 11 and ActualSongKey == -1:
                if self.SongKeys[Ptr3] == SongKey or self.SongKeys_Alt[Ptr3] == SongKey:
                    ActualSongKey = Ptr3
                Ptr3 += 1

            if ActualSongKey > -1:
                # i.e. the key was found...
                # now add the offset...

                ActualSongKey = ActualSongKey + SongOffset

                # wrap around if necessary...
                if ActualSongKey > 11:
                    ActualSongKey = ActualSongKey - 12

            self.CurrentSong = SongName
            self.CurrentSongKey = SongKey
            self.CurrentOffset = SongOffset

            #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
            #   First, split the string on newlines.

            SongTextLines = SongText.split('\n')

            #   Now, go through the lines...

            Ptr2 = 0

            #  In order to have the display in columns and have different colours for particular items etc
            #  we use a HTML viewer to display the song text.
            #  This means we can apply style sheets - however, it appears the HTML viewer doesn't
            #  fully implement HTML?
            SongTextHeader = "<html><head>"
            SongTextHeader = SongTextHeader + "<style>"
            SongTextHeader = SongTextHeader + "body { background-color: #555555;} "
            SongTextHeader = SongTextHeader + "p { font-size: 25px; margin: 0px;} "
            SongTextHeader = SongTextHeader + "table { width: 100%; border: 2px solid black; padding 20px;} "
            SongTextHeader = SongTextHeader + "tr { width: 100%; border: 2px solid black; padding 20px;} "
            SongTextHeader = SongTextHeader + "td { border: 2px solid black; padding 5px; background-color: #eeeeee;} "
            SongTextHeader = SongTextHeader + "</style>"
            SongTextHeader = SongTextHeader + "</head>"
            SongTextHeader = SongTextHeader + "<body>"

            SongText = "<table><tr><td>"

            SongTextLineNumber = 0

            # Work through all the lines of text
            while Ptr2 < (len(SongTextLines)-1):

                # Put the line we're working with into a working variable
                TextLine = SongTextLines[Ptr2]

                # If its not a blank line
                if len(TextLine) > 0:

                    # is it a command line?
                    if TextLine[0] == '.':

                        #   Line begins with '.' - it contains chords - need to work through letter by letter

                        Ptr3 = 0    # pointer into the text line
                        OutputLine = ''   # converted line

                        # Create a temp line with extra spaces at the end - so we don't read past the end of line.
                        TempLine = TextLine + "   "

                        while Ptr3 < len( TextLine ):

                            NewValue = ord(TextLine[Ptr3])

                            if 65 <= NewValue <= 71:
                                # This is a key value

                                # Get the chord
                                NewString = TextLine[Ptr3]

                                # Check: is this a minor or sharp?
                                if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
                                    NewString = NewString+TextLine[Ptr3+1]
                                    Ptr3 = Ptr3+1
                                    # Check: is this a minor or sharp?
                                    if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
                                        NewString = NewString+TextLine[Ptr3+1]
                                        Ptr3 = Ptr3+1

                                # NewString now contains the chord - convert it...
                                UpdatedChord = self.ConvertChord(NewString,SongOffset)

                                OutputLine = OutputLine+UpdatedChord

                            else:
                                OutputLine = OutputLine+TextLine[Ptr3]

                            Ptr3 = Ptr3+1

                        # Now put bold around it..
                        OutputLine = "<b>"+OutputLine+"</b>"
                    else:
                        OutputLine = TextLine
                else:
                    # its a blank line
                    OutputLine = '\n '

                # If we're too far down, go to another display column
                if SongTextLineNumber > 38 or "===" in TextLine:
                    SongTextLineNumber = 1
                    OutputLine = OutputLine+'</td><td>'
                    # print("NewLine")

                TextLine = "<p>"+OutputLine+"&nbsp;&nbsp;&nbsp;&nbsp;</p>"

                SongText = SongText+'\n'+TextLine

                Ptr2 = Ptr2+1
                SongTextLineNumber = SongTextLineNumber+1


            SongLyricsDisplay = SongText.replace('\n.','<b> ').replace('\n ','</b> ').replace(' ','&nbsp;')

            SongLyricsDisplay = SongLyricsDisplay.replace('SUS','sus')

            SongLyricsDisplay = SongLyricsDisplay.replace('[','<b><font color=''red''>[').replace(']',']</font></b>')

            SongLyricsDisplay = SongTextHeader + SongLyricsDisplay + '</td></tr></table></body></html>'

            # print(SongLyricsDisplay)

            self.SongText.setText(SongLyricsDisplay)
            self.CurrentKey.setText(self.SongKeys_Alt[ActualSongKey])


    #   User has clicked on a song on the on-screen list - display the song.
    def SongListSelected(self, index):

        #   This is the selected song...
        SelectedString = index.data()

        self.DisplaySong(SelectedString)


    #   Remove a song from the song list on screen
    def DelSelectedSong(self):

        # del the currently selected song - i.e. 'self.CurrentSong'

        Result = self.AskQuery("Delete Song?", "Delete "+self.CurrentSong)

        if Result == "YES":
            # Yes - delete the item in the on-screen list
            listItems = self.SongList.selectedIndexes()
            if not listItems:
                return
            for item in listItems:
                self.SongListModel.removeRow(item.row())

            Ptr = self.LocateSong(self.CurrentSong)

            if Ptr >= 0:
                ToRemove = self.SongDataList[Ptr]
                self.SongDataList.remove(ToRemove)

            print("Removed: " + self.CurrentSong)

    #   Clear the song list on-screen and data structure
    def ClearAll(self):

        Result = self.AskQuery("Clear Songlist?", "Clear Songlist?")

        if Result == "YES":
            self.SongListModel.clear()
            self.SongDataList = []

            print("Cleared")

    #   Save a specific song name from the data structure to a song file
    #   Save the file in 'OpenSong' format (xml)
    def SaveSong(self,SongName):

        #   Locate the given song
        Ptr = self.LocateSong(self.CurrentSong)

        if Ptr >= 0:
            #   Get the data about the song
            SingleSongData = self.SongDataList[Ptr]

            #   Get the default song location and add the song name
            Fname = self.SongLocation + '/' + SongName

            #   Linux / windows
            if os.sep == '\\':
                Fname = Fname.replace('/', '\\')

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
            New_SongText = New_SongText + '<capo print = "false" ></capo>\n'
            New_SongText = New_SongText + '<key>'+SingleSongData[2]+'</key>\n'
            New_SongText = New_SongText + '<aka></aka>\n'
            New_SongText = New_SongText + '<key_line></key_line>\n'
            New_SongText = New_SongText + '<user1></user1>\n'
            New_SongText = New_SongText + '<user2></user2>\n'
            New_SongText = New_SongText + '<user3></user3>\n'
            New_SongText = New_SongText + '<theme></theme>\n'
            New_SongText = New_SongText + '<linked_songs/>\n'
            New_SongText = New_SongText + '<tempo></tempo>\n'
            New_SongText = New_SongText + '<time_sig></time_sig>\n'
            New_SongText = New_SongText + '<backgrounds resize = "screen" keep_aspect = "false" link = "false" background_as_text = "false" />\n'
            New_SongText = New_SongText + '</song>\n'

            #   and write out the file
            with open(New_FileName, 'w') as myfile:
                myfile.write(New_SongText)


    #   User has clicked on 'Edit'
    def EditCurrentSong(self):

        #   Locate the song
        Ptr = self.LocateSong(self.CurrentSong)

        if Ptr > -1:
            SingleSongData = self.SongDataList[Ptr]

            #   Initialise and show the song
            dlg = EditWindow(SingleSongData)

            #   Activate the window on screen
            if dlg.exec_():
                print("Success!")
                #   Copy the song data to the main data structure
                self.SongDataList[Ptr][0] = self.SongLocation+'/'+dlg.ui.FName.text()
                self.SongDataList[Ptr][1] = dlg.ui.SongText.toPlainText()
                self.SongDataList[Ptr][2] = dlg.ui.SongKey.currentText()
                self.SongDataList[Ptr][3] = 0
                self.SongDataList[Ptr][4] = dlg.ui.FName.text()
                self.DisplaySong(self.CurrentSong)
                self.SaveSong(self.CurrentSong)
                print('Edited song saved')
            else:
                print("Cancel!")

    #   User has selected to add a new song
    def NewSong(self):

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
            self.SongDataList.append(SingleSongData)
            self.CurrentSong = SingleSongData[4]
            item = QStandardItem(self.CurrentSong)
            self.SongListModel.appendRow(item)
            self.DisplaySong(self.CurrentSong)
            self.SaveSong(self.CurrentSong)
        else:
            print("Cancel!")


    #   User has selected to add a song to the list
    def AddNewSong(self):

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
            self.SongDataList.append(NewSongData)
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

        #   Initialise window
        dlg = Prefs(self.SongPreferences)

        #   Activate preferences screen
        if dlg.exec_():
            print("Success!")

            #   Pick up the values from screen
            self.SongPreferences['PREFSVER'] = '0.2'
            self.SongPreferences['SONGDIR'] = dlg.ui.SongDirectory.text()

            with open(self.SongPreferencesFileName, 'w') as f:
                json.dump(self.SongPreferences, f)

            # Set up preference variables.
            self.InterpretPreferences()

        else:
            print("Cancel!")



#   MAIN CODE   =================================================================================

ProgramName = sys.argv[0]
ProgramName = ProgramName.upper()


#   If we're running in the GUI then set up and open the GUI...
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
