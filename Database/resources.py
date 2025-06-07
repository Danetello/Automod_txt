import os

foxholeversion = "V61"
ue_ver = "VER_UE4_27"

# main folder \Automod_txt
automodtxt_path = r"C:\Users\Max\Documents\Automod_txt" #CUSTOM

# Where stuff will be stored
version_folder = os.path.join(automodtxt_path, "Result", foxholeversion)

# Where fmodel store   \Output\Exports
Fmodel_output_folder = r"C:\Users\Max\Downloads\DLs\Output\Exports" #CUSTOM


# Template tool for .pak   \Template
template_folder = r"C:\Users\Max\Documents\Automod_txt\Template" #CUSTOM
war_pak_folder = os.path.join(template_folder, r"War")

locres_pak_folder = os.path.join(template_folder, r"War\Content\Localization") 
uasset_pak_folder = os.path.join(template_folder, r"War\Content\Slate\Styles") 

result_init_name = "War-WindowsNoEditor_p.pak"
bat_path = os.path.join(template_folder, "run.bat")


### .uasset resources

style_folder = os.path.join(automodtxt_path, r"Database\Style")
tool_executable = r"D:\backup\Image\modding\Utilities-master" #CUSTOM do not include UAssetGUI.exe in the path

### .locres resources \Utilities-master

tool_path = r"D:\backup\Image\modding\Utilities-master" #CUSTOM do not include UE4LocalizationsTool.exe in the path

