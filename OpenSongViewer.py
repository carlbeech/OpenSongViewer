import os, sys, time, datetime, hashlib, getopt, signal, json

import xml.etree.ElementTree as ET

#   Use 'platform' library to identify OS.
import platform

#   Get constants
import Constants

#   GUI INCLUDES
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

# from AboutDialog import Ui_AboutDialog

#   Main screen code
from MainWindow import Ui_MainWindow
from EditWindow import Ui_Dialog
from Prefs import Ui_PrefsEditor

VersionNumber = "0.1"

#   HISTORY
#
#   0.1     Initial release


#   Holds output from shell

def OutputHelp():
    print('fdf_scanner.py -i <inputdir> [-i <inputdir>] [-p <preservedir>] [-p <preservedir>] [-c <configfile>] [-w] [-o <outputfile>]')
    print('')
    print('Where')
    print('  -i <InputDir>  (Mandatory) directory to scan for duplicates')
    print('  -p <PreserveDir> directory to NOT delete from')
    print('  -c <ConfigFile>  file holding run parameters')
    print('  -w               output file in WINDOWS Command prompt syntax (batch file)')
    print('  -o <OutputFile>  put comments/deletions in specific file - default fdf_scanner_output.sh (or .bat)')


    
def ParseInputOpts(argv):
    #   Parse input options


    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:p:d:c:w",["ifile=","ofile=","preservedir="])
    except getopt.GetoptError:
        OutputHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            OutputHelp()
            sys.exit()


class AskQuery(QWidget):

    AskQuery_TEXT=''
    AskQuery_RESULT=0

    def __init__(self,DialogTitle,InputMessageText,ReturnValue):
        super().__init__()
        self.title = DialogTitle
        self.left = 500
        self.top = 500
        self.width = 600
        self.height = 600
        self.AskQuery_TEXT=InputMessageText
        self.initUI()
        ReturnValue=self.AskQuery_RESULT

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, 'Query', self.AskQuery_TEXT,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            self.AskQuery_RESULT=1
        else:
            print('No clicked.')
            self.AskQuery_RESULT=0

        self.show()




class EditWindow(QDialog):
    def __init__(self,SongData):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.FName.setText(SongData[0])
        self.ui.SongText.setPlainText(SongData[1])
        self.ui.SongKey.setCurrentText(SongData[2])
        self.show()

class Prefs(QDialog):
    def __init__(self,PreferencesData):
        super().__init__()
        self.ui = Ui_PrefsEditor()
        self.ui.setupUi(self)
        Ptr=0

        while( Ptr < len(PreferencesData)):

            if PreferencesData[Ptr][0] == 'SONGDIR':
                self.ui.SongDirectory.setText(PreferencesData[Ptr][1])

            Ptr=Ptr+1

        self.show()



#   *****************************************************************************
#   Main UI window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    #   List holding songs
    SongDataList = []
    SongKeys =     ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    SongKeys_Alt = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    CurrentSong = ''
    CurrentSongKey = ''
    CurrentOffset = 0
    SongLocation=''

    SongPreferences=[]

    SaveFileName='SongData.json'

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        #   Create the initial data structure to hold the song list.
        self.SongListModel = QStandardItemModel()
        self.SongList.setModel(self.SongListModel)

        #   Configuration data: default location of files

        # self.SongLocation = 'C:\\Users\\Carl\\Google Drive\\OpenSong\\OpenSong\\Songs'

        # Work out the directory where the python/executable lives.
        SongViewerPreferencesDir=os.getcwd()
        SongViewerPreferences=SongViewerPreferencesDir+'\\OpenSongViewerPrefs.json'

        # try to pull in the preferences
        try:
            with open(SongViewerPreferences) as f:
                self.SongPreferences = json.load(f)

        except:
            # none found - set default prefs.
            SongPref=['SONGDIR',SongViewerPreferencesDir]
            self.SongPreferences.append( SongPref )

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


    def InterpretPreferences(self):

        # Go through the preferences and set variables.
        Ptr=0

        while( Ptr < len(self.SongPreferences)):

            if self.SongPreferences[Ptr][0] == 'SONGDIR':
                self.SongLocation = self.SongPreferences[Ptr][1]

            Ptr=Ptr+1

    def AskQuery(self,QueryTitle,QueryText):

        resp = QMessageBox.question(self, QueryTitle, QueryText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)


        if resp == 16384:
            return "YES"
        else:
            return "NO"

#        Result=2
#        AskQuery(QueryTitle,QueryText,Result)
#        # Result=AskQuery_RESULT

