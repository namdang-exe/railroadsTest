#!/usr/bin/env python
# coding: utf-8

"""
This python script automates the updates of railroad crossing safety
Publication Date: 05/20/21
Author - Nam Dang, ALDOT Intern
"""

import arcpy
import os
from os import path
from arcpy import da
import datetime

################ Feature Class ################
# Loop through rows in the processed_data col and look for 0s

# Input and output paths
working_dir = os.getcwd()
######### Change your geodatabase directory here #########
geodb = r"gdbs\Railroads.gdb"
fc_name = "Rail_Inventory_Data_Collection"

inTable = path.join(working_dir, geodb, fc_name)
workspace = path.join(working_dir, geodb)

# Attributes to look for in the feature class
fields = ['processed_data', 'globalid', 'CrossingInventoryNumber']
# Python arrays
ID = []
folders = []

# Process: Create a parent folder, folder name = current date
now = datetime.datetime.now()  # current time
parent_folder = now.strftime("%m-%d-%y")
if not path.isdir(parent_folder):
    os.mkdir(parent_folder)

# Process: Edit Session
try:
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err:
    print(f"General error: {err}.")
except:
    print("Unexpected error. Please check the input again.")

# Process: Select and Update Data
try:
    with arcpy.da.UpdateCursor(inTable, fields) as cursor:
        for row in cursor:
            # look for 0s in the processed_table
            if not row[0]:
                crossing_folders = path.join(working_dir, parent_folder)
                store_file = path.join(crossing_folders, str(row[2]))
                # Append GUID and Crossing ID to a list
                ID.append(row[1])
                folders.append(store_file)
                if not path.isdir(store_file):
                    os.mkdir(store_file)
                row[0] = 1
            cursor.updateRow(row)
    del cursor

except RuntimeError:
    print(f"{inTable} is an invalid directory.")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err:
    print(f"General error: {err}.")
except:
    print("Unexpected error. Please check the input again.")

edit.stopOperation()
edit.stopEditing(True)

################ ATTACH ################
# Copy the attachments

# input and output paths
working_dir = os.getcwd()
######### Change your geodatabase here #########
geodb = r"gdbs\Railroads.gdb"
fc_name = "Rail_Inventory_Data_Collection__ATTACH"
inTable = path.join(working_dir, geodb, fc_name)
fields = ['rel_globalid', 'DATA']

# Process: copy attachments
tracking = [1 for _ in folders]  # tracks the file name in the folder
try:
    with arcpy.da.SearchCursor(inTable, fields) as cursor:
        for row in cursor:
            if row[0] in ID:
                attachment = row[1]
                index = ID.index(row[0])
                crossing_ID = path.split(folders[index])[1]
                file_name = f"{crossing_ID}_{tracking[index]}.jpg"
                folder = path.join(folders[index], file_name)
                open(folder, 'wb').write(attachment.tobytes())
                tracking[index] += 1

except RuntimeError:
    print(f"{inTable} is an invalid directory.")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err:
    print(f"General error: {err}.")
except:
    print("Unexpected error. Please check the input again.")
