import formatBibTeX
from formatBibTeX import *
from BibTeXclasses import bibentry

USEABBREVIATIONS = True

#Linked Mendeley BibTeX export file
mbibfilename = "library.bib"
#BibTeX file for LaTeX
bibfilename = "res_biblibrary.bib"


#global collectors
globalkeys=[]
globaljournals=[]
globalpublishers=[]

def main(fin,fout,accDuplicate=False,append=False):
    global USEABBREVIATIONS
    global fixedterms
    global globalkeys, globalpublishers, globaljournals
    f1 = open(fin,'r')
    lines = f1.readlines()
    f1.close()
    output = ""
    dattype = ""
    datkey = ""
    skip = 0
    level = 0
    debug = False
    hasdoi = False
    hasID = False
    doOutput = True #do we output this reference or not?
    thisEntry = None
    for line in lines:
        if line[0] != "%": #if this is not a comment
            #some default checks
            if debug == True: #in case that we are in debugging mode, then print the line
                print line
            if line.lstrip(" ").lower().startswith("doi"): #if this defines a doi, note that there is an identifier
                hasdoi = True
                hasID = True
            if line.lstrip(" ").lower().startswith("isbn ") or line.lstrip(" ").lower().startswith("isbn\t"): #if this defines an ISBN, note that there is an identifier
                hasID = True
            if line.lstrip(" ").lower().startswith("url "): #if this defines a url, note that there is an identifier
                hasID = True
            if line[0] == "@":
                if thisEntry != None and doOutput:
                    output += str(thisEntry)
                    journal = thisEntry.getvalue("journal")
                    if journal != None:
                        globaljournals.append(journal)
                #if this line defines a new entry:
                dattype = line[:5].lower()
                a = line.find("@")
                b = line.find("{",a)
                dattype = line[a+1:b].lower()
                    
                if level != 0 or skip != 0:
                    print "ERROR Unbalanced reference "+datkey+" level:"+str(level)+" skip:"+str(skip)
                level = 0
                skip = 0
                hasdoi = False
                hasID = False
                a = line.find("{")
                datkey = line[a+1:].rstrip(",\n")
                if datkey in globalkeys:
                    #print("dublicate key: "+datkey)
                    if accDuplicate:
                        doOutput = True
                    else:
                        doOutput = False
                else:
                    datkey = formatKey(datkey)
                    globalkeys.append(datkey)
                    doOutput = True
                thisEntry = bibentry(dattype,datkey)
                #if doOutput:
                #    output += line
                if datkey == "testkey":
                    debug = True
                else:
                    debug = False
            elif skip == 1 and level + line.count("{") - line.count("}") == 1:
                #if this line is the end of the continuation of a previous line
                skip = 0
            elif skip == 1:
                #if this line is a continuation of a previous line
                pass
            elif line == "}":
                #this case doen't seem to occur like ever :-S
                dattype = ""
                #output += line
                print "END OF ENTRY"
                output += str(thisEntry)
            else:
                #this line defines a key-value pair within an entry
                formatBibTeX.globalkeys = globalkeys
                if thisEntry != None:
                    thisEntry.addline(line)
                
                badkey = False
            level += line.count("{") - line.count("}")
            if debug == True:
                print skip,level,line
    if doOutput:
        output += str(thisEntry)
    
    if append == True:
        f2 = open(fout,"a")
    else:
        f2 = open(fout,"w")
    f2.write(output)
    f2.close()

    globalpublishers.sort(key=lambda x: x.upper(),reverse=False)
    globaljournals.sort(key=lambda x: x.upper(),reverse=False)
    return None
            

#Now we can take the mendeley library and convert it.
main(mbibfilename,bibfilename,False,False)
#Afterwards, add any other files you want to merge.
#main("myotherbibliography.bib",bibfilename,False,True)

#If you want to make sure, that your journals are not misspelled,
#why not print out a list of them and check if they look alright?
globaljournals = [j+", "+str(globaljournals.count(j)) for j in globaljournals]
temp = set(globaljournals)
globaljournals = list(temp)
globaljournals.sort(key=lambda x: x.upper(),reverse=False)

#Now we are done. If this is executed in a window, we can let 
#people check potential errors before the window closes
temp = input("Press Enter to close this window. ")
    
