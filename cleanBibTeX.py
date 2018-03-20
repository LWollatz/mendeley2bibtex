import codecs
import formatBibTeX
import errorHandler as err
from formatBibTeX import *
from BibTeXclasses import bibentry

#global collectors
globalkeys=[]

def createNewEntry(line,accDuplicate):
    dattype = line[:5].lower()
    a = line.find("@")
    b = line.find("{",a)
    dattype = line[a+1:b].lower()
    a = line.find("{")
    datkey = line[a+1:].rstrip(",\n")
    datkey = formatKey(datkey)
    if datkey in globalkeys:
        if accDuplicate:
            doOutput = True
            err.raiseError("dublicate key: "+datkey)
        else:
            doOutput = False
            err.raiseWarning("dublicate key: "+datkey)
    else:
        globalkeys.append(datkey)
        doOutput = True
    thisEntry = bibentry(dattype,datkey)
    return (thisEntry, dattype, datkey, doOutput)

def appendEntry(allEntries,thisEntry):
    if thisEntry != None:
        #print "completed "+datkey
        allEntries.append(thisEntry)
    return allEntries

def readFile(fin):
    f1 = codecs.open(fin,'r',encoding='utf-8')
    lines = f1.readlines()
    f1.close()
    return lines

def writeFile(fout,output,append=False):
    if append == True:
        f2 = open(fout,"a")
    else:
        f2 = open(fout,"w")
    f2.write(output)
    f2.close()
    return None
    

def main(fin,fout,accDuplicate=False,append=False,verbose=True):
    global globalkeys, AllErrors, mainVerbose
    err.mainVerbose = verbose
    lines = readFile(fin)
    output = ""
    dattype = ""
    datkey = ""
    skip = 0
    level = 0
    debug = False
    doOutput = True #do we output this reference or not?
    thisEntry = None
    allEntries = []
    for line in lines:
        if line[0] != "%": #if this is not a comment
            if debug == True: #in case that we are in debugging mode, then print the line
                print line
            if line[0] == "@":
                #output old entry
                if doOutput:
                    allEntries = appendEntry(allEntries,thisEntry)
                if level != 0 or skip != 0:
                    err.raiseError("Unbalanced reference "+datkey+" level:"+str(level)+" skip:"+str(skip),verbose)
                #if this line defines a new entry:
                (thisEntry, dattype, datkey, doOutput) = createNewEntry(line,accDuplicate)
                level = 0
                skip = 0
                if datkey == "testkey":
                    debug = True
                else:
                    debug = False
            elif skip == 1 and level + line.count("{") - line.count("}") == 1:
                #if this line is the end of the continuation of a previous line
                #TODO: append to current line and parse it
                #if thisEntry != None:
                #    thisEntry.addline(line)
                skip = 0
            elif skip == 1:
                #if this line is a continuation of a previous line
                #TODO: append to current line
                pass
            elif line == "}":
                #this case doen't seem to occur like ever :-S
                dattype = ""
                #output += line
                print "END OF ENTRY"
                allEntries = appendEntry(allEntries,thisEntry)
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
        allEntries = appendEntry(allEntries,thisEntry)

    allEntries.sort(key=lambda x: x.key,reverse=False)
    for entry in allEntries:
        output += str(entry)

    writeFile(fout,output,append)

    print "There were "+str(len(err.AllErrors))+" errors, and "+str(len(err.AllWarnings))+" warnings."
    return allEntries
            
      

    
