AllErrors=[]
AllWarnings=[]
mainVerbose=True

def raiseError(msg,verbose=mainVerbose):
    global AllErrors
    AllErrors.append(msg)
    if verbose:
        print "ERROR: "+msg
    return None

def raiseWarning(msg,verbose=mainVerbose):
    global AllWarnings
    AllWarnings.append(msg)
    if verbose:
        print "WARNING: "+msg
    return None
