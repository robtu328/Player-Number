#! /home/robtu/anaconda3/bin/python
import re
import os

def pars_06_annotation( filename, useDiff=True ):
   fileAnn = open(filename, 'r')
   number = 1
   objectNum = 0
   objectList = []
   for line in fileAnn.readlines():
       if not re.findall("^#", line) and not re.match(r'^\s*$', line): #remove remark and empty line
           # File Name
           matches = re.findall('^Image filename : ', line)
           if (matches != []):
             matches = re.findall("\"(.+?)\"", line)
             filename = matches[0]
             print(filename)


           #print(line)
           # Image Size
           matches = re.findall('^Image size \(X x Y x C\) \: \d+ x \d+ x \d+', line)
           if (matches != []):
             matches = re.findall('\d+ x \d+ x \d+', line)
             matches = matches[0].replace("x", '').split()
             #matches = re.findall("^Image ", line)
             #print(matches)
           
           # Objects
           matches = re.findall('^Objects with ground truth \:', line)
           if (matches != []):
             #matches = re.findall('\d+ \{ \s+ \}', line)
             matches = re.findall('\: \d+', line)
             objectNum = int(matches[0].replace(':', ''))
             #print(objectNum)
             
             matches = re.search('\d+ \{(.+?)\}', line)
             matches = matches.group(1).replace('"', '')
             classTypes = matches.replace('PAS', '')
             classTypesOrig = classTypes.split()
             print("classtyptOrig = ", classTypesOrig)
             classTypes = classTypes.replace('Right', '')
             classTypes = classTypes.replace('Left', '')
             
             subMatches = re.findall("Trunc", classTypes)
             if(subMatches!=[]):
                 Trunc = 1
            
             classTypes = classTypes.replace('Trunc', '')
             
             
             if(useDiff):
               classTypes = classTypes.replace('Difficult', '')
             classTypes = classTypes.replace('Frontal', '')
             classTypes = classTypes.replace('Rear', '')

             classTypes = classTypes.split()
             objType = matches.split()
             if (objectNum != len(objType)):
                 print ("Length mismatch ", objectNum, len(objType))
#             print(matches, classTypes)
#             print(objType)
            

           if (objectNum != 0):
               #print (number-1)
               #picString = "Bounding box for object {} \"{}\" (Xmin, Ymin) - (Xmax, Ymax) : ".format(number, objType[number-1])
               picString = "Bounding box for object {} \"{}\" \(Xmin, Ymin\) - \(Xmax, Ymax\) \: ".format(number, objType[number-1])
               matches = re.findall(picString, line)
               if (matches != []):
                   number = number + 1
                   matches = re.findall('\d+, \d+\) - \(\d+, \d+', line)
                   matches = re.sub("[(),-]","",matches[0])
                   matches = matches.split()
                   xmin=matches[0]
                   ymin=matches[1]
                   xmax=matches[2]
                   ymax=matches[3]
                   
                   truncated = 0
                   difficult = 0
                   re.findall('^Objects with ground truth \:', line)
                   #print ("ClassTypeOrig, number=",number-2, "name= " , classTypesOrig[number-2], " classType  ",  classTypes[number-2])
                   if(re.findall("Trunc", classTypesOrig[number-2]) !=[]):
                       truncated = 1
                   if(re.findall("Difficult", classTypesOrig[number-2]) !=[]):
                       difficult = 1
                   #print (classTypesOrig)
                   #print ("match", picString)
                   #print (classTypes, " ,", number - 2)
                   if( re.findall("Difficult", classTypes[number-2])==[]):
                     objectList.append([classTypes[number-2], xmin, ymin, xmax, ymax, truncated, difficult])
                   else:
                     print ("Difficult object found")
                   #print (xmin, ymin, xmax, ymax)



 
   if (objectNum != number -1):
      print ("object mismatch ", objectNum, ", ", number-1)
   
   fileAnn.close()
   print(objectNum, len(objectList), objectList)
   return filename, len(objectList), objectList 



if __name__ == '__main__':
    dirs = os.listdir("./" )

    for item in dirs:
      if os.path.isfile(item):
           f, e = os.path.splitext(item) 
           if (e == '.txt'):
               pars_06_annotation(item, useDiff=True)


    pars_06_annotation("000001.txt", False)
    pars_06_annotation("000004.txt", False)

