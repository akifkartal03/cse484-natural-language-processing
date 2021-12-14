import sys
import re

import sys
import re

def hypo(x):
    isPython2 = False;
    if sys.version_info[0] < 3:
        isPython2 = True
    i = 0
    vw = "aeıioöuü"
    cn = "bcçdfgğhjklmnprsştvyz"
    if isPython2:
        vw = vw.decode("utf-8")
        cn = cn.decode("utf-8")
    while i < len(x):
        if x[i] in vw:
            if i + 1 < len(x) and x[i+1] in vw:
                return x[0:i+1] + " " + hypo(x[i+1:len(x)])
            elif i + 2 < len(x) and x[i+2] in vw:
                return x[0:i+1] + " " + hypo(x[i+1:len(x)])
            elif i + 3 == len(x) and x[i+1] in cn and x[i+2] in cn:
                return x[0:i+3] + " " + hypo(x[i+3:len(x)])
            elif i + 3 < len(x) and x[i+3] in vw:
                return x[0:i+2] + " " + hypo(x[i+2:len(x)])
            elif i+3 < len(x) and x[i+1] in cn and x[i+2] in cn and x[i+3] in cn:
                return x[0:i+3] + " " + hypo(x[i+3:len(x)])
            elif i + 3 < len(x) and x[i:i+3] == 'str' or 'ktr' or 'ntr':
                return x[0:i+2] + " " + hypo(x[i+2:len(x)])
            else:
                return x[0:i+3] + " " + hypo(x[i+3:len(x)])
        i += 1

    return x

def lowerWithoutTurkish(str):
    rep = [('I','ı'),('İ','i')]
    for search, replace in rep:
            str = str.replace(search, replace)
    return str.lower()
