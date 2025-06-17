import os
import subprocess
import sys

print("Current working directory:", os.getcwd())

# Function to install a package if it's not already installed
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

# Install Pillow if not already installed
install_package('pandas')

import re
import pandas as pd
from pandas.api.types import is_object_dtype, is_numeric_dtype
import os
import shutil
import subprocess
import json
import copy

from Database.resources import foxholeversion, ue_ver, version_folder, automodtxt_path, Fmodel_output_folder
from Database.resources import template_folder, bat_path,  uasset_pak_folder, war_pak_folder, result_init_name
from Database.resources import style_folder, tool_executable

# create the version folder if not done yet
os.makedirs(version_folder, exist_ok=True)

# create all the path that will be used to read/create .uassets & .jsons
MapStyle_file_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\MapStyle.uasset")
HUDStyle_file_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\HUDstyle.uasset")
BaseStyle_file_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\BaseStyle.uasset")

json_Map_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\JsonMapstyle.json")
json_HUD_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\JsonHUDstyle.json")
json_Base_path = os.path.join(Fmodel_output_folder, r"War\Content\Slate\Styles\JsonBasestyle.json")

# stuff that serves for RGB part
factions = {"Colonial" : -3,
            "Warden" : -2}

# will allow to iterate between the json and uassets
location_dic = {
    "MapStyle" : [MapStyle_file_path, json_Map_path],
    "BaseStyle" : [BaseStyle_file_path, json_Base_path],
    "HUDStyle" : [HUDStyle_file_path, json_HUD_path]
}

tool_executable = os.path.join(tool_executable, r"UAssetGUI.exe")

# to make sure our json are compatible with the base material from .uassets
def convert_like(reference_value, input_value):
    ref_type = type(reference_value)

    if ref_type == int:
        return int(float(input_value))
    elif ref_type == float:
        return float(input_value)
    elif ref_type == bool:
        return str(input_value).lower() in ['true', '1']
    elif ref_type == str:
        return str(input_value)
    else:
        raise TypeError(f"Unsupported type: {ref_type}")

# convert regular RGB to UE4 color format
def ue4_fcolor2flinearcolor(i: float) -> float:
    i = i /255
    if i > 0.04045:
        return pow(i * (1.0 / 1.055) + 0.0521327, 2.4)
    else:
        return i * (1.0 / 12.92)

