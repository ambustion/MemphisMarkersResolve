# -*- coding: utf-8 -*-

# Memphis Markers - Improved Marker system for Davinci resolve. Import and export markers from Davinci Resolve.
# Copyright 2021, Brendon Rathbone

from tkinter import filedialog
from tkinter import *
import time

import os
import csv
#from timecode import Timecode
from SMPTE import SMPTE
#import ResolveTransport as rt

###env initialization
import sys
import os
from sys import platform
if platform == "linux" or platform == "linux2":
    env = "linux"
    Resolve_Loc = r'/opt/resolve/Developer/Scripting/Modules'
    print("Linux OS")
elif platform == "darwin":
    env = "mac"
    Resolve_Loc=r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules'
    print("System is mac OS")
elif platform == "win32":
    env = "win"
    Resolve_Loc=r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules'
    print("Windows OS")
else:
    print("error getting system platform")
sys.path.insert(1,Resolve_Loc)
import DaVinciResolveScript as bmd

ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
fu = bmd.scriptapp('Fusion')
resolve = bmd.scriptapp('Resolve')
print(resolve)

s = SMPTE()

trackType = "Video"
ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
config_loc = os.path.join(ScriptDir, "MemphisNotes_Config.ini")
# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
MAC_LINE_ENDING =b'\r'

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

ClipsBool = True

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()
startFrame = timeline.GetStartFrame()
fps = timeline.GetSetting('timelineFrameRate')
s.fps = fps
print(fps)
print(startFrame)

print(timeline.GetName())
mediapool = project.GetMediaPool()
bin = mediapool.GetCurrentFolder()
Clips = timeline.GetItemListInTrack()
if not project:
    print("No project is loaded")
    sys.exit()

status_text = ""
Frames_toggle = True
Folder_Name = ""
MetadataList = []
object_List = []
ScriptEMetadataList = []
ClipListNames = []
clip_list = []
CDL_List = []
NoteListwColors = []
colMap = {"Event":0,"Department":1,"timecode":2,"Description":3,"Timecode-out":5}
aboutText2 = "Copyright Brendon Rathbone 2021."
aboutText3 = '<h1>About Dialog</h1>\n<p>Version 0.5 - July 26 2021</p>\n<p>Memphis Markers is a simple program to import lists of notes into timeline markers within Davinci Resolve <p>\n<p>Copyright &copy; 2021 Brendon Rathbone.</p>'
URL = "https://paypal.me/ambustion"

TimelineText = "Timeline Clips"
TimelineText = "Timeline Clips - " + timeline.GetName()

dataLoaded = False
prefix = ""
NoteList = []
MarkerColorList = ["Blue","Green","Yellow","Red","Pink","Purple","Fuschia", "Rose","Lavendar","Sky","Mint","Lemon", "Sand", "Cocoa", "Cream","Cyan"]
ClipColorList = ["Orange","Apricot","Yellow","Lime","Olive","Green","Teal", "Navy","Blue","Purple","Violet","Pink", "Tan", "Beige", "Brown","Chocolate"]

ColorListVals = dict(Blue=[0, 0, 255], Green=[0, 255, 0], Yellow=[255, 255, 0], Red=[255, 0, 0], Pink=[255, 85, 255],
                     Purple=[85, 0, 127], Fuschia=[255, 85, 127], Rose=[255, 85, 127], Lavendar=[170, 170, 255],
                     Sky=[90, 140, 255], Mint=[85, 170, 127], Lemon=[255, 255, 127], Sand=[127, 117, 105],
                     Cocoa=[80, 56, 26], Cream=[255, 255, 193], Cyan=[0, 255, 255], Orange=[255, 85, 0],
                     Apricot=[255, 170, 0], Lime=[170, 255, 0], Olive=[0, 85, 0], Teal=[0, 170, 127],
                     Navy=[0, 0, 127], Violet=[100, 48, 145], Tan=[170, 170, 127], Beige=[245, 245, 184],
                     Brown=[95, 91, 71], Chocolate=[95, 83, 69])

AvidTracks = ["V1","V2","V3","V4","V5","V6","V7","V8"]

FUColors = {}

for k in ColorListVals:
    tmpvals = []
    for y in ColorListVals[k]:
        tmpvals.append(float((y+1)/255))
    tmpvals.append(1)
    FUColors.update({k:tmpvals})


