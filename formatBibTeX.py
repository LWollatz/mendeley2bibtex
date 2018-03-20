import errorHandler as err
import formatBibTeXidentifiers as fmtID
import re
from LaTeXstringify import *


#standard reg-ex you like your BibTeX keys to look like
keyPattern = "^[a-z]{2,4}[0-9]{4}[a-z]{0,1}$"

fixedterms = ['.NET','2D','3D']
fixedterms += ['ACCP','ACR-STR','ALAT','ASTM','ASTM','Amira 3D','Avizo 3D','Azure','ATS','Aquilion ONE / GENESIS Edition']
fixedterms += ['BMP','Bing','BioImage','BisQue','Bisquik','BrainMaps','BrainMaps']
fixedterms += ['CAP','COPD','CT','CellProfiler','CAD']
fixedterms += ['DICOM','DICONDE','Dcm-Ar','Deep Zoom']
fixedterms += ['EMBC','EMI','EMR','ERS','eScience']
fixedterms += ['FACTA','FEMA','FITS','Facebook',"Fiji"]
fixedterms += ['GIF','Google Maps']
fixedterms += ['HELP','HRCT','HTML5','Hadoop','HL7']
fixedterms += ['IEEE','ImageJ','ImageJ2','iPad','IoT','IPF','IT']
fixedterms += ['JPEG','JPG','JSON','JavaScript','JRS']
fixedterms += ['LinkBench','LB-Index','LungJ']
fixedterms += ['MR','MRI','Microsoft','MySQL','MCTV','MX16Evo','MEDJACK.2','MS-FSA']
fixedterms += ['NASA','NEMA','NHS','NoSQL','NIH','NSIP']
fixedterms += ['OAIS','OLAWSDS','OME','OMERO','OsiriX','OsiriX MD']
fixedterms += ['PACS','PET','PNG','ParaView','Philips']
fixedterms += ['RDBMS','RDF','RabbitMQ','RIS','Raspberry Pi']
fixedterms += ['SPIE','SPECT','SQL','STORM','ScImage','Silverlight','SOMATOM Perspective']
fixedterms += ['TIF','TIFF']
fixedterms += ['US'] #check this doesn't cause issues
fixedterms += ['V3D','V3D','VA','VGStudio MAX','VESSEL12']
fixedterms += ['WebGL','Windows']
fixedterms += ['XBM','XML','Yahoo','Zoomify']
fixedterms.sort(key=lambda x: x.upper(),reverse=False)
strterms = "['" + "','".join(fixedterms) + "']"
fixedterms.sort(key=lambda x: len(x),reverse=True)

_SMALL = {
        '0' : '',
        '1' : 'one',
        '2' : 'two',
        '3' : 'three',
        '4' : 'four',
        '5' : 'five',
        '6' : 'six',
        '7' : 'seven',
        '8' : 'eight',
        '9' : 'nine',
        '10' : 'ten',
        '11' : 'eleven',
        '12' : 'twelve',
        '13' : 'thirteen',
        '14' : 'fourteen',
        '15' : 'fifteen',
        '16' : 'sixteen',
        '17' : 'seventeen',
        '18' : 'eighteen',
        '19' : 'nineteen',
        '20' : 'twenty',
        '30' : 'thirty',
        '40' : 'forty',
        '50' : 'fifty',
        '60' : 'sixty',
        '70' : 'seventy',
        '80' : 'eighty',
        '90' : 'ninety'
    }

globalkeys=[]

# distributer

