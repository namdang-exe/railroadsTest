#!/usr/bin/env python
# coding: utf-8

import arcpy
import os
from os import path
from arcpy import da
import time

start_time = time.time()

################ Feature Class ################

filePath = os.getcwd()
ID = []
folders = []
# Change this to change the root folder name
attachs_folder_name = "rr_folders"
if not path.isdir(attachs_folder_name):
    os.mkdir(attachs_folder_name)
inTable = r"C:\Users\dangn\PycharmProjects\railroadsTest\gdbs\Railroads.gdb\Rail_Inventory_Data_Collection"
with da.SearchCursor(inTable, ['globalid', 'CrossingInventoryNumber']) as cursor:
    for item in cursor:
        fileFolders = path.join(filePath, "rr_folders")
        fileStore = path.join(fileFolders, str(item[1]))
        # Append GUID and folders' name to a list
        ID.append(item[0])
        folders.append(fileStore)
        if not path.isdir(fileStore):
            os.mkdir(fileStore)

################ ATTACH ################

# Relica the attachments
# input and output paths
filePath = os.getcwd()
inTable = r"C:\Users\dangn\PycharmProjects\railroadsTest\gdbs\Railroads.gdb\Rail_Inventory_Data_Collection__ATTACH"
# import attachments
with da.SearchCursor(inTable, ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'rel_globalid']) as cursor:
    for item in cursor:
        attachment = item[0]
        filenum = "RR" + str(item[2]) + "_"
        filename = filenum + str(item[1])
        if item[3] in ID:
            index = ID.index(item[3])
            folder = path.join(folders[index], filename)
            open(folder, 'wb').write(attachment.tobytes())

print("Updated sucessfully. It took {} seconds".format(time.time() - start_time))