def Add_Colors_To_Clips(notes):
    global timeline
    global prefix
    itm = dlg.GetItems()
    prefix = itm["Prefix"].Text
    trackList = timeline.GetTrackCount("video")
    clipList = []
    for x in range(1,int(trackList)+1):
        tmpclipList = timeline.GetItemListInTrack("video",x)
        if tmpclipList == None:
            print()
        else:
            for y in tmpclipList:
                    clipList.append(y)

    ClipRanges = []
    for x in clipList:
        start = x.GetStart()
        dur = x.GetDuration()
        end = x.GetEnd()
        ClipRanges.append({"start":start,"dur":dur, "end":end})

    Span_Marks = []
    for x in notes:
        for y in ClipRanges:
            if y["start"] < int(s.getframes(x[2])) and y["end"] > int(s.getframes(x[2])):
                padded = x[0].zfill(3)
                name = prefix + padded
                span = y["start"] - startFrame
                Span_Marks.append([span,x[4],name,x[1] + " " + x[3],y["dur"]])

    for x in Span_Marks:
        timeline.AddMarker(int(x[0]), str(x[1]), str(x[2]), str(x[3]),int(x[4]))

def Add_Markers_To_Clips(notes):
    global timeline
    global prefix
    itm = dlg.GetItems()
    prefix = itm["Prefix"].Text
    trackList = timeline.GetTrackCount("video")
    clipList = []
    for x in range(1,int(trackList)+1):
        tmpclipList = timeline.GetItemListInTrack("video",x)
        #print(tmpclipList)
        if tmpclipList == None:
            print()
        else:
            for y in tmpclipList:


                    clipList.append(y)




    ClipRanges = []
    for x in clipList:


        start = x.GetStart()
        dur = x.GetDuration()
        end = x.GetEnd()
        ClipRanges.append({"start":start,"dur":dur, "end":end})

    Span_Marks = []
    for x in notes:
        for y in ClipRanges:
            if y["start"] < int(s.getframes(x[2])) and y["end"] > int(s.getframes(x[2])):

                padded = x[0].zfill(3)
                name = prefix + padded
                span = y["start"] - startFrame
                Span_Marks.append([span,x[4],name,x[1] + " " + x[3],y["dur"]])
    for x in Span_Marks:
        print(x)
        timeline.AddMarker(int(x[0]), str(x[1]), str(x[2]), str(x[3]),int(x[4]))



def TC_Clean(timecode):
    numeric_string = re.sub("[^0-9]", "", timecode)
    TCFormat = ':'.join(numeric_string[i:i+2] for i in range(0, len(numeric_string), 2))
    return TCFormat

def create_table():
    NL = []
    for x in NoteList:
        # NL = []
        x[2] = TC_Clean(x[colMap['Timecode']])
        if x[colMap['Timecode']] != "None":
            x[5] = TC_Clean(x[colMap['Timecode']])
        if x[0] != "":
            NL.append(x)
    NoteList = NL
    Colors = MarkerColors(NoteList)
    print("Color list is: " + str(Colors))
    NoteListwColors = []
    for x in NoteList:
        print(x)
        for y in Colors:
            if x[colMap['Department']] == y[0]:
                print(newitem)
                newitem = x[colMap['Event']], x[colMap['Department']], x[colMap['timecode']], x[colMap['Description']], y[1],x[colMap['Timecode-out']]
                print(newitem)
                NoteListwColors.append(newitem)
    for x in NoteListwColors:
        itRow = itm['Tree'].NewItem()
        itRow.Text[0] = str(x[0])
        itRow.Text[1] = str(x[1])
        itRow.Text[2] = str(x[2])
        itRow.Text[3] = str(x[3])
        itRow.Text[4] = str(x[4])
        itRow.Text[5] = str(x[5])
        #itRow.Text[6] = str(x[6])
        itRow.BackgroundColor[4] = {"R": FUColors.get(str(x[4]))[0], "G": FUColors.get(str(x[4]))[1],
                                    "B": FUColors.get(str(x[4]))[2], "A": 1}
        itRow.TextColor[4] = {"R": 0, "G": 0, "B": 0, "A": 1}
        itm['Tree'].AddTopLevelItem(itRow)