def doFormat(fieldtype,value):
    global globalkeys
    fieldtype = fieldtype.lower()
    if fieldtype == "address":
        value = formatAddress(value)
    elif fieldtype == "annote":
        value = formatAnnote(value)
    elif fieldtype == "author":
        value = formatAuthor(value)
    elif fieldtype == "booktitle":
        value = formatBooktitle(value)
    elif fieldtype == "chapter":
        value = formatChapter(value)
    elif fieldtype == "crossref":
        value = formatCrossref(value,globalkeys)
    elif fieldtype == "edition":
        value = formatEdition(value)
    elif fieldtype == "editor":
        value = formatEditor(value)
    elif fieldtype == "howpublished":
        value = formatHowpublished(value)
    elif fieldtype == "institution":
        value = formatInstitution(value)
    elif fieldtype == "journal":
        value = formatJournal(value)
    elif fieldtype == "key":
        value = formatKey(value)
    elif fieldtype == "month":
        value = formatMonth(value)
    elif fieldtype == "note":
        value = formatNote(value)
    elif fieldtype == "number":
        value = formatNumber(value)
    elif fieldtype == "organization":
        value = formatOrganization(value)
    elif fieldtype == "pages":
        value = formatPages(value)
    elif fieldtype == "publisher":
        value = formatPublisher(value)
    elif fieldtype == "school":
        value = formatSchool(value)
    elif fieldtype == "series":
        value = formatSeries(value)
    elif fieldtype == "title":
        value = formatTitle(value)
    elif fieldtype == "type":
        value = formatType(value)
    elif fieldtype == "volume":
        value = formatVolume(value)
    elif fieldtype == "year":
        value = formatYear(value)
    
    #print("non-standard field %s",fieldtype)
    if fieldtype == "isbn":
        value = formatISBN(value)
    elif fieldtype == "url":
        value = formatURL(value)
    elif fieldtype == "doi":
        value = formatDOI(value)
    elif fieldtype == "pmid":
        value = formatPMID(value)
    elif fieldtype == "issn":
        value = formatISSN(value)
    elif fieldtype == "day":
        value = formatDay(value)
    elif fieldtype == "urldate":
        value = formatUrldate(value)
    elif fieldtype == "abstract":
        value = value

    
    
    
    #print "unknown field '%s'" % (fieldtype)
    return value

#standard fields

def formatAddress(address):
    """Usually the address of the publisher or other type of institution.
       For major publishing houses, van Leunen recommends omitting the
       information entirely. For small publishers, on the other hand, you
       can help the reader by giving the complete address."""
    #format city, country, standardize the country
    return address

def formatAnnote(annote):
    """An annotation. It is not used by the standard bibliography styles,
       but may be used by others that produce an annotated bibliography. """
    #clear from special characters
    annote = remSpecialChar(annote)
    return annote 

def formatAuthor(author):
    """The name(s) of the author(s), in the format described in the LATEX
       book"""
    #no need to do anyting except if empty, replace with pre-defined default
    return author

def formatBooktitle(booktitle):
    """Title of a book, part of which is being cited. See the LATEX book for
       how to type titles. For book entries, use the title field instead."""
    booktitle = _keepAbbreviations(booktitle)
    if booktitle.startswith("Proceedings"):
        booktitle = booktitle.replace("Proceedings","Proc.")
    if booktitle.startswith("Transactions"):
        booktitle = booktitle.replace("Transactions","Trans.")
    return booktitle

def formatChapter(chapter):
    """A chapter (or section or whatever) number."""
    try:
        chapter = str(int(chapter))
    except ValueError:
        raise ValueError("Chapter %s is not a number" % chapter)
        pass
    return chapter

def formatCrossref(crossref,keys=None):
    """The database key of the entry being cross referenced."""
    #if keys provided, check that crossref is in keys
    if (keys != None):
        if crossref in keys:
            return crossref
        else:
            raise KeyError("The crossreference %s was not found in the existing list of keys",crossref)
    return crossref

def _TextToOrdinal(text):
    defend = True
    for num in num2ord.keys():
        if text.endswith(num):
            text = text[:-1*len(num)]+num2ord[num]
            defend = False
            break
    if defend:
        if text.endswith("e"):
            text = text[:-1]
        if text.endswith("t"):
            text = text[:-1]
        text = text+"th"
    return text

