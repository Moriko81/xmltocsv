# converting xml files to csv files 
# now this can only convert one file...
# 2023/05/23
import os
print(os.getcwd()) # show current directory

# os.chdir("E:\\Dropbox\\07_NagasawaText\\program_py") 
os.chdir("C:\\Users\\Sugie001\\Dropbox\\07_NagasawaText\\program_py") # UU
# os.chdir("E:\\Dropbox\\07_NagasawaText\\program_py") # at home 
# os.chdir("C:\\Users\\sugie\\Dropbox\\07_NagasawaText\\program_py") #　laptop

from xml.etree import ElementTree as ET 
import csv                              

# tree = ET.parse("RB102.rdf")  # read a xml file 
tree = ET.parse("RB105.rdf")    # read a xml file 

# create csv file  
# if i use 'utf-8', it will cause error 
csvfile = open("data.csv",'w',encoding='utf-8-sig')

# writer function returna a writer object 
csvwriter = csv.writer(csvfile)

# make a column as a header as a list
col_names = ["bibRecordSubCategory", 
             "identifier",
             "identifier.1",
             "seeAlso",
             "seeAlso.1",
             "title", 
             "title.1",
             "volume.Description.value",              
             "edition",      
             "creator", 
             "creator.1", 
             "publisher.Agent.name", 
             "publisher.Agent.description",   
             "publisher.Agent.locatin",                
             "publicationPlace.text", 
             "date", 
             "issued.text",                
             "description",
             "description.1",
             "description.2", 
             "subject",
             "subject.1", 
             "subject.2",
             "subject.3",
             "subject.4", 
             "subject.5", 
             "subject.6",             
             "language.text",             
             
             "audience", 
             "extent", 
             "price", 
             "materialType.resource"
             ]
col_names

# write the clomun names into csvwriter with writerow function
csvwriter.writerow(col_names)

# get a root node 
root = tree.getroot()
print(root)

# make a dictionary of namespaces to use for the second argument of "iterfind"
namespace = {
  'dcndl':'http://ndl.go.jp/dcndl/terms/',
  'dc': 'http://purl.org/dc/elements/1.1/',
  'dcterms': 'http://purl.org/dc/terms/', 
  'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
  'rdfs':'http://www.w3.org/2000/01/rdf-schema#',  
  'foaf':'http://xmlns.com/foaf/0.1/'
} 

#　extract texts or value of attributes for each element
result = [] # empty list 

for subcate in root.iterfind(".//dcndl:bibRecordSubCategory", namespace):
    if subcate != None:
        result.append(subcate.text)

for identifier in root.iterfind(".//dcndl:BibResource/dcterms:identifier", namespace):
    test = list(identifier.attrib.values())
    test = test[0].split('terms/')
    test2 = test[1]  + '_' + identifier.text
    result.append(test2)

for seeAlso in root.iterfind(".//dcndl:BibResource/rdfs:seeAlso", namespace):
    test = list(seeAlso.attrib.values())
    test = test[0].split('go.jp/')
    result.append(test[1])

for title_dcterms in root.iterfind(".//dcterms:title", namespace):
    result.append(title_dcterms.text)
    
for title_dc in root.iterfind(".//dc:title/rdf:Description/rdf:value", namespace):
    result.append(title_dc.text)  

for volume in root.iterfind(".//dcndl:volume/rdf:Description/rdf:value", namespace):
    result.append(volume.text)  
        
for edition in root.iterfind(".//dcndl:edition", namespace):
    if edition != None:
        result.append(edition.text) 
    else:
       edition = ''
       result.append(edition) 

for creator_dcterms in root.iterfind(".//dcterms:creator/foaf:Agent/foaf:name", namespace):
    result.append(creator_dcterms.text) 
    
for creator_dc in root.iterfind(".//dc:creator", namespace):
    result.append(creator_dc.text)
    
for publisherName in root.iterfind(".//dcterms:publisher/foaf:Agent/foaf:name", namespace):
    result.append(publisherName.text)  
    
for publisherDes in root.iterfind(".//dcterms:publisher/foaf:Agent/dcterms:description", namespace):
    result.append(publisherDes.text) # description    
    
for publisherLoc in root.iterfind(".//dcterms:publisher/foaf:Agent/dcndl:location", namespace):
    result.append(publisherLoc.text) # location
    
for publicationPlace in root.iterfind(".//dcndl:publicationPlace", namespace):
    result.append(publicationPlace.text)  

for date in root.iterfind(".//dcterms:date", namespace):
    result.append(date.text)  
  
for issued in root.iterfind(".//dcterms:issued", namespace):
    result.append(issued.text) 

# if there is "subject-description-value", 
# get "subject-description-about" and "subject-description-value"   
# i only need after "auth/" in subject-description-about"
# this should be 3 rows; "description", "description.1", "description.2"  
# not finished yet
for subject in root.iterfind(".//dcterms:subject/rdf:Description", namespace):
    test = subject.attrib
    if test == None:
        test = ''
        result.append(test)
    else:
        test2 = list(test.values()) # dict_values
        test3 = test2[0].split('auth/')
        test4 = test3[1].split('/')
        for value in root.iterfind(".//dcterms:subject/rdf:Description/rdf:value", namespace):
            test5 = test4[0] + '_' + value.text
            result.append(test5)
        
# this should be seven rows 
# not finished yet
for subjectRe in root.iterfind(".//dcterms:subject[@rdf:resource]", namespace):
    test =subjectRe.attrib
    if test == None:
        test = ''
        result.append(test)
    else:
        test2 = list(test.values())
        test3 = test2[0].split('class/')
        result.append(test3[1])

for language in root.iterfind(".//dcterms:language", namespace):
    result.append(language.text) # jpn
 
for extent in root.iterfind(".//dcterms:extent", namespace):
    result.append(extent.text) # page, size  
     
for materialType in root.iterfind(".//dcndl:materialType", namespace):
    test = list(materialType.attrib.values()) # two attributes, i need second one
    result.append(test[1]) 
    
for price in root.iterfind(".//dcndl:price", namespace):
    result.append(price.text)
     
for audience in root.iterfind(".//dcterms:audience", namespace):
    result.append(audience.text)  

print(result) 

csvwriter.writerow(result)
csvfile.close()

import pandas as pd
dataframe = pd.read_csv('data.csv')
print(dataframe.shape)

# end

