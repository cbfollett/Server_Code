#import modules
import arcpy, sys, os, string

#specify folder containing MXDs

#variable input of folder location
#inFolder = raw_input("Please enter folder containing 10.1 MXDs to Publish to ArcServer: ")

#lets try using Canada first

#publish folder variable is for the destination folder, represented as a string, for the arcgis server
#this variable will work...
publish_folder = "HSIP_2013_Region5"

inFolder = r"D:\AGS_SvrData\Test_Folder2"

path= inFolder

#walks through the directory and adds files
for (path, dirs, files) in os.walk(path):
	for fl in files:
		if fl.lower().endswith(".mxd"):
			listmxd = arcpy.mapping.MapDocument(os.path.join(path, fl))
			print listmxd.filePath


#specify connection File Path
con = 'GIS Servers/arcgis on R05-GIS1_6080 (publisher).ags' 


#look in folder for mxds
MapPath= []
MapFolder = os.listdir(inFolder)
for file in MapFolder:
    fileExt = os.path.splitext(file)[1]
    if fileExt == ".mxd":
        MapPath = os.path.join(inFolder, file)
        file = MapPath.strip('\'')
        mxd = arcpy.mapping.MapDocument(file)
        base = os.path.basename(file)
        serviceName = base[:-4]
        SDDraft = file[:-4] + ".sddraft"
        sd = file[:-4] + ".sd"

        #Create Map SD Draft

        #Syntax
#CreateMapSDDraft (map_document, out_sddraft, service_name, {server_type}, {connection_file_path}, {copy_data_to_server}, {folder_name}, {summary}, {tags})
        print "\n" + "Publishing: " + base
        analysis = arcpy.mapping.CreateMapSDDraft(mxd, SDDraft, serviceName, "ARCGIS_Server", con, "False", publish_folder, "None", "None")

#the below line is the start of being able to edit the 
 #       doc = DOM.parse(SDDraft)

#xml.dom.minidom will be used to change pooling and other factors

        # stage and upload the service if the sddraft analysis did not contain errors
        if analysis['errors'] == {}:
            # Execute StageService
            print "Staging Service"
            arcpy.StageService_server(SDDraft, sd)
            # Execute UploadServiceDefinition
            print "Uploading Service Definition"
            arcpy.UploadServiceDefinition_server(sd, con)
            print "Publishing " + base +" succeeded" + "\n"
        else:
            # if the sddraft analysis contained errors, display them
            print analysis['errors']