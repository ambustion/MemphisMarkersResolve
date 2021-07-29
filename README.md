# ResolveMarkersPanel
Import list of Markers for Davinci Resolve

![](/ScreenCapture2.JPG)

This module allows you to import a Comma Separated List of notes for Davinci Resolve timelines and manipulate markers colors. You can choose to either import individual marks at specific timecodes, or have them span clips located at each timecode. 

Primarily this is used for creating VFX markers and adding notes for grabbing stills or making changes. 

Relies on Igor Ridanovic's module for timecode, located here: https://github.com/IgorRidanovic/smpte/blob/master/SMPTE.py
Just put that in your Resolve Scripting Modules Location and if your scripting environment is set up correctly it should work.

I've also included a basic module for transport control within the script. If you want to jump around to current timeline markers you can double click on any entry within the Current Timeline Markers window. This helps with review. You'll also have to add ResolveTransport.py to your modules folder. 

SCRIPT LOCATIONS:

    Mac OS X:
      - All users: /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
      - Specific user:  /Users/<UserName>/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
    Windows:
      - All users: %PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
      - Specific user: %APPDATA%\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts
    Linux:
      - All users: /opt/resolve/Fusion/Scripts  (or /home/resolve/Fusion/Scripts/ depending on installation)
      - Specific user: $HOME/.local/share/DaVinciResolve/Fusion/Scripts

MODULE LOCATIONS:

    Mac OS X:
    RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

    Windows:
    RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"

    Linux:
    RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    (Note: For standard ISO Linux installations, the path above may need to be modified to refer to /home/resolve instead of /opt/resolve)