# open the mod template .csv and extract the infos needed from it (and format them)
for modfile in os.listdir(style_folder):
    file_path = os.path.join(style_folder, modfile)
    file_name = modfile[:-4]
    
    print(f"----------------------------------------{modfile}----------------------------------------")

    mod_directory = os.path.join(version_folder, file_name)
    os.makedirs(mod_directory, exist_ok=True)

    df_mod_data = pd.read_csv(file_path)
    df_mod_data.drop(columns = "Naming (not used)", inplace=True)
    
    cols_to_object = [
        "File", "Number (list)", "Faction", "Type",
        "Branches", "Target", "Values"]
    
    for col in cols_to_object:
        df_mod_data[col] = df_mod_data[col].astype("object")
    
    for col in df_mod.columns:
        if is_numeric_dtype(df_mod_data[col]):
            df_mod_data[col] = df_mod_data[col].fillna(0.0)
        elif is_object_dtype(df_mod_data[col]):
            df_mod_data[col] = df_mod_data[col].fillna("")
    
    for col in cols_to_object:
        df_mod_data[col] = df_mod[col].astype("object")
    
    cols_to_split = ["Number (list)", "Branches"]
    for col in cols_to_split:
        df_mod_data[col] = df_mod_data[col].apply(lambda x: [int(i) for i in str(x).split(" ") if i.isdigit()])
    
    df_mod_data["Values"] = df_mod_data["Values"].apply(lambda x: x.split(", "))
    df_mod_data["Target"] = df_mod_data["Target"].apply(lambda x: x.split(", "))
    df_mod_data["File"] = df_mod_data["File"].apply(lambda x: x.strip(" "))
 
    ######## Creating the .jsons

    for style in location_dic:
        style_path = location_dic[style][0]
        json_path = location_dic[style][1]
    
        command = [tool_executable, "tojson", style_path, json_path, ue_ver]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error at json phase {json_path}: {e.stderr}")
        except Exception as e:
            print(f"Error at json phase: {str(e)}")

    df_mod = df_mod_data.copy(deep=True)

    ### REGULAR Map RGB
    print("\n### REGULAR Map RGB \n")
    
    with open(json_Map_path) as f:
        data = json.load(f)
    
    RGB = ["R", "G", "B"]

    RGB_bool = df_mod[df_mod["Faction"] != ""].empty # log if RGB part is used for the mod or not
    
    for faction in factions:
        df_mod_small = df_mod[df_mod["Faction"] == faction]
    
        for idx in df_mod_small.index: # iteration through the world map elements to edit
            target = df_mod_small.loc[idx, "Number (list)"] 
            for reference in target :
                reference = int(reference)
    
                print(reference, faction)
    
                for color in RGB : 
                    color_ref = df_mod_small.loc[idx, color]
                    
                    data_target = data['Exports'][0]['Data'][0]['Value'][reference]['Value'][factions[faction]]["Value"][1]["Value"][0]["Value"][0]["Value"][color] 
    
                    if isinstance(data_target, float) and 0 <= color_ref <= 255: # convert the color data if needed
                            color_ref = ue4_fcolor2flinearcolor(color_ref)
    
                    print(color_ref)
    
                    data['Exports'][0]['Data'][0]['Value'][reference]['Value'][factions[faction]]["Value"][1]["Value"][0]["Value"][0]["Value"][color] = convert_like(data_target, color_ref)
                    
    with open(json_Map_path, 'w') as f: #save the edited .json after RGB step
        json.dump(data, f, separators=(',', ':'))    
    
    
    ### Other
    print("\n### Other \n")
    
    df_mod_other = df_mod[df_mod["Faction"] == ""]
    df_mod_other

    file_list = df_mod_other["File"].unique()

    partial_location_dic = {"MapStyle" :  location_dic["MapStyle"]} if not RGB_bool else {} #if RGB is used, manually add BaseStyle in case not used later, so the file is created
    partial_location_dic = {k: location_dic[k] for k in file_list if k in location_dic}
    
    for file in file_list: # start iteration between the style files jsons
        json_path = location_dic[file][1]
    
        print(file)
    
        with open(json_path) as f:
            data = json.load(f)
    
        df_style = df_mod[df_mod["File"] == file]
            
        for idx in df_style.index:
            target = df_style.loc[idx, "Number (list)"] 
            print(idx, target)
            for reference in target :
                reference = int(reference)
    
                path = ["Exports", 0, "Data", 0, "Value", reference]
    
                depth = df_style.loc[idx, "Branches"]
                targets = df_style.loc[idx, "Target"]
                values = df_style.loc[idx, "Values"]
                
                for i in range(len(depth)):
                    path.extend(["Value", int(depth[i])])  #build the path for json parsing and reach target
                    
                path.extend(["Value"])
    
                result = data
                for key in path:
                    result = result[key]
                
                print(result)
    
                for j in range(len(targets)):   
                    try:
                        values[j] = int(values[j])
                        
                        if isinstance(result[targets[j]], float) and isinstance(values[j], int) and 0 <= values[j] <= 255: # convert the color data if needed
                            values[j] = float(values[j])
                            
                            values[j] = ue4_fcolor2flinearcolor(values[j])
                            
                        print("RGB convert ok")
                        
                    except (ValueError, TypeError, StopIteration):
                        print("skip convert")
                        pass
                    
                    result[targets[j]] = convert_like(result[targets[j]], values[j])
                
                print("------------------------------")
                
        with open(json_path, 'w') as f:
            json.dump(data, f, separators=(',', ':'))

    ######## Creating the .uassets

    uasset_result_list = {}

    for style in partial_location_dic:
        style_path = partial_location_dic[style][0]
        json_path = partial_location_dic[style][1]
    
        
        style_name = re.search(r'\\Styles\\(.+)', style_path).group(1)
        style_result = os.path.join(mod_directory, style_name)

        uasset_result_list[style_name] = style_result
    
        command = [tool_executable, "fromjson", json_path, style_result]
    
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"File created: {style_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error with the .uasset command : {e.stderr}")
        except Exception as e:
            print(f"Error happened during .uassets phase : {str(e)}")

    ######## Creating the mod

    #create the template correct folders (delete war first)
    
    shutil.rmtree(war_pak_folder)
    os.makedirs(uasset_pak_folder, exist_ok=True)

    #move the files copy

    for file in uasset_result_list.keys():
        
        file_copy = os.path.join(uasset_pak_folder, file)
        shutil.copy(uasset_result_list[file], file_copy)
        
    #use the .bat

    result_path = os.path.join(template_folder, result_init_name)
    result_name = "War-WindowsNoEditor_"+ foxholeversion + "_" + file_name + ".pak"
    final_result_path = os.path.join(template_folder, result_name)

    subprocess.run(bat_path, shell=True, cwd=template_folder)

    #rename the .pak

    print("------------------------------")
    try:
        os.rename(result_path, final_result_path)
        print(f"mod created :{result_name} ")
    except:
        print("WARNING!! Please make sure to archive stuff first, to avoid duplicate names (MOD WAS CREATED BUT NOT RENAMED, CONSIDER RERUN THE SCRIPT FULLY AFTER FULL CLEAR)")
    

    
  
    
