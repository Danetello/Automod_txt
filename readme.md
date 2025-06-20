# AUTOMOD_TXT

---

- [AUTOMOD\_TXT](#automod_txt)
  - [Tool Setup](#tool-setup)
  - [Dependencies](#dependencies)
    - [Required](#required)
    - [Required (Depending on use case)](#required-depending-on-use-case)
  - [How To Use](#how-to-use)
    - [.Locres Use Case](#locres-use-case)
    - [.Uasset Use Case](#uasset-use-case)
      - [Understanding the Example File](#understanding-the-example-file)
    - [Summarized Workflow](#summarized-workflow)

---

## Tool Setup

- Before making changes for your specific use case, first edit the following variables in `./Database/resources.py`.
  - Set `automodtxt_path` in `line 7` to the absolute file path of the current application directory.
  - Set `Fmodel_output_folder` in `line 13` to the absolute file path of the export folder for [FModel](https://fmodel.app/) to the file level of `./Output/Export`.
  - Set `template_folder` in `line 17` to the absolute file path of your [Template Packer](https://drive.google.com/file/d/1VBHwGTtEZyMP_vDioHa1eamu481YxyiD/view) folder. You can also point it to the absolute file path of `./Template`, as there also exists a full copy of the Template Packer there.
  - Set `foxholeversion` in `line 3` to the current game version. This will be used in the auto naming of the generated mod alongside what type mod it was.

- To edit .uassets files, the following is required.
  - Download the [UAssetGUI](https://github.com/atenfyr/UAssetGUI/releases) application.  
  - In `./Database/resources.py`, the following needs to be edit.
    - Set the `ue_ver` variable in `line 4` to your version of UE4 if you use a different version than UE4.27.
    - Set the `tool_executable` variable in `line 30` to the absolute file path of your install directory for the UAssetGUI application. Note: This is only the folder path and you should not include the .exe in the path.
  - You will need to export the style files, using [FModel](https://fmodel.app/), in .uasset format.

- To edit .locres files, the following is required.

  - Download the [UE4localizationsTool](https://github.com/amrshaheen61/UE4LocalizationsTool/releases/tag/v2.7) application.  

  - In `./Database/resources.py`, the following needs to be edit.
    - Set the `tool_path` variable in `line 34` to the absolute file path of the UE4localizationsTool install folder, to the `./Utilities-master` level. Make sure not to include the application .exe in this file path.
  - You will need to export the .locres files using [FModel](https://fmodel.app/).

If you are unsure of how some file paths should look, the `./Database/resources.py` file contains some hints that might help.

## Dependencies

### Required

    - Python 3.12
    - FModel
    - Template Packer (If you don't want to use the included one)

### Required (Depending on use case)

    - UAssetGUI (.uassets)
    - UE4localizationsTool (.locres)

## How To Use

### .Locres Use Case

The .locres is simple to use and has two columns, as shown in the table below.

| text_to_find | replacement_text |
|--------------|------------------|
| Bluefin      | Blåhaj           |

### .Uasset Use Case

The workflow for this use case is centred around the .`/Style` folder. Inside this folder you will initially find the `TEMPLATE_EXAMPLE_UASSET.csv` file. This contains some basic examples of how this tool is intended to be used. It's a good idea to keep a copy of this file, but you probably don't want to keep it in the folder for reasons that will quickly become apparent.

This tool allows for multiple different variations of style mods to be generated consecutively. Each `.csv` file that's placed in the `./Style` folder will prompt the tool to create a separate mod based on its contents.  

#### Understanding the Example File

In the `TEMPLATE_EXAMPLE_UASSET.csv` file you will find 11 columns, as seen in the table below.

| File | Naming | Number | Faction | R | G | B | Type | Branches | Target | Values |
|------|--------|--------|---------|---|---|---|------|----------|--------|--------|

- `File` indicates the specific style file you want to edit. (3 possibilities: MapStyle, BaseStyle, HUDStyle - case sensitive)
- `Naming` is where you can give a name that will describe the edit that will be made in this line. This value is not actually used in the program, but more for later reference.
- `Number` is a bit complicated:
  - First, it indicates the line number of the value that you want to edit.
    - You will need to open the Style file yourself and count out each index position of hte value you want to later edit.
    - Another option is to use this [Google Sheet](https://docs.google.com/spreadsheets/d/1E8W9mijbKwDHuM73D5bBYRcdp9prEsBpabbaMBvW0B8/edit?gid=0#gid=0) as reference as it already has the calculated index position of the contents of all the style file.
  - Second, you can group together duplicate edits to multiple index position by placing them in a space separated list in the same row, for this specific column. (Separator for multiple value must be " ")
- `Faction` is only used when making map file for "REGULAR RGB" (see Google Sheet). Specifying `Colonial` or `Warden` will indicate to the program which part of the specified value to edit. If the icon is faction agnostic, then this can be left open.
- `R`, `G` and `B` are used to specify the color you want it to be changed to. This can be indicated in standard RGB code (0-255) or in linear RGB code (0.0-1.0) as the script will automatically convert between the two. This is only used for icon color edits of the `MapStyle` file. Also used only for "REGULAR RGB".
- `Type` is used to indicate the type of value you want to edit. Only one possible value is important, setting "RGB" if it's a color edit (and not a "REGULAR RGB" one of the MapStyle). Any other value will just be indicative.
- `Branches` are used to further indicate the position of the value you want to edit. This value is not relevant to the faction icon color edits of the `MapStyle` file as there are custom scripts to specifically handle them. 
  - Branches indicate to the application how to "parse" the style file by indicating positions at incremental depths. So, for 2 0 1, it means that, from the position indicated by the number column, you will choose the 3rd option in it(Counted from 0). Then, it will go the the first option of that one. Then, it will go to the second option of that one. (Separator must be " ")
  - If you need unique branch handling for each index number you indicate, then they will all need to be in their own rows and can not be grouped together for convenience.
- `Target` indicate the name of the value that needs to be edited, it can be "R, G, B" for a color, but "X" and "Y" for image size. You only need to remove one of the names to prevent it from being edited. (Separator must be ", ")
This value is not relevant to the faction icon color edits of the `MapStyle` file as there are custom scripts to specifically handle them. (the "REGULAR RGB" ones) 
- `Values` are used to indicate the new value as you specified in the `Target` column. It can be of any type depending of your target (Integer, Float or String); though RGB value can also see the input being made in standard RGB code (0-255), as if "RGB" is specified in type, value will be converted if needed (If you put "RGB" and Linear RGB value, it will also works). (Separator must be ", ")
This value is not relevant to the faction icon color edits of the `MapStyle` file as there are custom scripts to specifically handle them. (the "REGULAR RGB" ones)

### Summarized Workflow

- Complete the initial tool setup.
- Identify the needs of your mod, such as which .locres and style files you will use.
- Create the template in the corresponding folder (Style, CodeStrings or Content) by copying and then editing the example .csv. It may take some time but you only need to do it once.
- Run the the corresponding .bat to launch the tool. The tool will automatically make the mod for you as well.
- Take your created mod in the `./Template` folder, or where you specified it in the `./Database/resources.py` file. Rename to what you want. (Though it shouldn't be needed as it will follow the name of the template)
- You can edit and have multiple style files, of different types, into one mod, but for .locres, each file is handled separately, one template per file, so one file per mod (You can merge the 2 mods after without issues).
