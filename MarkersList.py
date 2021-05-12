
from tkinter import filedialog
from tkinter import *

import os
import csv
#from timecode import Timecode
from SMPTE import SMPTE

s = SMPTE()

trackType = "Video"
ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
config_loc = os.path.join(ScriptDir, "CDL2Resolve_Config.ini")

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()
startFrame = timeline.GetStartFrame()
fps = timeline.GetSetting('timelineFrameRate')
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

aboutText1 = "LiveGrade2Resolve is a resolve script written by Brendon Rathbone to import a folder of CDL's and match them to a timeline of clips for DIT handoff on scripted Television shows."
aboutText2 = "Copyright Brendon Rathbone 2021."
aboutText3 = '<h1>About Dialog</h1>\n<p>Version 1 - May 06 2021</p>\n<p>Notes2Resolve is a simple program to import lists of notes into timeline markers within Davinci Resolve <p>\n<p>Copyright &copy; 2021 Brendon Rathbone.</p>>'

default_LUT = r"/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/Arri/Arri Alexa LogC to Rec709.dat"
TimelineText = "Timeline Clips"
TimelineText = "Timeline Clips - " + timeline.GetName()

dataLoaded = False
prefix = ""
NoteList = []
ColorList = ["Blue","Green","Yellow","Red","Pink","Purple","Fuschia", "Rose","Lavendar","Sky","Mint","Lemon", "Sand", "Cocoa", "Cream","Cyan"]


ColorListVals = {"Blue":[0,0,255],"Green":[0,255,0],"Yellow":[255,255,0],
                 "Red":[255,0,0],"Pink":[255,255,0],"Purple":[85,0,127],"Fuschia":[255,85,127],
                 "Rose":[255,85,127],"Lavendar":[170,170,255],"Sky":[90,140,255],"Mint":[85,170,127],
                "Lemon":[255,255,127], "Sand":[127,117,105], "Cocoa":[80,56,26], "Cream":[255,255,193],"Cyan":[0,255,255]}


FUColors = {}


for k in ColorListVals:
    #print(ColorListVals[k])
    tmpvals = []
    for y in ColorListVals[k]:
        tmpvals.append(float((y+1)/255))
    tmpvals.append(1)
    #print(tmpvals)
    FUColors.update({k:tmpvals})
#print(FUColors)



def Add_Markers_To_Clips(notes):
    global timeline
    global prefix
    itm = dlg.GetItems()
    prefix = itm["Prefix"].Text
    #print("Prefix will be " + prefix)
    trackList = timeline.GetTrackCount("video")
    #print(trackList)
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

    #print(Span_Marks)

    for x in Span_Marks:
        print(x)
        timeline.AddMarker(int(x[0]), str(x[1]), str(x[2]), str(x[3]),int(x[4]))



def TC_Clean(timecode):
    numeric_string = re.sub("[^0-9]", "", timecode)
    TCFormat = ':'.join(numeric_string[i:i+2] for i in range(0, len(numeric_string), 2))
    return TCFormat

