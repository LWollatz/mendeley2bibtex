from formatBibTeX import *

def tryFormat(datkey,fieldtype,value):
    try:
        value = doFormat(fieldtype,value)
    except Exception as e:
        print("ERROR in %s: %s" % (datkey,e))
        pass
    return value

entry2field={
    'article':{
    'required':['author','title','journal','year'],
    'optional':['volume','number','pages','month','note']
    },
    'book':{
    'required':['author','editor','title','publisher','year'],
    'optional':['volume','number','series','address','edition','month','note']
    },
    'booklet':{
    'required':['title'],
    'optional':['author','howpublished','address','month','year','note']
    },
    'conference':{
    'required':['author','title','booktitle','year'],
    'optional':['editor','volume','number','series','pages','address','month','organization','publisher','note']
    },
    'inbook':{
    'required':[],
    'optional':['author','title','howpublished','month','year','note']
    },
    'incollection':{
    'required':['author','title','booktitle','publisher','year'],
    'optional':['editor','volume','number','series','type','chapter','pages','address','edition','month','note']
    },
    'inproceedings':{
    'required':['author','title','booktitle','year'],
    'optional':['editor','volume','number','series','pages','address','month','organization','publisher','note']
    },
    'manual':{
    'required':['title'],
    'optional':['author','organization','address','edition','month','year','note']
    },
    'mastersthesis':{
    'required':['author','title','school','year'],
    'optional':['type','address','month','note']
    },
    'misc':{
    'required':[],
    'optional':['author','title','howpublished','month','year','note']
    },
    'phdthesis':{
    'required':['author','title','school','year'],
    'optional':['type','address','month','note']
    },
    'proceedings':{
    'required':['title','year'],
    'optional':['editor','volume','number','series','address','month','organization','publisher','note']
    },
    'techreport':{
    'required':['author','title','institution','year'],
    'optional':['type','number','address','month','note']
    },
    'unpublished':{
    'required':['author','title','note'],
    'optional':['month','year']
    }
             }

fieldnames = ['address','annote','author','booktitle','chapter','crossref','edition','editor','howpublished','institution','journal','key','month','note','number','organization','pages','publisher','school','series','title','type','volume','year']
otherFieldnames = ['day','doi','isbn','url','issn','pmid','arxivid','eprint']

class bibentry:
    def __init__(self,bibtype,key):
        bibtype = bibtype.lower()
        self.bibtype = bibtype
        self.key = key
        self.required = []
        self.optional = []
        self.ignored  = []
        self.others = []
        self.unknown = []
        self.fields = {}
        return None
    
    def __str__(self):
        #add start of the entry, like @article{name1996
        ans = "@"+self.bibtype+"{"+self.key+",\n"
        #remove dublicates from field lists and sort them alphabetically
        self.required = list(set(self.required))
        self.required.sort()
        self.optional = list(set(self.optional))
        self.optional.sort()
        self.ignored = list(set(self.ignored))
        self.ignored.sort()
        self.others = list(set(self.others))
        self.others.sort()
        #then put all of them together
        #if len(self.unknown) > 0:
        #    allfields = self.ignored + self.others + [''] + self.unknown
        #else:
        #    allfields = self.ignored + self.others
        allfields = self.ignored + self.others
        if len(allfields) > 0:
            allfields = self.required + self.optional + [''] + allfields
        else:
            allfields = self.required + self.optional
        if len(allfields) > 0:
            ans += "\n".join(allfields)
        #remove the separating ',' from the last line
        ans = ans.rstrip(",")
        #add the } to cloase the entry
        ans += "\n}\n"
        return ans

    def getvalue(self,key):
        if key in self.fields:
            return self.fields[key]
        return None

    def addline(self,line):
        global entry2field, fieldnames, otherFieldnames
        b = line.find("=")
        fieldtype = line[:b].lower()
        fieldtype = fieldtype.rstrip(" ").rstrip("\t").rstrip(" ")
        fieldtype = fieldtype.lstrip(" ").lstrip("\t").lstrip(" ")
        if fieldtype != "" and fieldtype != '}':
            a = line.find("{")
            b = line.rfind("}")
            value = tryFormat(self.key,fieldtype,line[a+1:b])
            #determine the best fit entry type:
            temptype = "misc"
            if self.bibtype in entry2field:
                temptype = self.bibtype
            #fix field type
            if fieldtype == "urldate":
                #Mendeley uses urldate for websites, but instead we want howpublished and note defined.
                fieldtype = "note"
                if temptype == "misc":
                    self.addline("howpublished = {Online}")
            if fieldtype == "type":
                #Mendeley doesn't differentiate between PhD and Master Thesis
                if "msc" in value.lower() or "master" in value.lower() or "bachelor" in value.lower() and self.bibtype in ["phdthesis","mastersthesis","thesis"]:
                    self.bibtype = "mastersthesis"
            #append to dictionary of fields
            self.fields[fieldtype] = value
            #format as line
            field = "    "+fieldtype+"\t= {"+value+"},"
            #append to the correct list of fields
            if fieldtype in entry2field[temptype]['required']:
                self.required.append(field)
            elif fieldtype in entry2field[temptype]['optional']:
                self.optional.append(field)
            elif fieldtype in fieldnames:
                self.ignored.append(field)
            elif fieldtype in otherFieldnames:
                self.others.append(field)
            else:
                self.unknown.append(field)
        return None
