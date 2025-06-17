# AUTOMOD
## This tool require some setup : 

* For .uassets:
Get this .exe : [uassets](https://github.com/atenfyr/UAssetGUI/releases)  
You shouldn't need to change it, but in resource.py file there is the unreal version used, which is important (I think) for the tool

* For .locres:
1. Get this .exe : [UE4localizationsTool](https://github.com/amrshaheen61/UE4LocalizationsTool/releases/tag/v2.7)  

2. The "template" folder for .pak that we use for modding. (Included in the repo but just in case)

3. Head to Database and edit resources.py in function, to point the patht to those tools, as well as other things.
    I gave guidelines on what's expected at the end of the path.

    There is no package requirements, the tool creates and manage his own venv.
    However Python 3.12 is required at least.

### This tool allows to use reference file(s) to "automate" the process of updating style files (named .uassets) and .locres files.

* Created mods will be named based on the version of foxhole, which have to be manually edited in the resource file.
* Created mods will bear the name of their template/reference (.csv) file.
* One reference file = 1 mod

### There is demo template for .locres and style files. The locsres one is quite simple (2 columns csv : "text_to_find", "replacement_text")
* But the one for style file is way more complex:
* There is 2 part in it, regular RGB replacement from MapStyle is quite easy. But Base, HUD and the rest of Map will require you to do some research on WHERE is what you want to replace. 
1. You can find the number reference for each element on this google sheet: https://docs.google.com/spreadsheets/d/1E8W9mijbKwDHuM73D5bBYRcdp9prEsBpabbaMBvW0B8/edit?gid=0#gid=0 (RGB MapStyle is from 28 to 110 for example)
2. You can use both regular RGB color code (0-255) or UE4 color value, they'll get converted automatically.

Initial .locres and style files must be extracted with Fmodel first. The fmodel output folder must be indicated in the resource.py file

## GUIDE FOR THE Style template.

If the reference you want is a regular icon in Map (28-110), and you want to edit the RGB, you just need to fill the numbers, the faction, and the R, the G and the B.
If they are "identical", you can regroup the numbers (space divider).
(for those DO NOT FILL the file column)

(Use the mapping in the google sheet for the numbers)

If it's from another file, or not 28-110, you'll need more information:
* You need to fill the File column with MapStyle, BaseStyle or HUDStyle (case sensitive)
* You'll need to fill the number column the same way.
* You can ignore faction and RGB.
* Branches are how to "parse" the json/file, how to go deep in it : 2 0 1 means that when you'll go down from the top reference (your number), you'll "open" the third option, then the first one, then the 2 second option (We count from 0 in Python, so first = 0)
* Targets are the name of all the elements you want to replace when you're at the end of your branch.
* If 2 things are on the same numbers, but not at the same "depth", you'll need 2 different lines in the template.

In both cases, Type and Naming are just for you so you don't get lost.


How to use, in short :
* Do the initial settings correctly
* Identify the needs of your mod (which .locres, which style file etc)
* Create the template in the corresponding folder (Style, CodeStrings or Content). It may take some time but you only need to do it once.
* Run the the corresponding .bat
* Get your mod, renamed as it should be, in the Template folder.

(A mod created can use multiple Style files, but not multiple locres, nor both at the same time). You'll need to do some fusions after if you need them.