def formatEdition(edition):
    """The edition of a book--for example, ``Second''. This should be an
       ordinal, and should have the first letter capitalized, as shown here;
       the standard styles convert to lower case when necessary."""
    num2ord={"one":"first","two":"second","three":"third","five":"fifth","twelve":"twelfth"}
    edition = str(edition)
    edition = edition.lower()
    edition = edition.replace("edition","")
    if edition.endswith("th") or edition.endswith("st") or edition.endswith("nd") or edition.endswith("rd"):
        try:
            edition = int(edition[:-2])
        except ValueError:
            return edition.capitalize() #already in right format
    #if we reach here, then the edition is not in the right format,
    #but is it a number or a text?
    try:
       edition = float(edition)
       edition = _small2eng(edition)
    except ValueError:
        pass
    #now it's definitely text, just need to format it to ordinal
    edition = _TextToOrdinal(edition)
    return edition.capitalize()

def formatEditor(editor):
    """Name(s) of editor(s), typed as indicated in the LATEX book. If there is
       also an author field, then the editor field gives the editor of the book
       or collection in which the reference appears. """
    return editor

def formatHowpublished(howpublished):
    """How something strange has been published. The first word should be
       capitalized. """
    return howpublished.capitalize()

def formatInstitution(institution):
    """The sponsoring institution of a technical report."""
    return institution

def formatJournal(journal,abbrev=True):
    """A journal name. Abbreviations are provided for many journals; see the
       Local Guide."""
    #abbreviate or expand?
    return journal

def formatKey(key):
    """Used for alphabetizing, cross referencing, and creating a label when
       the ''author'' information (described in Section 4) is missing. This
       field should not be confused with the key that appears in the \cite
       command and at the beginning of the database entry. """
    if " " in key:
        raise ValueError("errornous key: "+key)
    elif not re.match(keyPattern,key):
        err.raiseWarning("strange key: "+key)
    return key