def GetCSV(file):
    global NoteList
    global NoteListwColors
    NoteList = []
    with open(file, mode='r',encoding="utf8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # skip the headers
        line_count = 0
        for row in csv_reader:

            NoteList.append(row)

    dataLoaded = True
    NL = []
    for x in NoteList:
        #NL = []
        x[2] = TC_Clean(x[2])
        if x[0] != "":
            NL.append(x)
    NoteList = NL
    Colors = MarkerColors(NoteList)
    print("Color list is: " + str(Colors) )
    NoteListwColors = []
    for x in NoteList:

        for y in Colors:
            if x[1] == y[0]:
                newitem = x[0],x[1],x[2],x[3],y[1]

                NoteListwColors.append(newitem)
    for x in NoteListwColors:
        itRow = itm['Tree'].NewItem()
        itRow.Text[0] = str(x[0])

        itRow.Text[1] = str(x[1])
        itRow.Text[2] = str(x[2])
        itRow.Text[3] = str(x[3])
        itRow.Text[4] = str(x[4])
        itRow.BackgroundColor[4] = {"R": FUColors.get(str(x[4]))[0], "G": FUColors.get(str(x[4]))[1], "B": FUColors.get(str(x[4]))[2], "A": 1}
        itRow.TextColor[4] = {"R":0,"G":0,"B":0,"A":1}
        itm['Tree'].AddTopLevelItem(itRow)




def change_colors(Category, NewColor):
    global NoteListwColors
    NewMarks = []
    for x in NoteListwColors:
        print(x)

        if x[1] == Category:
            tmpitem = x[0],x[1],x[2],x[3],NewColor
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
        if x[0] != "":
            CleanedData.append(x)
    Categories = []
    CatClean = []
    for x in CleanedData:
        Categories.append(x[1])
    [CatClean.append(x) for x in Categories if x not in CatClean]
    Categories = CatClean

    CatColors = []
    for x in Categories:
        CatIndex = Categories.index(x)
        CatColors.append(ColorList[CatIndex])
    CatColorList = tuple(zip(Categories,CatColors))

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
        #ev['item'].Text[0] = ColorSelected




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
                                        ui.Button(
                                            {"ID": "TemplateButton", "Text": "Generate CSV Template", "Weight": 0.5})
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

def ColorSelect(Category, currentColor):

    global ColorList
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
    for x in ColorList:

        itm["ColSel"].AddItem(x)

    def _func(ev):
        print("selecting " + itm["ColSel"].CurrentText + "as new color")
        changes = [Category, itm["ColSel"].CurrentText]
        print("changes are " + str(changes))
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
dlg = disp.AddWindow({"WindowTitle": "Markers2Resolve", "ID": "MyWin", "Geometry": [100, 100, 600, 500], },
                     [
                         ui.VGroup({"Spacing": 2, },
                                   [
                                       # Add your GUI elements here:
                                       ui.Label({"ID": "Timeline", "Text": TimelineText, "Weight": 0.5}),
                                       ui.Tree({"ID": "Tree", "SortingEnabled": True,
                                                "Events": {"ItemDoubleClicked": True, "ItemClicked": True}}),
                                       ui.VGap(0, .2),
                                       ui.HGroup({"Spacing": 2, },
                                                 [
                                                     ui.Button({"ID": "CSVButton", "Text": "Get CSV", "Weight": 0.5}),
                                                    ui.Button({"Weight": "0.25", "ID": 'SelectColorsButton',
                                                  "Text": 'SelectMarkerColors'}),



                                                 ]),
                                        ui.VGap(0, .2),
                                        ui.LineEdit({"ID":"Prefix", "PlaceholderText":"EnterMark Name Prefix"}),
                                        ui.VGap(0, .2),

                                        ui.Button({"ID": "MarksButton", "Text": "Add Marks To Timeline",
                                                                "Weight": 0.5}),
                                        ui.Button({"ID": "ClipsButton", "Text": "Add Marks To Clips span",
                                                                "Weight": 0.5}),
                                       ui.HGap(0, .5),
                                       ui.Label({"ID": "Status", "Text": "Waiting for input", "Weight": 0.5,
                                                 "Alignment": {"AlignHCenter": True}}),
                                       ui.HGap(0, 2),
                                       ui.Button({"Weight": "0.25", "ID": 'AboutDialogButton',
                                                  "Text": 'Show the About Dialog'})

                                   ]),
                     ])

itm = dlg.GetItems()

hdr = itm["Tree"].NewItem()
hdr.Text[0] = 'Event'
hdr.Text[1] = 'Department'
hdr.Text[2] = 'TC'
hdr.Text[3] = 'Description'
hdr.Text[4] = 'Color'

itm["Tree"].SetHeaderItem(hdr)

itm["Tree"].ColumnCount = 5
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
    root = Tk ()
    root.lift()
    root.withdraw()

    file = filedialog.askopenfilename(parent=root, title="Select file",
                                     filetypes=(("CSV files", "*.CSV"), ("all files", "*.*")))

    GetCSV(file)
    root.destroy()




dlg.On.CSVButton.Clicked = _func


def _func(ev):

    itm['Status'].Text = "Getting Markers"

    addMarks(NoteListwColors)
    print("finished")
    itm['Status'].Text = "Finished"


dlg.On.MarksButton.Clicked = _func

def _func(ev):
    prefix = itm["Prefix"].Text
    print("Prefix will be " + prefix)
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
