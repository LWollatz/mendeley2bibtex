#helper functions

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


def keepAbbreviations(title):
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

def TextToOrdinal(text):
    num2ord={"one":"first","two":"second","three":"third","five":"fifth","twelve":"twelfth"}
    #defend = True
    for num in num2ord.keys():
        if text.endswith(num):
            text = text[:-1*len(num)]+num2ord[num]
            #defend = False
            #break
            return text
    #if defend:
    if text.endswith("e"):
        text = text[:-1]
    if text.endswith("t"):
        text = text[:-1]
    text = text+"th"
    return text

def _get_num(num):
    '''Get token <= 90, return '' if not matched'''
    return _SMALL.get(num, '')

def _norm_num(num):
    """Normelize number (remove 0's prefix). Return number and string"""
    n = int(num)
    return n, str(n)

def small2eng(num):
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

def getMonthFormat(form="short"):
    if form == "long":
        desMonths = ["","January","February","March","April","May", "June", "July", "August", "September", "October", "November", "December"]
    elif form == "number":
        desMonths = ["","1","2","3","4","5", "6", "7", "8", "9", "10", "11", "12"]
    else:
        desMonths = ["","Jan","Feb","Mar","Apr","May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return desMonths

def formatIntMonth(month,desMonths):
    month = int(month)
    if month >= 1 and month <= 12:
        month = desMonths[month]
    else:
        raise Exception("couldn't identify month "+month)
        month = desMonths[0]
    return month

def formatStrMonth(month,desMonths):
    month = month.lower()
    monthX = desMonths[0]
    for m in desMonths[1:]:
        if m.lower() in month:
            monthX = m
    return monthX