def formatMonth(month,form="short"):
    """The month in which the work was published or, for an unpublished work,
       in which it was written. You should use the standard three-letter
       abbreviation, as described in Appendix B.1.3 of the LATEX book. """
    if form == "long":
        desMonths = ["","January","February","March","April","May", "June", "July", "August", "September", "October", "November", "December"]
    elif form == "number":
        desMonths = ["","1","2","3","4","5", "6", "7", "8", "9", "10", "11", "12"]
    else:
        desMonths = ["","Jan","Feb","Mar","Apr","May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    try:
        month = int(month)
        if month >= 1 and month <= 12:
            month = desMonths[month]
        else:
            raise Exception("couldn't identify month "+month)
            month = desMonths[0]
    except ValueError:
        month = month.lower()
        monthX = desMonths[0]
        for m in desMonths[1:]:
            if m.lower() in month:
                monthX = m
        month = monthX
    return month

def formatNote(note):
    """Any additional information that can help the reader. The first word
       should be capitalized. """
    note = remSpecialChar(note)
    return note

def formatNumber(number):
    """The number of a journal, magazine, technical report, or of a work in a
       series. An issue of a journal or magazine is usually identified by its
       volume and number; the organization that issues a technical report
       usually gives it a number; and sometimes books are given numbers in a
       named series. """
    try:
        number = str(int(number))
    except ValueError:
        raise ValueError("Number %s is not a number" % number)
    return number

def formatOrganization(organization):
    """The organization that sponsors a conference or that publishes a manual."""
    return organization

def formatPages(pages):
    """One or more page numbers or range of numbers, such as 42-111 or 7,41,73-97
       or 43+ (the `+' in this last example indicates pages following that don't
       form a simple range). To make it easier to maintain Scribe-compatible
       databases, the standard styles convert a single dash (as in 7-33) to the
       double dash used in TEX to denote number ranges (as in 7-33)."""
    #check -- or ---- or -
    return pages

def formatPublisher(publisher):
    """The publisher's name. """
    return publisher

def formatSchool(school):
    """The name of the school where a thesis was written. """
    return school

def formatSeries(series):
    """The name of a series or set of books. When citing an entire book, the
       title field gives its title and an optional series field gives the name
       of a series or multi-volume set in which the book is published. """
    return series

def formatTitle(title):
    """The work's title, typed as explained in the LATEX book."""
    #replace {} in title to match fixed terms as defined elsewhere
    title = title.lstrip("\t").rstrip("\t")
    title = title.lstrip(" ").rstrip(" ")
    #title = title.title()
    title = _keepAbbreviations(title)
    return title

def formatType(btype):
    """The type of a technical report--for example, ''Research Note''"""
    return btype

def formatVolume(volume):
    """The volume of a journal or multivolume book. """
    return str(int(volume))

def formatYear(year):
    """The year of publication or, for an unpublished work, the year it was
       written. Generally it should consist of four numerals, such as 1984,
       although the standard styles can handle any year whose last four
       nonpunctuation characters are numerals, such as `(about 1984)'."""
    ans = ""
    for char in str(year):
        try:
            c = int(char)
            ans += str(c)
        except ValueError:
            pass
    return str(int(ans))

#Non-standard fields

def formatDay(day):
    """This is a non-standard field. If you want to include information for
       the day of the month, the month field is usually the best place. For
       example
         month = jul # "~4,"
       will probably produce just what you want."""
    return str(int(day))

def formatISBN(isbn):
    return fmtID.formatISBN(isbn)

def formatISSN(issn):
    return issn

def formatURL(url):
    return fmtID.formatURL(url)
    
def formatUrldate(urldate):
    urldate = str(urldate)
    if "-" in urldate:
        urldate = urldate.split("-")
        urldate.reverse()
        urldate = "/".join(urldate)
    return "Accessed on " + urldate

def formatDOI(doi):
    return fmtID.formatDOI(doi)

def formatPMID(pmid):
    return pmid







#helper functions

def _keepAbbreviations(title):
    global fixedterms
    if title.startswith("{") and title.endswith("}"):
        if not title[1:-1] in fixedterms:
            title = title[1:-1]
    specialcharsS = [' ','(','[','-','"',"'","`"]
    specialcharsE = [' ',':',',',';','.',')',']','!','?','-','"',"'"]
    title = " " + title + " "
    for term in fixedterms:
        title = title.replace("{"+term+"}",term)
        for f1 in specialcharsS:
            for f2 in specialcharsE:
                title = title.replace(f1+term+f2,f1+"{"+term+"}"+f2)
        #title = title.replace(" "+term+" "," {"+term+"} ")
        #title = title.replace(" "+term+","," {"+term+"},")
        #title = title.replace(" "+term+":"," {"+term+"}:")
    title = title.rstrip(" ").lstrip(" ")
    return title

def _get_num(num):
    '''Get token <= 90, return '' if not matched'''
    return _SMALL.get(num, '')

def _norm_num(num):
    """Normelize number (remove 0's prefix). Return number and string"""
    n = int(num)
    return n, str(n)

def _small2eng(num):
    '''English representation of a number <= 999
       taken from http://www.blog.pythonlibrary.org/2010/10/21/python-converting-numbers-to-words/
       '''
    global _SMALL
    n, num = _norm_num(num)
    hundred = ''
    ten = ''
    if len(num) == 3: # Got hundreds
        hundred = _get_num(num[0]) + ' hundred'
        num = num[1:]
        n, num = _norm_num(num)
    if (n > 20) and (n != (n / 10 * 10)): # Got ones
        tens = _SMALL.get(num[0] + '0', '')
        ones = _SMALL.get(num[1], '')
        ten = tens + ' ' + ones
    else:
        ten = _SMALL.get(num, '')
    if hundred and ten:
        return hundred + ' ' + ten
        #return hundred + ' and ' + ten
    else: # One of the below is empty
        return hundred + ten
