#helper functions

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
