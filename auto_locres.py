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
import shutil
from Database.resources import foxholeversion, version_folder, automodtxt_path, Fmodel_output_folder
from Database.resources import template_folder, bat_path,  locres_pak_folder, war_pak_folder, result_init_name
from Database.resources import tool_path

# create the version folder if not done yet
os.makedirs(version_folder, exist_ok=True)


# path of initial locres file
basedir = os.path.join(Fmodel_output_folder, r"War\Content\Localization") 

StringFile = os.path.join(basedir, r"Foxhole-CodeStrings\en\Foxhole-CodeStrings.locres")
ContentFile = os.path.join(basedir, r"Foxhole-Content\en\Foxhole-Content.locres")

# create path for reading mod reference files
ContentFolder = os.path.join(automodtxt_path, r"Database\Content")
CodeStringFolder = os.path.join(automodtxt_path, r"Database\CodeStrings")

# create path for copies of locres
copyfolder = os.path.join(automodtxt_path, r"Database\!File")
os.makedirs(copyfolder, exist_ok=True)

filename_string_copy = os.path.join(copyfolder, "Foxhole-CodeStrings.locres")
shutil.copy(StringFile, filename_string_copy)        

filename_content_copy = os.path.join(copyfolder, "Foxhole-Content.locres")
shutil.copy(ContentFile, filename_content_copy) 

# create the locres .txt file in proper location

tool_executable = os.path.join(tool_path, "UE4LocalizationsTool.exe")

print(" -- Locres txt creation -- \n")

command = [tool_executable, "export", filename_content_copy]
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(f"Import Result :\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error with the command : {e.stderr}")
except Exception as e:
    print(f"Error : {str(e)}")

command = [tool_executable, "export", filename_string_copy]
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(f"Import Result :\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error with the command : {e.stderr}")
except Exception as e:
    print(f"Error : {str(e)}")

# VARIOUS DEFINITIONS

codestr = filename_string_copy + ".txt"
content = filename_content_copy + ".txt"

dic =  {
    ContentFolder : [content, "Foxhole-Content.locres.txt"],
    CodeStringFolder : [codestr, "Foxhole-CodeStrings.locres.txt"]
}

def readfile (file):
    codedb = pd.read_csv(file, sep="=", header=None, names=["source", "translation"], usecols=[0, 1])
    return codedb

def read_template(file_path):
    data_db = pd.read_csv(file_path, header=None, names=["target", "replacement"], index_col="target")
    return data_db

def import_csv_to_ue4_localizations(csv_path, tool_path):
    tool_executable = os.path.join(tool_path, "UE4LocalizationsTool.exe")
    
    if not os.path.exists(tool_executable):
        print(f"Erreur : L'outil UE4LocalizationsTool n'est pas trouvé à {tool_executable}")
        return
    
    if not os.path.exists(csv_path):
        print(f"Erreur : Le fichier txt '{csv_path}' n'existe pas.")
        return
    
    command = [tool_executable, "-import", csv_path]

    
    print(f" -- Importing {file} as locres -- \n")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Import Result :\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error with the command : {e.stderr}")
    except Exception as e:
        print(f"Error : {str(e)}")    

# starting the core loop

for category in dic.keys(): # loop through category folders
    df = readfile(dic[category][0])
    
    df = df.astype('object')
    df.fillna("", inplace=True)

    filtered_df = df.copy()
    filtered_df

    filename = ""
    filename = dic[category][0][:-4]

    for file in os.listdir(category): # loop through mod template files
        file_path = os.path.join(category, file)
        data_db = read_template(file_path)

        print (f"\n ------- {file} ------- \n")
        

        dossier_mod = os.path.join(version_folder, file[:-4]) #create the mod folder to store the .locres and .txt
        os.makedirs(dossier_mod, exist_ok=True)

        df_mod = filtered_df

        for i in data_db.index:  # replace the data in the .txt converted to dataframe
            pattern = rf'\b{i}\b'
            replacement = data_db.loc[i, "replacement"]
            df_mod["translation"] = df_mod["translation"].apply(lambda x: re.sub(pattern, replacement, x))

        csv_path = os.path.join(dossier_mod, dic[category][1])[:-4] + ".txt"
        df_mod.to_csv(csv_path, index=None, header=None, sep="=") # save the edited csv/txt

        mod_copy = (os.path.join(dossier_mod, dic[category][1])[:-4])
        shutil.copy(filename, mod_copy)
        
        import_csv_to_ue4_localizations(csv_path, tool_path) # create the locres from the csv

        #create the template correct folders (delete war first)
        
        shutil.rmtree(war_pak_folder)
        os.makedirs(locres_pak_folder, exist_ok=True)

        #### move to pak stuff

        pak_folder_full = os.path.join(locres_pak_folder, dic[category][1][:-11], "en")
        pak_mod_path = os.path.join(pak_folder_full, dic[category][1][:-4])

        os.makedirs(pak_folder_full, exist_ok=True)
        
        shutil.copy(mod_copy, pak_folder_full)


        #use the .bat

        result_path = os.path.join(template_folder, result_init_name)
        result_name = "War-WindowsNoEditor_"+ foxholeversion + "_" + file[:-4] + ".pak"
        final_result_path = os.path.join(template_folder, result_name)

        subprocess.run(bat_path, shell=True, cwd=template_folder)
        print(f"mod created :{result_name} ")

        #rename the .pak
    
        try:
            os.rename(result_path, final_result_path)
            print(f"mod created :{result_name} ")
        except:
            print("WARNING!! Please make sure to archive stuff first, to avoid duplicate names (MOD WAS CREATED BUT NOT RENAMED, CONSIDER RERUN THE SCRIPT FULLY AFTER FULL CLEAR)")
        
        
        
    

    