def pickHeaders(columns):
    global NoteList
    global Headers
    global NoteListwColors
    #global colMap
    headerwin = disp.AddWindow(
        {"ID": "headerWin", "WindowTitle": 'Header Selection', "Geometry": [700, 100, 400, 200]},
        [
            ui.VGroup({"ID": 'root'},
                      ## Add your GUI elements here:
                      [
                          # Add your GUI elements here:
                          ui.Label({"ID": "Markers", "Text": "Unknown column layout, please pick headers", "Weight": 0.5}),
                          ui.HGroup({"Weight": "0"},
                                    [
                                        ui.Label({"ID": "Event", "Text": "Event"}),
                                        ui.ComboBox({"ID":"EventCombo"})
                                        ]),
                          ui.HGroup({"Weight": "0"},
                                    [
                                        ui.Label({"ID": "Dept", "Text": "Department"}),
                                        ui.ComboBox({"ID": "DeptCombo"})
                                    ]),
                          ui.HGroup({"Weight": "0"},
                                    [
                                        ui.Label({"ID": "TC", "Text": "Timecode"}),
                                        ui.ComboBox({"ID": "TCCombo"})
                                    ]),
                          ui.HGroup({"Weight": "0"},
                                    [
                                        ui.Label({"ID": "Description", "Text": "Description"}),
                                        ui.ComboBox({"ID": "DescCombo"})
                                    ]),
                          ui.HGroup({"Weight": "0"},
                                    [
                                        ui.Label({"ID": "TCo", "Text": "Timecode-out"}),
                                        ui.ComboBox({"ID": "TCoCombo"})
                                    ]),
                          ui.Button({"ID":"OK", "Text":"OK"})
                      ]),
        ])

    Hitm = headerwin.GetItems()
    for x in columns:
        Hitm['EventCombo'].AddItem(x)
        Hitm['DeptCombo'].AddItem(x)
        Hitm['TCCombo'].AddItem(x)
        Hitm['DescCombo'].AddItem(x)
        Hitm['TCoCombo'].AddItem(x)
    Hitm['EventCombo'].AddItem("None")
    Hitm['DeptCombo'].AddItem("None")
    Hitm['TCCombo'].AddItem("None")
    Hitm['DescCombo'].AddItem("None")
    Hitm['TCoCombo'].AddItem("None")

    Hitm['EventCombo'].SetCurrentIndex(0)
    Hitm['DeptCombo'].SetCurrentIndex(6)
    Hitm['TCCombo'].SetCurrentIndex(1)
    Hitm['DescCombo'].SetCurrentIndex(6)
    Hitm['TCoCombo'].SetCurrentIndex(6)


    def _func(ev):
        global colMap
        colMap = {"Event":Hitm["EventCombo"].CurrentIndex,"Department":Hitm["DeptCombo"].CurrentIndex,"timecode":Hitm["TCCombo"].CurrentIndex,"Description":Hitm["DescCombo"].CurrentIndex,"Timecode-out":Hitm["TCoCombo"].CurrentIndex}
        if Hitm["EventCombo"].CurrentText == "None":
            colMap["Event"] = "None"
        if Hitm["DeptCombo"].CurrentText == "None":
            colMap["Department"] = "None"
        if Hitm["TCCombo"].CurrentText == "None":
            colMap["timecode"] = "None"
        if Hitm["DescCombo"].CurrentText == "None":
            colMap["Description"] = "None"
        if Hitm["TCoCombo"].CurrentText == "None":
            colMap["Timecode-out"] = "None"
        print(colMap)
        #return colMap
        disp.ExitLoop()

    headerwin.On.OK.Clicked = _func

    def _func(ev):
        disp.ExitLoop()

    headerwin.On.headerWin.Close = _func

    headerwin.Show()
    disp.RunLoop()
    headerwin.Hide()

