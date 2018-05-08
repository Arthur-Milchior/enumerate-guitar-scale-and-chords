increase_fret_limit = 4
decreasing_fret_limit=4

import os
from util import *
from data import * 
def scale2Pos(scale_dif,basePos):
    poss = [basePos]
    lastPos =basePos
    firstFret = basePos.fret
    for ivl in scale_dif:
        pos = lastPos.add(ivl, min = max(lastPos.fret -4,1), max = firstFret +4)
        if pos is None:
            return False
        if pos.string != lastPos.string:
            firstFret= pos.fret
        poss.append(pos)
        lastPos = pos
    return poss

major = [2,2,1,2,2,2,1]
pos1= Pos(1,1)
index = """<html><head><title>All transposable scale on a standard guitar</title></head>
<body>
Here is the list of each scales I found in English wikipedia. With the exception of the scales which can not be easily be played on guitar, e.g. scales using interval smaller than half-tones.

For each of them, there is the list of way to play this scale, on one octave, on a standard guitar fret. The only exception being the <a href="https://en.wikipedia.org/wiki/Algerian_scale">Algerian scale</a> which, by definition, is played on two octaves.

Here are the technical restrictions I used, to choose which scale's position to generates.
<ul><li>
It is assumed that, there is never more than %d fret from the first to the last note played on a single string.
</li><li> Furthermore, there is never more than %d fret in distance from the the highest note played on a string, and the lowest note played on the following string. </li></lu>
<ul>
"""%(increase_fret_limit,decreasing_fret_limit)

for (names,scale_dif) in scales_dif:
    name = names[0]
    folder = "scale/"+name
    ensureFolder(folder)
    web = """<html><head><title>All transposable %s on a standard guitar</title></head><body>Each transposable version of the scale %s.<br/> Successive notes are separated by %s half-notes
<hr/>"""%(name,name, str(scale_dif))
    for string in range(1,7):
        for fret in range(1,5):
            print ("""considering %s %d-%d"""%(name,string,fret))
            basePos = Pos(string,fret)
            poss = scale2Pos(scale_dif, basePos)
            if poss is False:
                print("poss is false:continue")
                continue
            file ="%d-%d-%s.svg"%( string, fret, name)
            path = "%s/%s" %(  folder,file)
            sop=SetOfPos(poss)
            print(sop)
            if not sop.isOneMin():
                print("no one:continue")
                continue
            print("drawing")
            with open (path, "w") as f:
                sop.draw(f)
            web += """<img src="%s"/>\n"""%file
    web+="""</body></html>"""
    index += """<li><a href="%s">"""%name
    for name in names:
        index += "%s, " % name
    index +="""</a></li>"""
    with open("%s/index.html"% folder,"w") as f:
        f.write(web)



index +="""</ul></body>
</html>"""
with open("scale/index.html","w") as f:
    f.write(index)
