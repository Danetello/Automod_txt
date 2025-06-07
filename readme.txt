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

Initial .locres and style files must be extracted with Fmodel first. The fmodel output folder must be indicated in the resource.py file

