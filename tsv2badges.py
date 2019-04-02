#!/usr/bin/env python
# Generate badges svg
# USAGE: ./tsv2badges.py badges.svg badges.tsv; 

import os, sys, gzip

svgfn, tsvfn = sys.argv[1:3]

_svg = svg = "".join(open(svgfn).readlines())

names = [l[:-1].split('\t') for l in open(tsvfn) if l.strip() and not l.startswith('#')]

NAME = "Name surname"
USERPASS = "username"
AFFILIATION = "AFFILIATION"

i = 0
for data in names:
    name, user, passwd, affiliation = data[:4]
    # split name
    if len(name)<17:
        name = 25*" " + name #name.replace(" ", "\n", 1); print(name) #"\n"+name
    # strip affiliation
    if len(affiliation)>40:
        affs = affiliation.split(',')
        l = ii = 0
        while l<40:
            ii += 1
            l += len(affs[-ii])
        affiliation = ",".join(affs[-ii:])
            
    if NAME not in _svg:
        i += 1
        # store new svg
        outfn="%s.%s.svg"%(svgfn, i); print(outfn)
        with open(outfn, "w") as out:
            out.write(_svg)
        # convert to pdf and remove svg
        os.system("inkscape %s --export-pdf=%s.pdf"%(outfn, outfn)); os.unlink(outfn)
        # reset template
        _svg = svg
        
    # replace
    _svg = _svg.replace(NAME, name, 1).replace(USERPASS, "u: %s p: %s"%(user, passwd), 1).replace(AFFILIATION, affiliation, 1)
    
if _svg != svg: 
    i += 1
    while NAME in _svg:
        _svg = _svg.replace(NAME, "", 1).replace(USERPASS, "", 1).replace(AFFILIATION, "", 1)
    # store new svg
    outfn="%s.%s.svg"%(svgfn, i); print(outfn)
    with open(outfn, "w") as out:
        out.write(_svg)
    # convert to pdf and remove svg
    os.system("inkscape %s --export-pdf=%s.pdf"%(outfn, outfn)); os.unlink(outfn)
    
os.system("gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=%s.pdf -dBATCH %s*svg.pdf"%(svgfn, svgfn))
print("rm  %s*svg.pdf"%svgfn)

