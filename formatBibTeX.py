import errorHandler as err
import formatBibTeXidentifiers as fmtID
import formatBibTeXhelpers as helper
import re
from LaTeXstringify import *


#standard reg-ex you like your BibTeX keys to look like
keyPattern = "^[a-z]{2,4}[0-9]{4}[a-z]{0,1}$"




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
    booktitle = helper.keepAbbreviations(booktitle)
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



def formatEdition(edition):
    """The edition of a book--for example, ``Second''. This should be an
       ordinal, and should have the first letter capitalized, as shown here;
       the standard styles convert to lower case when necessary."""
    
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
       edition = helper.small2eng(edition)
    except ValueError:
        pass
    #now it's definitely text, just need to format it to ordinal
    edition = helper.TextToOrdinal(edition)
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



def formatMonth(month):
    """The month in which the work was published or, for an unpublished work,
       in which it was written. You should use the standard three-letter
       abbreviation, as described in Appendix B.1.3 of the LATEX book. """
    desMonths = helper.getMonthFormat()
    try:
        month = helper.formatIntMonth(month,desMonths)
    except ValueError:
        month = helper.formatStrMonth(month,desMonths)
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
    title = helper.keepAbbreviations(title)
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



fncmapping = {"address":formatAddress,
              "annote":formatAnnote,
              "author": formatAuthor,
              "booktitle": formatBooktitle,
              "chapter": formatChapter,
              "crossref": formatCrossref,
              "edition": formatEdition,
              "editor": formatEditor,
              "howpublished": formatHowpublished,
              "institution": formatInstitution,
              "journal": formatJournal,
              "key": formatKey,
              "month": formatMonth,
              "note": formatNote,
              "number": formatNumber,
              "organization": formatOrganization,
              "pages": formatPages,
              "publisher": formatPublisher,
              "school": formatSchool,
              "series": formatSeries,
              "title": formatTitle,
              "volume": formatVolume,
              "year": formatYear,
              "isbn": formatISBN,
              "url": formatURL,
              "doi": formatDOI,
              "pmid": formatPMID,
              "issn": formatISSN,
              "day": formatDay,
              "urldate": formatUrldate
              }
# distributer

def doFormat(fieldtype,value):
    global fncmapping
    fieldtype = fieldtype.lower()
    if fieldtype in fncmapping:
        value = fncmapping[fieldtype](value)
    return value