def GetCSV(file):
    global NoteList
    global NoteListwColors
    #global colMap
    NoteList = []
    HeaderList = []
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        HeaderList = fieldnames
    print(HeaderList)

    with open(file, mode='r',encoding="utf8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # skip the headers
        line_count = 0
        for row in csv_reader:

            NoteList.append(row)
    if fieldnames == ['Event','Department','TC','Description']:
        print('standard csv Layout')
    else:
        pickHeaders(HeaderList)
        print(NoteList)
        tmpNoteList = []
        for x in NoteList:
            if colMap["Event"] != "None":
                Event = x[colMap["Event"]]
            else:
                Event = None
            if colMap["Department"] != "None":
                Department = x[colMap["Department"]]
            else:
                Department = None
            if colMap["timecode"] != "None":
                timecode = x[colMap["timecode"]]
            else:
                timecode = None
            if colMap["Description"] != "None":
                Description = x[colMap["Description"]]
            else:
                Description = None
            if colMap["Timecode-out"] != "None":
                tcO = x[colMap["Timecode-out"]]
            else:
                tcO = None

            tmpNoteList.append([Event,Department,timecode,Description,tcO])
        print("printing tmp notelist")
        print(tmpNoteList)
        NoteList = tmpNoteList

        print("print colmap1")
        print(colMap)
    print("printing colmap")
    print(colMap)
    dataLoaded = True
    NL = []
    for x in NoteList:
        print("printing Notelist")
        print(x)
        x[2] = TC_Clean(x[2])
        if x[0] != "":
            NL.append(x)
        else:
            print("x[0] is blank")
    NoteList = NL
    Colors = MarkerColors(NoteList)
    print("Color list is: " + str(Colors) )
    NoteListwColors = []

    for x in NoteList:
        for y in Colors:
            print(y)
            if x[1] == y[0]:
                newitem = x[0],x[1],x[2],x[3],y[1],x[4]
                print("printing newitem")
                print(newitem)
                NoteListwColors.append(newitem)

    for x in NoteListwColors:
        itRow = itm['Tree'].NewItem()
        itRow.Text[0] = str(x[0])
        itRow.Text[1] = str(x[1])
        itRow.Text[2] = str(x[2])
        itRow.Text[3] = str(x[3])
        itRow.Text[4] = str(x[4])
        itRow.Text[5] = str(x[5])
        itRow.BackgroundColor[4] = {"R": FUColors.get(str(x[4]))[0], "G": FUColors.get(str(x[4]))[1], "B": FUColors.get(str(x[4]))[2], "A": 1}
        itRow.TextColor[4] = {"R":0,"G":0,"B":0,"A":1}
        itm['Tree'].AddTopLevelItem(itRow)

def change_colors(Category, NewColor):
    global NoteListwColors
    NewMarks = []
    for x in NoteListwColors:
        print(x)

        if x[1] == Category:
            tmpitem = x[0],x[1],x[2],x[3],NewColor,x[5]
            NewMarks.append(tmpitem)
        else:
            NewMarks.append(x)
    NoteListwColors = NewMarks
    try:
        itm2 = win.GetItems()
    except:
        print()
    itm['Tree'].Clear()
    try:
        itm2['ColorTree'].Clear()
    except:
        print()
    Categories = []
    for x in NoteListwColors:
        print("adding " + str(x))
        itRow = itm['Tree'].NewItem()
        itRow.Text[0] = str(x[0])
        itRow.Text[1] = str(x[1])
        itRow.Text[2] = str(x[2])
        itRow.Text[3] = str(x[3])
        itRow.Text[4] = str(x[4])
        itRow.Text[5] = str(x[5])
        itRow.BackgroundColor[4] = {"R": FUColors.get(str(x[4]))[0], "G": FUColors.get(str(x[4]))[1],
                                    "B": FUColors.get(str(x[4]))[2], "A": 1}
        itRow.TextColor[4] = {"R": 0, "G": 0, "B": 0, "A": 1}
        itm['Tree'].AddTopLevelItem(itRow)
        Categories.append([x[1],x[4]])

    CatClean = []

    [CatClean.append(x) for x in Categories if x not in CatClean]
    print(CatClean)
    for x in CatClean:
        try:
            it2Row = itm2['ColorTree'].NewItem()
            it2Row.Text[0] = str(x[0])
            it2Row.Text[1] = str(x[1])
            itm2['ColorTree'].AddTopLevelItem(it2Row)
        except:
            print()

def MarkDictCleaner():
    markDictclean = []
    timeline = project.GetCurrentTimeline()
    TimelineText = timeline.GetName()
    TLMarks = timeline.GetMarkers()
    for x in TLMarks:
        MarkDict = TLMarks.get(x)
        print(x)
        TC = s.gettc(x + int(startFrame))
        # rint(str(MarkDict["color"]))
        color = str(MarkDict["color"])

        name = str(MarkDict["name"])
        note = str(MarkDict["note"])
        duration = str(MarkDict["duration"])
        customData = str(MarkDict["customData"])
        markDictclean.append({"color":color,"timecode":TC,"name":name,"note":note,"duration":duration,"customData":customData})
    print(markDictclean)
    return markDictclean



def GenerateTemplate():
    print()

def addMarks(Marks):
    global prefix
    global NoteList
    itm = dlg.GetItems()
    prefix = itm["Prefix"].Text
    print("Prefix will be " + prefix)

    cleanList = [sublist for sublist in NoteList if any(sublist)]
    #print(cleanList)
    for x in Marks:
        #print(x)

        Event = str(x[0])
        padded = Event.zfill(3)
        name = prefix+padded

        Description = str(x[3])
        Department = str(x[1])

        Time = x[2]
        frameID = int(s.getframes(x[2])) - int(startFrame)
        color = str(x[4])
        print("marker color will be " + color)
        print("marker to frames " + str(int(s.getframes(x[2]))))
        print("startframe" + str(startFrame))
        print(frameID)


        print("Timecode" + Time)


        timeline.AddMarker(frameID, color, name, Description + " - " + Department, 1)



def MarkerColors(Data):
    CleanedData = []
    for x in Data:
        print(x)
        if x[0] != "":
            CleanedData.append(x)
    Categories = []
    CatClean = []
    for x in CleanedData:
        Categories.append(x[1])

    [CatClean.append(x) for x in Categories if x not in CatClean]
    Categories = CatClean
    print(Categories)
    CatColors = []
    mainitm = dlg.GetItems()
    for x in Categories:
        CatIndex = Categories.index(x)
        if mainitm["CorFBox"].CurrentText == "Markers":
            CatColors.append(ColorList[CatIndex])
        elif mainitm["CorFBox"].CurrentText == "Clip Colors":
            CatColors.append(ClipColorList[CatIndex])
    CatColorList = tuple(zip(Categories,CatColors))
    print(CatColorList)
    return CatColorList

def MarksWindow(Data):
    global win
    for x in Data:
        print(x)
    width, height = 500, 250
    win = disp.AddWindow(
        {"ID": "MarksWin", "WindowTitle": 'Marker Color Selection', "Geometry": [700, 100, 400, 100]},
        [
            ui.VGroup({"ID": 'root'},
                      ## Add your GUI elements here:
                      [
                          # Add your GUI elements here:
                          ui.Label({"ID": "Markers", "Text": "Please Select Marker Colors", "Weight": 0.5}),
                          ui.Tree({"ID": "ColorTree", "SortingEnabled": True,
                                   "Events": {"ItemDoubleClicked": True, "ItemClicked": True}}),
                      ]),
        ])

    itm = win.GetItems()
    mainitm = dlg.GetItems()
    MarkerColors(NoteList)
    col = itm["ColorTree"].NewItem()
    col.Text[0] = 'Category'
    col.Text[1] = 'Color'

    itm["ColorTree"].SetHeaderItem(col)

    itm["ColorTree"].ColumnCount = 2
    ###Resize the Columns
    itm['ColorTree'].ColumnWidth[0] = 90
    itm['ColorTree'].ColumnWidth[1] = 90
    for x in Data:
        itRow = itm['ColorTree'].NewItem()
        itRow.Text[0] = str(x[0])
        itRow.Text[1] = str(x[1])
        itRow.BackgroundColor[1] = {"R": FUColors.get(str(x[1]))[0], "G": FUColors.get(str(x[1]))[1],
                                    "B": FUColors.get(str(x[1]))[2], "A": 1}
        itRow.TextColor[1] = {"R": 0, "G": 0, "B": 0, "A": 1}
        itm['ColorTree'].AddTopLevelItem(itRow)
    ###close the Marks window
    def _func(ev):
        print('[Double Clicked] ' + str(ev['item'].Text[0]) + " " + str(ev['item'].Text[1]))
        ColorSelected = ColorSelect(ev['item'].Text[0],ev['item'].Text[1])
        print("selected color for " + ColorSelected[0] + " is "+ ColorSelected[1])
    win.On.ColorTree.ItemDoubleClicked=_func
    def _func(ev):
        disp.ExitLoop()

    win.On.MarksWin.Close = _func

    win.Show()
    disp.RunLoop()
    win.Hide()


def AboutWindow():
    width, height = 500, 250
    win = disp.AddWindow(
        {"ID": "AboutWin", "WindowTitle": 'About Dialog', "Geometry": "{200, 200, 200, 100}"},
        [
            ui.VGroup({"ID": 'root'},
                      ## Add your GUI elements here:
                      [
                          ui.TextEdit({"ID": 'AboutText', "ReadOnly": "true",
                                       "Alignment": "{AlignHCenter = true,AlignTop = true}", "HTML": aboutText3}),
                          ui.VGroup({"Weight": "0"},
                                    [

                                    ui.Label({"ID": "EMAIL", "Text": aboutText2,
                                              "Alignment": "{AlignHCenter = true, AlignTop = true}", "WordWrap": "true",
                                              "OpenExternalLinks": "true"}),
                                        ui.Label({"ID" : "URL", "Text":f"Buy me a Coffee: <a href={URL}>{URL}</a>",
                                                  "Alignment": {"AlignHCenter":True, "AlignTop":True},"OpenExternalLinks" : True,}),
                                        ]),
                      ]),
        ])

    itm = win.GetItems()



    ###close the about window
    def _func(ev):
        disp.ExitLoop()

    win.On.AboutWin.Close = _func

    win.Show()
    disp.RunLoop()
    win.Hide()

def AvidMarkerExport(dict,track):
    #TLitm = TLwin.GetItems()
    savePath = fu.RequestDir()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = TimelineText + "_Markers_avid_" + timestr + ".txt"
    #track = itm["AvidTrack"].GetCurrentText()
    print("current track is: "+ track)
    fullFilename = os.path.join(savePath + file)
    avidColors = ['red','green','blue','yellow','magenta','cyan','black','white']


    with open(fullFilename, 'w', newline='\n',encoding='utf-8') as outcsv:
        writer = csv.writer(outcsv,delimiter='\t')
        for x in dict:
            if x['color'].lower() in avidColors:
                print(x)
                writer.writerow([x["name"],x["timecode"],track,x["color"].lower(),x["note"], x["duration"]])
            else:
                writer.writerow([x["name"],x["timecode"],track,'black',x["note"], x["duration"]])
    with open(fullFilename, 'rb') as open_file:
        content = open_file.read()

    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    content = content.replace(MAC_LINE_ENDING, UNIX_LINE_ENDING)

    with open(fullFilename, 'wb') as open_file:
        open_file.write(content)
    print("exporting avid txt")

def CSVExport(dict):
    savePath = fu.RequestDir()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = TimelineText + "_Markers_"+timestr+".csv"
    fullFilename = os.path.join(savePath + file)
    with open(fullFilename, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv,encoding="latin1")
        writer.writerow(["Color", "Timecode", "Name","Note","Duration","customData"])
        for x in dict:
            writer.writerow([x["color"],x["timecode"],x["name"],x["note"].encode("latin1","ignore"),x["duration"],x["customData"]])
    print("exporting generic CSV")

def TLMarkWin():
    timeline = project.GetCurrentTimeline()
    TimelineText = timeline.GetName()
    TLMarks = timeline.GetMarkers()
    #print(TLMarks)
    def GetCurrentMarks():


        col = itm["TLTree"].NewItem()
        col.Text[0] = 'color'
        col.Text[1] = 'timecode-in'
        col.Text[2] = 'name'
        col.Text[3] = 'note'
        col.Text[4] = 'duration'
        col.Text[5] = 'customData'
        col.Text[6] = 'timecode-out'

        itm["TLTree"].SetHeaderItem(col)

        itm["TLTree"].ColumnCount = 7
        ###Resize the Columns
        itm["TLTree"].ColumnWidth[0] = 90
        itm["TLTree"].ColumnWidth[1] = 90
        itm["TLTree"].ColumnWidth[2] = 90
        itm["TLTree"].ColumnWidth[3] = 300
        itm["TLTree"].ColumnWidth[4] = 90
        itm["TLTree"].ColumnWidth[5] = 90
        for x in TLMarks:
            itRow = itm['TLTree'].NewItem()
            MarkDict = TLMarks.get(x)

            TC = s.gettc(x + int(startFrame))

            itRow.Text[0] = str(MarkDict["color"])
            itRow.Text[1] = str(TC)
            itRow.Text[2] = str(MarkDict["name"])
            itRow.Text[3] = str(MarkDict["note"])
            itRow.Text[4] = str(MarkDict["duration"])
            itRow.Text[5] = str(MarkDict["customData"])
            
            itm['TLTree'].AddTopLevelItem(itRow)
        #return TLMarks




    width, height = 500, 250
    TLwin = disp.AddWindow(
        {"ID": "AboutWin", "WindowTitle": 'Current Timeline Markers', "Geometry": [800, 100, 1000, 300]},
        [
            ui.VGroup({"ID": 'root', "Spacing": 2, },
                      ## Add your GUI elements here:
                      [
                          ui.Label({"ID": "Timeline", "Text": TimelineText, "Weight": 0.5}),
                          ui.Tree({"ID": "TLTree", "SortingEnabled": True, "Weight": 2,
                                   "Events": {"ItemDoubleClicked": True, "ItemClicked": True}}),
                          ui.VGap(0, .2),
                          ui.HGroup({"Spacing": "2","Alignment": {"AlignHCenter": True}},
                                    [
                                        ui.VGap(0, .2),
                                    ui.Button({"ID": "AvidExport","Text": "Export to Avid", "Weight": 0}),
                                        ui.ComboBox({"ID": "AvidTrack","Weight": 0}),
                                    ui.Button({"ID": "CSVExport", "Text": "Export Generic CSV", "Weight": 0}),
                                        ui.HGap(0, .5),

                                        #ui.Button(
                                            #{"ID": "TemplateButton", "Text": "Generate CSV Template", "Weight": 0.5})
                                        ]),
                          ui.VGap(0, .2),
                          ui.Label({"ID": "dblClick", "Text": "Double Click to go to note('color or deliver page only!)", "Weight": 2,"Alignment": {"AlignHCenter": True}}),
                      ]),
        ])

    itm = TLwin.GetItems()
    TLMarks = GetCurrentMarks()
    for x in AvidTracks:
        itm["AvidTrack"].AddItem(x)

    ###close the about window
    def _func(ev):
        disp.ExitLoop()

    TLwin.On.AboutWin.Close = _func

    def _func(ev):
        print(ev['item'].Text[1])
        timeline.SetCurrentTimecode(ev['item'].Text[1])

    TLwin.On.TLTree.ItemDoubleClicked = _func

    def _func(ev):
        cleanMarks = MarkDictCleaner()
        track = itm['AvidTrack'].GetCurrentText()
        AvidMarkerExport(cleanMarks,track)

    TLwin.On.AvidExport.Clicked = _func

    def _func(ev):
        cleanMarks = MarkDictCleaner()
        CSVExport(cleanMarks)

    TLwin.On.CSVExport.Clicked = _func

    TLwin.Show()
    disp.RunLoop()
    TLwin.Hide()

def ColorSelect(Category, currentColor):

    global MarkerColorList
    global colwin

    width, height = 500, 250
    colwin = disp.AddWindow(
        {"ID": "ColorSelectWin", "WindowTitle": 'SelectColor', "Geometry": [1100, 100, 400, 100]},
        [
            ui.VGroup({"ID": 'root'},
                      ## Add your GUI elements here:
                      [
                                    ui.Label({"ID": "ColTitle", "Text": "Please Select A Color for " + Category,
                                              "Alignment": "{AlignHCenter = true,AlignTop = true}", "WordWrap": "true",
                                              "OpenExternalLinks": "true"}),
                        ui.ComboBox({"ID":"ColSel", }),
                          ui.Button({"ID": "SubmitColor","Text": "Submit", "Weight": 0.5})

                      ]),
        ])
    itm = colwin.GetItems()
    mainitm = dlg.GetItems()
    if mainitm["CorFBox"].CurrentText == "Markers":
        for x in MarkerColorList:
            itm["ColSel"].AddItem(x)
    elif mainitm["CorFBox"].CurrentText == "Clip Colors":
        for x in ClipColorList:
            itm["ColSel"].AddItem(x)

    def _func(ev):
        print("selecting " + itm["ColSel"].CurrentText + "as new color")
        changes = [Category, itm["ColSel"].CurrentText]
        change_colors(changes[0],changes[1])
        disp.ExitLoop()
    colwin.On.SubmitColor.Clicked = _func
    ###close the about window
    def _func(ev):
        disp.ExitLoop()
    colwin.On.ColorSelectWin.Close = _func

    colwin.Show()
    disp.RunLoop()
    colwin.Hide()


###initialize main window
dlg = disp.AddWindow({"WindowTitle": "Memphis Markers", "ID": "MyWin", "Geometry": [100, 100, 600, 500], },
                     [
                         ui.VGroup({"Spacing": 2, },
                                   [
                                       # Add your GUI elements here:
                                       ui.TabBar({"ID":"TabBar"}),

                                       ui.Label({"ID": "Timeline", "Text": TimelineText, "Weight": 0.5}),
                                       ui.Tree({"ID": "Tree", "SortingEnabled": True,
                                                "Events": {"ItemDoubleClicked": True, "ItemClicked": True}}),
                                       ui.VGap(0, .2),
                                       ui.HGroup({"Spacing": 2, },
                                                 [
                                                     ui.Button({"ID": "CSVButton", "Text": "Get CSV", "Weight": 0.5}),
                                                    ui.Button({"Weight": "0.25", "ID": 'SelectColorsButton',
                                                  "Text": 'Select Colors'}),
                                                     ui.ComboBox({"ID":"CorFBox"})



                                                 ]),
                                        ui.VGap(0, .2),
                                        ui.LineEdit({"ID":"Prefix", "PlaceholderText":"Enter Mark Name Prefix"}),
                                        ui.VGap(0, .2),

                                        ui.Button({"ID": "MarksButton", "Text": "Add Marks To Timeline",
                                                                "Weight": 0.5}),
                                        ui.Button({"ID": "ClipsButton", "Text": "Add Marks To Clips span",
                                                                "Weight": 0.5}),
                                       ui.Button({"ID": "ColorsButton", "Text": "Add Colors To Clips",
                                                  "Weight": 0.5}),
                                       ui.HGap(0, .5),
                                       ui.Label({"ID": "Status", "Text": "Waiting for input", "Weight": 0.5,
                                                 "Alignment": {"AlignHCenter": True}}),
                                       ui.HGap(0, 2),
                                        ui.Button({"Weight": "0.25", "ID": 'TLButton',
                                                  "Text": 'Current Timeline Markers'}),
                                        ui.HGap(0, 2),
                                       ui.Button({"Weight": "0.25", "ID": 'AboutDialogButton',
                                                  "Text": 'Show the About Dialog'})


                                   ]),
                     ])

itm = dlg.GetItems()
itm['TabBar'].AddTab()
itm["CorFBox"].AddItem("Markers")
itm["CorFBox"].AddItem("Clip Colors")


hdr = itm["Tree"].NewItem()
hdr.Text[0] = 'Event'
hdr.Text[1] = 'Department'
hdr.Text[2] = 'TC'
hdr.Text[3] = 'Description'
hdr.Text[4] = 'Color'
hdr.Text[5] = 'TC-Out'

itm["Tree"].SetHeaderItem(hdr)

itm["Tree"].ColumnCount = 6
###Resize the Columns
itm['Tree'].ColumnWidth[0] = 90
itm['Tree'].ColumnWidth[1] = 90
itm['Tree'].ColumnWidth[2] = 90
itm['Tree'].ColumnWidth[3] = 90
itm['Tree'].ColumnWidth[3] = 90




# Close Main Window
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# Add your GUI element based event functions here:
def _func(ev):
    TLMarkWin()
dlg.On.TLButton.Clicked = _func

def _func(ev):
    root = Tk ()
    root.lift()
    root.withdraw()
    file = fu.RequestFile()
    GetCSV(file)
    root.destroy()
dlg.On.CSVButton.Clicked = _func

def _func(ev):
    MarkerColors(NoteList)
    create_table()
dlg.On.CorFBox.CurrentIndexChanged = _func

def _func(ev):
    itm['Status'].Text = "Getting Colors and adding metadata..."
    Add_Colors_To_Clips(NoteListwColors)
    itm['Status'].Text = "Finished"
dlg.On.MarksButton.Clicked = _func

def _func(ev):
    itm['Status'].Text = "Getting Markers"
    addMarks(NoteListwColors)
    itm['Status'].Text = "Finished"
dlg.On.MarksButton.Clicked = _func

def _func(ev):
    prefix = itm["Prefix"].Text
    Add_Markers_To_Clips(NoteListwColors)
dlg.On.ClipsButton.Clicked = _func

def _func(ev):
    MC = MarkerColors(NoteList)
    MarksWindow(MC)
dlg.On.SelectColorsButton.Clicked = _func

def _func(ev):
    ColorSelected = ColorSelect(ev['item'].Text[1], ev['item'].Text[4])
dlg.On.Tree.ItemDoubleClicked=_func

def _func(ev):
    AboutWindow()
dlg.On.AboutDialogButton.Clicked = _func

dlg.Show()
disp.RunLoop()
dlg.Hide()