#        print("Final Returning "+str(Result))
#        return Result


    def SaveSongListAs(self):

        # Set the new default file name for songs.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        SaveFile = QFileDialog.getSaveFileName(self, 'Save Song List As',self.SongLocation)

        if os.sep == '\\':
            FName = SaveFile.replace('/', '\\')

        self.SaveFileName=SaveFile[0]

        # and save the songlist
        self.SaveSongList()

    def SaveSongList(self):
        # Take the current songdata and save this to a file e.g. 'SongData.json'
        SaveFileName=self.SaveFileName
        with open(SaveFileName,'w') as f:
            json.dump(self.SongDataList,f)

        print("Saved updated song list "+SaveFileName)

    def LoadSongList(self):
        # Identify and load songdata, then update the screen.

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        if fileName and len(fileName[0])>0:

            #   If Windows, change the separator
            FName = fileName[0]
            if os.sep == '\\':
                FName = FName.replace('/', '\\')

            # Set the default from now on...
            self.SaveFileName=FName

            # Now, open then file and read the JSON data.

            with open(FName) as f:
                self.SongDataList=json.load(f)

            # Clear out and populate the song list panel.

            self.SongListModel.clear()

            Ptr=0

            while Ptr < len(self.SongDataList):
                FName = self.SongDataList[Ptr][0]
                item = QStandardItem(FName)
                self.SongListModel.appendRow(item)
                Ptr=Ptr+1


    def LocateSong(self,SongName):

        #   Locate the song...
        Ptr = 0
        RetValue = -1

        while Ptr < len(self.SongDataList) and RetValue == -1:

            if self.SongDataList[Ptr][0] == SongName:
                # Located the song information...
                RetValue = Ptr

            Ptr = Ptr + 1

        return RetValue

    def TransposeMinusSelected(self):

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")
            #print(self.SongDataList[SongPtr][3])
            # Take it down a key
            self.SongDataList[SongPtr][3] -= 1

            #print(self.SongDataList[SongPtr][3])

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # Wraparound if necessary
            if self.SongDataList[SongPtr][3] < 0:
                self.SongDataList[SongPtr][3] = 11

            # print(self.SongDataList[SongPtr][3])

            # now re-display
            self.DisplaySong(self.CurrentSong)

            self.SaveSongList()

    def TransposePlusSelected(self):

        #   Locate the song...
        SongPtr = self.LocateSong(self.CurrentSong)

        if SongPtr > -1:
            # got a valid song..

            print("Located song")
            #print(self.SongDataList[SongPtr][3])

            # take it up a key
            self.SongDataList[SongPtr][3] += 1

            #print(self.SongDataList[SongPtr][3])

            # 0 1  2 3  4 5 6  7 8  9  10 11
            # c c# d d# e f f# g g# a  a# b

            # too high - wraparound
            if self.SongDataList[SongPtr][3] > 11:
                self.SongDataList[SongPtr][3] = 0

            #print(self.SongDataList[SongPtr][3])

            # now re-display
            self.DisplaySong(self.CurrentSong)

            self.SaveSongList()

    def ConvertChord(self, ChordString, Offset):

        Ptr1=0
        TempString=''
        IsMinor=0
        while (Ptr1<len(ChordString)):
            if ChordString[Ptr1]=='M':
                IsMinor=1
            else:
                TempString=TempString+ChordString[Ptr1]
            Ptr1=Ptr1+1

        if len(TempString)>2:
            print("Weird?")

        Ptr3 = 0

        ActualSongKey = -1

        while Ptr3 < 11 and ActualSongKey == -1:
            if self.SongKeys[Ptr3] == TempString or self.SongKeys_Alt[Ptr3] == TempString:
                ActualSongKey = Ptr3
            Ptr3 += 1

        ActualSongKey=ActualSongKey+Offset

        if ActualSongKey>11:
            ActualSongKey=ActualSongKey-12
            #print("Chordstring:" + ChordString + " Offset:" + str(Offset) + " Final:" + self.SongKeys[ActualSongKey])

        OutputString=self.SongKeys_Alt[ActualSongKey]
        if IsMinor==1:
            OutputString=OutputString+"m"

        OutputString = OutputString.replace('G#','Ab')
        OutputString = OutputString.replace('A#','Bb')
        #OutputString = OutputString.replace('F#','Gb')
        OutputString = OutputString.replace('D#','Eb')

        # print("Chordstring:"+ChordString+" Offset:"+str(Offset)+" Final:"+OutputString)

        return OutputString

    def DisplaySong(self,SongName):

        #   Locate the song...
        Ptr = 0

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
                #print("ActualSongKey:"+str(ActualSongKey))
                ActualSongKey = ActualSongKey + SongOffset
                #print("ActualSongKey+offset:"+str(ActualSongKey))

                # wrap around if necessary...
                if ActualSongKey > 11:
                    ActualSongKey = ActualSongKey - 12

                #print("ActualSongKey final:"+str(ActualSongKey))

            self.CurrentSong = SongName
            self.CurrentSongKey = SongKey
            self.CurrentOffset = SongOffset

            #   SongText is in 'SongText' variable - chords are defined with lines beginning with '.'
            #   First, split the string on newlines.

            SongTextLines = SongText.split('\n')

            #   Now, go through the lines...

            Ptr2 = 0

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

            SongTextLineNumber=0

            # Work through all the lines of text
            while Ptr2 < (len(SongTextLines)-1):

                #print(Ptr2) # line number - we want to go to next column at row>40
                #print(SongTextLines[Ptr2])

                # Put the line we're working with into a working variable
                TextLine = SongTextLines[Ptr2]

                # If its not a blank line
                if len(TextLine) > 0:

                    # is it a command line?
                    if TextLine[0] == '.':

                        #   Line begins with '.' - it contains chords - need to work through letter by letter

                        Ptr3 = 0    # pointer into the text line
                        OutputLine=''   # converted line

                        # Create a temp line with extra spaces at the end - so we don't read past the end of line.
                        TempLine = TextLine + "   "

                        while Ptr3 < len( TextLine ):

                            NewValue = ord(TextLine[Ptr3])

                            if (NewValue >= 65 and NewValue<=71):
                                # This is a key value

                                # Get the chord
                                NewString = TextLine[Ptr3]

                                #print("0:"+TempLine[Ptr3]+" 1:"+TempLine[Ptr3+1]+" 2:"+TempLine[Ptr3+2])

                                # Check: is this a minor or sharp?
                                if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
                                    NewString=NewString+TextLine[Ptr3+1]
                                    Ptr3=Ptr3+1
                                    # Check: is this a minor or sharp?
                                    if (TempLine[Ptr3+1] == 'M') or (TempLine[Ptr3+1] == '#') or (TempLine[Ptr3+1] == 'b'):
                                        NewString=NewString+TextLine[Ptr3+1]
                                        Ptr3=Ptr3+1

                                # NewString now contains the chord - convert it...
                                UpdatedChord=self.ConvertChord(NewString,SongOffset)

                                OutputLine=OutputLine+UpdatedChord

                            else:
                                OutputLine=OutputLine+TextLine[Ptr3]

                            Ptr3=Ptr3+1

                        # Now put bold around it..
                        OutputLine="<b>"+OutputLine+"</b>"
                    else:
                        OutputLine=TextLine
                else:
                    # its a blank line
                    OutputLine='\n '

                # If we're too far down, go to another display column
                if SongTextLineNumber > 38 or "===" in TextLine:
                    SongTextLineNumber = 1
                    OutputLine = OutputLine+'</td><td>'
                    # print("NewLine")

                TextLine = "<p>"+OutputLine+"&nbsp;&nbsp;&nbsp;&nbsp;</p>"

                #   TextLine.replace('A', 'Ab').replace('Ab', 'G').replace('G', 'Gb').replace('Gb', 'F').replace('F', 'Fb').replace('Fb', 'E').replace('E', 'Eb').replace('Eb', 'D').replace('D', 'Db').replace('Db', 'C').replace('C', 'B').replace('B', 'Bb').replace('Bb', 'A')

                SongText = SongText+'\n'+TextLine

                Ptr2 = Ptr2+1
                SongTextLineNumber=SongTextLineNumber+1


            SongLyricsDisplay = SongText.replace('\n.','<b> ').replace('\n ','</b> ').replace(' ','&nbsp;')

            SongLyricsDisplay = SongLyricsDisplay.replace('SUS','sus')

            SongLyricsDisplay = SongLyricsDisplay.replace('[','<b><font color=''red''>[').replace(']',']</font></b>')

            SongLyricsDisplay = SongTextHeader+ SongLyricsDisplay +'</td></tr></table></body></html>'

            #print(SongLyricsDisplay)

            self.SongText.setText(SongLyricsDisplay)
            self.CurrentKey.setText(self.SongKeys_Alt[ActualSongKey])


    def SongListSelected(self, index):

        #   This is the selected song...
        SelectedString = index.data()

        self.DisplaySong(SelectedString)


    def DelSelectedSong(self):

        # del the currently selected song - i.e. 'self.CurrentSong'

        Result=self.AskQuery("Delete Song?", "Delete "+self.CurrentSong)

        if Result == "YES":
            # Yes - delete the item in the on-screen list
            listItems = self.SongList.selectedIndexes()
            if not listItems:
                return
            for item in listItems:
                self.SongListModel.removeRow(item.row())

            Ptr=0

            while Ptr < len(self.SongDataList):
                if self.SongDataList[Ptr][0] == self.CurrentSong:
                    ToRemove=self.SongDataList[Ptr]
                    self.SongDataList.remove(ToRemove)
                Ptr=Ptr+1

            print("Removed: "+self.CurrentSong)

    def ClearAll(self):

        Result=self.AskQuery("Clear Songlist?", "Clear Songlist?")

        if Result == "YES":
            self.SongListModel.clear()
            self.SongDataList=[]

            print("Cleared")

    def SaveSong(self,SongName):

        FoundPtr=-1
        Ptr=0
        while Ptr < len(self.SongDataList):
            if self.SongDataList[Ptr][0] == self.CurrentSong:
                SingleSongData = self.SongDataList[Ptr]
                FoundPtr=Ptr
            Ptr = Ptr + 1

        if FoundPtr > -1:
            # Found the song to save

            New_FileName = self.SongLocation +'\\'+ SongName
            New_SongText = '<?xml version="1.0" encoding="UTF-8"?>\n'
            New_SongText = New_SongText + '<song>\n'
            New_SongText = New_SongText + '<title>'+SingleSongData[0]+'</title>\n'
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

            with open(New_FileName, 'w') as myfile:
                myfile.write(New_SongText)



    def EditCurrentSong(self):

        FoundPtr=-1
        Ptr=0
        while Ptr < len(self.SongDataList):
            if self.SongDataList[Ptr][0] == self.CurrentSong:
                SingleSongData = self.SongDataList[Ptr]
                FoundPtr=Ptr
            Ptr = Ptr + 1

        if FoundPtr > -1:
            dlg=EditWindow(SingleSongData)
            if dlg.exec_():
                print("Success!")
                self.SongDataList[FoundPtr][0]=dlg.ui.FName.text()
                self.SongDataList[FoundPtr][1]=dlg.ui.SongText.toPlainText()
                self.SongDataList[FoundPtr][2]=dlg.ui.SongKey.currentText()
                self.SongDataList[FoundPtr][3]=0
                self.DisplaySong(self.CurrentSong)
                self.SaveSong(self.CurrentSong)
            else:
                print("Cancel!")

    def NewSong(self):

        SingleSongData=['New Song','.C\n Words','C',0]
        SingleSongData[0] = 'New Song'
        SingleSongData[1] = '.C\n Words'
        SingleSongData[2] = 'C'
        SingleSongData[3] = 0

        dlg = EditWindow(SingleSongData)
        if dlg.exec_():
            print("Success!")
            SingleSongData[0]= dlg.ui.FName.text()
            SingleSongData[1] = dlg.ui.SongText.toPlainText()
            SingleSongData[2] = dlg.ui.SongKey.currentText()
            SingleSongData[3] = 0
            self.SongDataList.append(SingleSongData)
            self.CurrentSong=SingleSongData[0]
            item = QStandardItem(self.CurrentSong)
            self.SongListModel.appendRow(item)
            self.DisplaySong(self.CurrentSong)
            self.SaveSong(self.CurrentSong)
        else:
            print("Cancel!")

    def AddNewSong(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, 'Open file', self.SongLocation, 'OpenFile(*)')

        if fileName and len(fileName[0])>0:

            #   If Windows, change the separator
            FName = fileName[0]
            if os.sep == '\\':
                FName = FName.replace('/', '\\')
            FName = FName.replace(self.SongLocation+'\\', '')
            item = QStandardItem(FName)
            self.SongListModel.appendRow(item)

            #   Read in the song data, to add to the list...

            print("reading file...")

            with open(fileName[0], 'r') as myfile:
                SongData = myfile.read()

            print("getting data")

            tree = ET.ElementTree(ET.fromstring(SongData))

            print("getting lyrics")
            # SongLyrics = tree.getiterator('lyrics')
            SongLyrics = list(tree.iter('lyrics'))
            # SongKey = tree.getiterator('key')
            print("getting key")

            KeyData=tree.find('key')

            if KeyData is None:
                SongKeyValue='C'
            else:
                SongKey = list(tree.iter('key'))
                if SongKey[0].text is None:
                    SongKeyValue = 'C'
                else:
                    SongKeyValue = SongKey[0].text

            print("create list element")
            # Create list element, SongName, LyricsText, Key, OffsetToKey
            print("Filename:"+FName)
            print("Lyrics:"+SongLyrics[0].text)
            print("Key:"+SongKeyValue)

            NewSongData = [FName, SongLyrics[0].text, SongKeyValue, 0]

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

    def UpdatePrefs(self):

        dlg=Prefs(self.SongPreferences)
        if dlg.exec_():
            print("Success!")

            Ptr=0

            while ( Ptr < len(self.SongPreferences)):

                if self.SongPreferences[Ptr][0]=='SONGDIR':
                    self.SongPreferences[Ptr][1]=dlg.ui.SongDirectory.text()

                Ptr=Ptr+1

            SongViewerPreferences = os.getcwd()
            SongViewerPreferences = SongViewerPreferences + '\\OpenSongViewerPrefs.json'

            with open(SongViewerPreferences, 'w') as f:
                json.dump(self.SongPreferences, f)

            # Set up preference variables.
            self.InterpretPreferences

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
