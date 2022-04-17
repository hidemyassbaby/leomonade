# -*- coding: utf-8 -*-
import sys, os, re, json
from os import listdir
from os.path import isfile,join
import operator

# import six
# if six.PY2: py_ver = 2
# if six.PY3: py_ver = 3
# print ('\n' + '----------------------------------') 
# print('Running Python Version - ' + str(py_ver))

myPath = sys.path[0]

xmlFolder = os.path.join(myPath, 'xmlFiles')
jsonFolder = os.path.join(myPath, 'jsonFiles')

fileList=[]

if os.path.exists (xmlFolder):
    print ('\n' + 'JEN xml  Folder located ......') 
else:
    print ('JEN xml Folder not found.... ') 
    print ('Please check your settings ') 
    print (xmlFolder) 
    print ('Script will now Exit ......') 
    exit ()

if os.path.exists (jsonFolder):
    print ('JSON Folder located ......') 
else:
    print ('JSON Folder not found.... ') 
    print ('Script wiil create the following... ') 
    print (jsonFolder) 
    os.mkdir(jsonFolder) 





fileList = [f for f in listdir(xmlFolder) if isfile(join(xmlFolder, f))]

jsdata = {'items' : []} 
# idict = {} 

list_pattern = re.compile(
        '((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<f4m>.+?</f4m>'
        '|<info>.+?</info>|'
        '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail>'
        '<mode>[^<]+</mode>|'
        '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail>'
        '<date>[^<]+</date>))', re.MULTILINE | re.DOTALL)

regex = '<%s>(.+?)<\/%s>'

tag1 = 'name' 
tag1a = 'title' 
tag2 = 'link'
tag3 = 'sublink'
tag4 = 'thumbnail'
tag5 = 'fanart'
tag6 = 'meta'
tag7 = 'imdb'
tag8 = 'content'
tag9 = 'tvshowtitle'
tag10 = 'year'
tag11 = 'season'
tag12 = 'episode'
tag13 = 'summary'

tag_list = [tag1, tag1a, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10, tag11, tag12, tag13] 

def writeMe(wData, wFile) :
    f3 = open(wFile,'w')
    f3.write(wData)
    f3.close()
    return


def readMe(rFile) :  
    with open(rFile , 'r') as f3 :
        rData = f3.read()
    f3.close()  
    return rData
        
def writeJS(wData, wFile) :
    f3 = open(wFile,'w')
    json.dump(wData,f3,indent=4,sort_keys=False)
    f3.close()

def readJS(rFile) :
    rData = [] 
    f3 = open(rFile,'r')   
    rData = json.loads(f3.read())
    f3.close() 
    return rData

def get_Folders(dirname):
    path =dirname
    xml_filelist = []
    xml_folderlist = []
    json_filelist = []
    json_folderlist = []

    for root, dirs, files in os.walk(path):
        
        for folder in dirs:
            # append the folder name to the lists
            xml_folderlist.append(os.path.join(root,folder))
            json_folderlist.append(os.path.join(root,folder).replace(xmlFolder,jsonFolder)) 
            
        for file in files:
            # append the file name and path to the lists
            xml_filelist.append(os.path.join(root,file))
            json_filelist.append(os.path.join(root,file).replace(xmlFolder,jsonFolder).replace('.xml','.json'))
            #
            # filelist.append(file) # append name only 
            # filelist.append(file.replace('.xml','.json')) # append name only 
        
    ## create any missing json folders
    for nf in json_folderlist:     
        if not os.path.exists(nf): os.mkdir(nf) 
        
    ### prints for checking 
    ## print all the xml folder names
    # for name in xml_folderlist:  
        # print('\n' + 'xml Folder - ' + name) 
        
    ## print all the json folder names
    # for name in json_folderlist:     
        # print('\n' + 'json Folder - ' + name) 
        
    ## print all the xml file names
    # for name in xml_filelist:
        # print('\n' + name)
        
    ## print all the json file names
    # for name in json_filelist:
        # print('\n' + name)
    
    return  xml_filelist
    
fileList = get_Folders(xmlFolder)

for file in fileList:    
    jsdata = {'items' : []} 
    jsinfo = []
      
    inputFile = file
    outputFile = file.replace(xmlFolder,jsonFolder).replace('.xml' , '.json')
      
    print ('\n' + 'Processing File - ' + str(file)) 
    data = readMe(file).replace('\n','').replace('\r','').replace('\t','')
           
    myData = list_pattern.findall(data)
    
    for md in myData :
        idict = {} 
        if 'item' in md : this_item = 'item'  
        elif 'dir' in md : this_item = 'dir'  
        else  : this_item = 'unknown' 
        idict.update({"type": this_item}) 
                       
        for tag in tag_list:
            t = '' 
            t = ''. join(re.findall(regex %(tag, tag), md, re.MULTILINE | re.DOTALL)) 
            if t : 
                if  tag == 'link' and 'sublink' in t :                   
                    subs = re.findall(regex %('sublink' , 'sublink'), md, re.MULTILINE | re.DOTALL)
                    idict.update({"link" : subs})   
                    
                elif tag == 'link' and not 'sublink' in t :  
                    idict.update({"link" : t})   
                       
                elif tag == 'name' : idict.update({"title" : t})   
                elif tag == 'meta' : pass        
                elif tag == 'sublink' : pass              
                else : idict.update({tag : t})   
                                
            else : 
                pass
                   
        jsinfo.append(idict)
       
#    try :     
#        jsinfo.sort(key = operator.itemgetter('title') , reverse = False)    
#    except :
#        print ('\n' + '--------- WARNING ---------') 
#        print ( '--------- ERROR SORTING  ---> ') 
#        print (outputFile) 
#        print ( '---------------' + '\n') 
       
    try :     
        for i in jsinfo :
            jsdata['items'].append(i)
    except :
        print ('\n' + '--------- WARNING ---------') 
        print ( '--------- ERROR APPENDING  ---> ') 
        print (outputFile) 
        print ( '---------------' + '\n') 
    
    # for i in jsinfo :
        # jsdata['items'].append(i)

    try :
        writeJS(jsdata, outputFile) 
    except :
        print ('\n' + '--------- WARNING ---------') 
        print ( '--------- ERROR WRITING  ---> ') 
        print (outputFile) 
        print ( '---------------' + '\n') 
        
    
print ('\n' + '--- FINISHED JSON CONVERSION ---') 


