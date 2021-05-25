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

# Loop through rows in the table and look for 0s
# Input and output paths
filePath = os.getcwd()
# geodb = r"gdbs\Railroads.gdb"
# fc_name = "Rail_Inventory_Data_Collection"
# inTable = path.join(filePath, geodb, fc_name)
inTable = r"C:\Users\dangn\PycharmProjects\railroadsTest\gdbs\Railroads.gdb\Rail_Inventory_Data_Collection"
workspace = r"C:\Users\dangn\PycharmProjects\railroadsTest\gdbs\Railroads.gdb"
# Attributes to look for in the feature class
fields = ['processed_data', 'globalid', 'CrossingInventoryNumber']
# Python arrays
ID = []
folders = []

# Process: Create a parent folder, folder name = current date
now = datetime.datetime.now()  # current time
parent_folder = f"{now.month}-{now.day}-{now.year}"
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
# look for 0s in the processed_table
try:
    with arcpy.da.UpdateCursor(inTable, fields) as cursor:
        for row in cursor:
            if not row[0]:
                crossing_folders = path.join(filePath, parent_folder)
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
filePath = os.getcwd()
inTable = r"C:\Users\dangn\PycharmProjects\railroadsTest\gdbs\Railroads.gdb\Rail_Inventory_Data_Collection__ATTACH"
fields = ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'rel_globalid']
# Process: copy attachments
try:
    with arcpy.da.SearchCursor(inTable, fields) as cursor:
        for row in cursor:
            attachment = row[0]
            filenum = "RR" + str(row[2]) + "_"
            filename = filenum + str(row[1])
            if row[3] in ID:
                index = ID.index(row[3])
                folder = path.join(folders[index], filename)
                open(folder, 'wb').write(attachment.tobytes())

except RuntimeError:
    print(f"{inTable} is an invalid directory.")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err:
    print(f"General error: {err}.")
except:
    print("Unexpected error. Please check the input again.")
