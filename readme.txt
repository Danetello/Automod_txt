This tool require some setup : 

- For .uassets:
Get this .exe :      https://github.com/atenfyr/UAssetGUI/releases 
You shouldn't need to change it, but in resource.py file there is the unreal version used, which is important (I think) for the tool

- For .locres:
Get this .exe :      https://github.com/amrshaheen61/UE4LocalizationsTool/releases/tag/v2.7

- The "template" folder for .pak that we use for modding. (Included in the repo but just in case)

- Head to Database and edit resources.py in function, to point the patht to those tools, as well as other things.
I gave guidelines on what's expected at the end of the path.

There is no package requirements, the tool creates and manage his own venv.
However Python 3.12 is required at least.

----------------

This tool allows to use reference file(s) to "automate" the process of updating style files (named .uassets) and .locres files.

Created mods will be named based on the version of foxhole, which have to be manually edited in the resource file.
Created mods will bear the name of their template/reference (.csv) file.
One reference file = 1 mod

------------------

There is demo template for .locres and style files. The locsres one is quite simple (2 columns csv : "text_to_find", "replacement_text")
But the one for style file is way more complex:
- There is 2 part in it, regular RGB replacement from MapStyle is quite easy. But Base, HUD and the rest of Map will require you to do some research on WHERE is what you want to replace. 
- You can find the number reference for each element on this google sheet: https://docs.google.com/spreadsheets/d/1E8W9mijbKwDHuM73D5bBYRcdp9prEsBpabbaMBvW0B8/edit?gid=0#gid=0 (RGB MapStyle is from 28 to 110 for example)
- You can use both regular RGB color code (0-255) or UE4 color value, they'll get converted automatically.

Initial .locres and style files must be extracted with Fmodel first. The fmodel output folder must be indicated in the resource.py file

