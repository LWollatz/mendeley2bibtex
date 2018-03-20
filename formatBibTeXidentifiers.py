def _idgroup(number):
    first_digit = int(number[0])
    if first_digit <= 5 or first_digit == 7:
        group = number[0]
    elif first_digit == 6:
        group = number[:3]
    elif first_digit == 8:
        group = number[:2]
    elif int(number[:3]) == 999:
        group = number[:5]
    elif int(number[:2]) == 99:
        group = number[:4]
    else:
        if int(number[1]) <= 4:
            group = number[:2]
        else:
            group = number[:3]
    return group

def _idpublisher(number):
    if int(number[:2]) < 20:
        publisher = number[0:2]
    elif int(number[:3]) < 700:
        publisher = number[:3]
    elif int(number[:4]) < 8500:
        publisher = number[:4]
    elif int(number[:5]) < 90000:
        publisher = number[:5]
    elif int(number[:6]) < 950000:
        publisher = number[:6]
    else:
        publisher = number[:7]
    return publisher

def formatISBN10(ISBNt):
    #print "ISBN10"
    IDG = _idgroup(ISBNt)
    ISBNt = ISBNt[len(IDG):]
    IDP = _idpublisher(ISBNt)
    ISBNt = ISBNt[len(IDP):]
    ISBNout = IDG+"-"+IDP+"-"+ISBNt[:-1]+"-"+ISBNt[-1]
    return ISBNout

def formatISBN13(ISBNt):
    #print "ISBN13"
    if ISBNt[:3] == "978":
        IDE = "978"
    elif ISBNt[:3] == "979":
        IDE = "979"
    else:
        print "WARNING strange ISBN13",str(ISBN).replace("-","")
        IDE = ISBNt[:3]
    ISBNt = ISBNt[len(IDE):]
    IDG = _idgroup(ISBNt)
    ISBNt = ISBNt[len(IDG):]
    IDP = _idpublisher(ISBNt)
    ISBNt = ISBNt[len(IDP):]
    ISBNout = IDE+"-"+IDG+"-"+IDP+"-"+ISBNt[:-1]+"-"+ISBNt[-1]
    return ISBNout
   
def formatISBN(ISBN):
    """takes an ISBN and returns a string that splits the ISBN correctly"""
    ISBNt = str(ISBN)
    ISBNt = ISBNt.replace("ISBN","")
    ISBNt = ISBNt.replace(":","")
    ISBNt = ISBNt.replace(" ","")
    if(ISBNt.find("-") >= 0):
        return ISBNt
    ISBNt = ISBNt.replace("-","")
    if len(ISBNt) == 10:
        ISBN = formatISBN10(ISBNt)
    elif len(ISBNt) == 13:
        ISBN = formatISBN13(ISBNt)
    else:
        raise Exception("ISBN %s is of wrong length (%d), expected 10 or 13" % (ISBNt,len(ISBNt)))
    return str(ISBN)

def formatURL(url):
    url = url.replace("{\\_}","\\_").replace("{\\&}","\\&").replace("{\\#}","\\#")
    urls = url.split(" ")
    url = urls[0]
    return url

def formatDOI(doi):
    doi = str(doi)
    doi = doi.replace("http://","")
    doi = doi.replace("https://","")
    doi = doi.replace("dx.doi.org/","")
    doi = doi.replace("dx.doi.org","")
    doi = doi.replace("org","")
    doi = doi.replace("doi:","")
    doi = doi.replace("doi","")
    doi = doi.replace(" ","")
    doi = doi.lstrip(".")
    doi = doi.lstrip("/")
    return doi
