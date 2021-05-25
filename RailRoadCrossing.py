#!/usr/bin/env python
# coding: utf-8

# In[304]:


import arcpy
from arcpy import da
import os


# In[305]:


fd = r"C:\Users\locked\Documents\RailInventory\RR Test FGDB\RailSafetyInventory.gdb\Rail_Inventory_Data_Collection__ATTACH"
compTo = r"C:\Users\locked\Documents\RailInventory\RR Test FGDB\RailSafetyInventory.gdb\Rail_Inventory_Data_Collection"
folder_Path = r"C:\Users\locked\Documents\RailInventory"
new_Folder = "RailRoadCrossing_id"

arcpy.management.CreateFolder(folder_Path, new_Folder)

fileLocation = folder_Path + "\\" + new_Folder
#check to see if mTable exists and if it does delete it
# if arcpy.Exists(mTable):
#     arcpy.Delete_management(mTable)
    
mTable = arcpy.CreateTable_management("in_memory", "PlaceHolder")
arcpy.AddField_management(mTable, "ID", "TEXT")
arcpy.AddField_management(mTable, "DATA", "BLOB")


# In[306]:

###### FEATURE CLASS  ######
fcFields = ["GLOBALID"]
fcDictionary = {r[0]:r[1:] for r in arcpy.da.SearchCursor(compTo, fcFields)}


# In[307]:

##### ATTACH ######
fdAttach = ["REL_GLOBALID", "DATA"]
fdDictionary = {r[0]:r[1:] for r in arcpy.da.SearchCursor(fd, fdAttach)}


# In[319]:


cTable = arcpy.da.InsertCursor(mTable, "ID")

for i in fcDictionary:
    if i in fdDictionary:
        cTable.insertRow([i])       
        print(i)
      

       


# In[320]:


with arcpy.da.SearchCursor(cTable, ["DATA", "ID"], ) as cursor:
          for item in cursor:
              attachment = item[0]
              filename = str(item[1])
              open(fileLocation + os.sep + filename, 'wb').write(attachment.tobytes())
              print (filename)
del cursor                


# In[ ]:




