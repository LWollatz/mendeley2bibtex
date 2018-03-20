#this file provides functions to convert strings to LaTeX

#check https://tex.stackexchange.com/tags/accents/info
#and detexify
_UNICODE = {
    139: '\guilsinglleft{}',
    147: '``',
    160: ' ',
    177: '+-',
    181: '\textmu{}',
    194: '\^{A}',
    226: '\^{a}',
    254: '',
    255: '',
    277: '\u{e}',
    287: '\u{g}',
    304: '\.{I}',
    305: '\i{}',
    351: "\c{s}",
    8208: '-',
    8209: '-',
    8210: '--',
    8211: '--',
    8212: '--',
    8213: '--',
    8216: "`",
    8217: "'",
    8218: ",",
    8219: "`",
    8220: "``",
    8221: "''",
    8222: '"`',
    8223: "``",
    8249: "\textsmaller{}",
    8250: "\textgreater{}",
    9147: '-',
    9148: '-',
    9679: '*',
    9692: "'",
    9693: "`",
    9694: ",",
    65533: ''
    }

def remSpecialChar(text):
    """removes special LaTeX/BibTeX characters from a string"""
    text = text.replace("{","").replace("}","")
    text = text.replace("\\","")
    text = text.replace("&","")
    return text

def remUnicode(text):
    """removes unicode characters from a string - doesn't really work yet."""
    #encoding = detect(text)['encoding']
    #print encoding
    #text = unicode(text,encoding,errors='ignore')
    #text = text.encode("utf-32")
    #for code in _UNICODE:
    #    text = text.replace(code, _UNICODE[code])
    #try:
    #    text = text.encode("ascii")
    #except UnicodeDecodeError:
    #    text = text.decode("utf-8")
    cleantext = ""
    for char in text:
        if ord(char) in _UNICODE:
            cleantext += _UNICODE[ord(char)]
        elif ord(char) >= 128:
            print "unkown LaTeX escape for unicode "+unichr(ord(char)).__repr__()+" - please define "+str(ord(char))+": "+unichr(ord(char))+" in formatBibTeX"#+text+"\n"
            cleantext += char
        else:
            cleantext += char
    return cleantext.encode("ascii")
