import json
from html.parser import HTMLParser
import pandas as pd
import sys

inputfile = ""
outputfile = ""
data = ""

if (len(sys.argv) == 2):
    if (str(sys.argv[1]).lower() not in ['-h', 'h', 'help', '-help']):
        print("Incorrect or too few argument(s). Please type -h for help.")
        exit()
    else:
        print("usage: python jsonld_to_html.py <path to input json-ld file> <path to output html file>")
        exit()
elif (len(sys.argv) == 3):
    try:
        # Load input data file
        inputfile=sys.argv[1]
        with open(sys.argv[1]) as json_file:
            data = json.load(json_file) 
    except Exception as e:
        print("Input file is not a valid JSON file.")
        exit()
    try:
        # Valid output file path
        f = open(sys.argv[2], "w")
    except Exception as e:
            print("Output file path is not valid.")
            exit()
    outputfile = sys.argv[2]
else:
    print("Incorrect number of argument(s). Please type -h for help.")
    exit()

# Load data
with open(inputfile) as json_file:
    data = json.load(json_file)   
    
# Load JSON-LD-key to HTML-template-variable mappings
df = pd.read_csv ("mappings/jsonld_to_htmltemplate_mapping.csv", index_col=None)


# In[142]:


# Software metadata
software_var = {}
# Dependency dataset metadata
depdataset_var = {}

# Helper function: Resolve JSON-LD-key to HTML-template-variable mappings
def resolve_value(key, jsondata):
    keyparts = key.split(";")
    if (len(keyparts) == 1):
        return jsondata[keyparts[0]]
    else:
        jsondata=jsondata[keyparts[0]]
        new_key = ";".join(keyparts[1:])
        if keyparts[1] in jsondata:
            return resolve_value(new_key, jsondata)
        else:
            return ""
        
# Resolve JSON-LD-key to HTML-template-variable mappings  
def get_value(input_variable):
    global data
    global df
    
    json_key = df[df['html_template_variable']==input_variable]['jsonld_key'].values[0]
    keyparts = json_key.split(";")
    if keyparts[0] in data:
        result = resolve_value(json_key, data)
        return result
    else:
        return ""
    
# For isBasedOn property: special case
def get_new_key(input_variable):
    global df
    
    json_key = df[df['html_template_variable']==input_variable]['jsonld_key'].values[0]
    return json_key.replace("isBasedOn;","")

# Obtain related software or data dependencies from isBasedOn property
def handle_isBasedOn():
    global data
    global software_var
    global depdataset_var
    
    if "isBasedOn" in data:
        if len(data["isBasedOn"]) > 0:
            for item in data["isBasedOn"]:
                if (item["@type"] == "SoftwareApplication"):
                    software_var = item
                else:
                    depdataset_var = item

# Handle isBasedOn property
handle_isBasedOn()

import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/html_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(

# Dataset
jsonld=data,
datasetname=get_value('datasetname'),
datasetdescription=get_value('datasetdescription'),
datasetversion=get_value('datasetversion'),
datasetencodingFormat=get_value('datasetencodingFormat'),
datasetdateCreated=get_value('datasetdateCreated'),
datasetdatePublished=get_value('datasetdatePublished'),
datasetlicense=get_value('datasetlicense'),
dataseturl=get_value('dataseturl'),
datasetinLanguage=get_value('datasetinLanguage'),
datasettemporal=get_value('datasettemporal'),
datasettemporalCoverage=get_value('datasettemporalCoverage'),
datasetkeywords=get_value('datasetkeywords'),
    
# Author
authorimage=get_value('authorimage'),
authorname=get_value('authorname'),
authorjobTitle=get_value('authorjobTitle'),
authoremail=get_value('authoremail'),
affiliationname=get_value('affiliationname'),
affiliationurl=get_value('affiliationurl'),
organizationimageurl=get_value('organizationimageurl'),

# Contributor
contributorlist=get_value('contributorlist'),

# Publisher
publisherorganizationname=get_value('publisherorganizationname'),
publisherorganizationlogo=get_value('publisherorganizationlogo'),
publisherorganizationurl=get_value('publisherorganizationurl'),
publisherpersonname=get_value('publisherpersonname'),
publisherpersonjobTitle=get_value('publisherpersonjobTitle'),
publisheremail=get_value('publisheremail'),
publisherimage=get_value('publisherimage'),
publisherpersonaffiliationname=get_value('publisherpersonaffiliationname'),
publisherpersonaffiliationurl=get_value('publisherpersonaffiliationurl'),
publisherpersonaffiliationimage=get_value('publisherpersonaffiliationimage'),

# Download
downloadurl=get_value('downloadurl'),
downloadencodingFormat=get_value('downloadencodingFormat'),
downloadcontentSize=get_value('downloadcontentSize'),

# Software
softwarename=resolve_value(get_new_key('softwarename'), software_var),
softwaredescription=resolve_value(get_new_key('softwaredescription'), software_var),
softwarecategory=resolve_value(get_new_key('softwarecategory'), software_var),
softwareos=resolve_value(get_new_key('softwareos'), software_var),
softwareversion=resolve_value(get_new_key('softwareversion'), software_var),
softwareurl=resolve_value(get_new_key('softwareurl'), software_var),

# Dependency dataset
depdatasetname=resolve_value(get_new_key('depdatasetname'), depdataset_var),
depdatasetdescription=resolve_value(get_new_key('depdatasetdescription'), depdataset_var),
depdatasetversion=resolve_value(get_new_key('depdatasetversion'), depdataset_var),
depdataseturl=resolve_value(get_new_key('depdataseturl'), depdataset_var),

# Publication
publicationname=get_value('publicationname'),
publicationauthorlist=get_value('publicationauthorlist'),
publicationpublishername=get_value('publicationpublishername'),
publicationdatePublished=get_value('publicationdatePublished'),
publicationsameAs=get_value('publicationsameAs'),
publicationpublisherurl=get_value('publicationpublisherurl')

)

#print(outputText)

# Save result to file
with open(outputfile, "w") as fh:
    fh.write(outputText)





