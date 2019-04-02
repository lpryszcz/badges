#!/usr/bin/env python

# USAGE: python get_usernames.py participants.txt > badges.tsv

import codecs, os, random, string, sys, unicodedata

fn = sys.argv[1]

UTF8Reader = codecs.getreader('utf8')
handle = UTF8Reader(open(fn))

N=5
homebase = "/home/" # /ngschool/users/
gid = 1100
badgeline = "%s\t%s\t%s\t%s\n"
unameline = "%s:%s:%s:%s:%s,,,:%s:/bin/bash\n"

def normalize_char(c):
    try:
        cname = unicodedata.name(c)
        cname = cname[:cname.index(' WITH')]
        return unicodedata.lookup(cname)
    except (ValueError, KeyError):
        return c

def normalize(s):
    return ''.join(normalize_char(c) for c in s)

# get writer
UTF8Writer = codecs.getwriter('utf8')
out1, out2 = open(fn+".badges.tsv", "w"), open(fn+".newusers", "w")
out1, out2 = UTF8Writer(out1), UTF8Writer(out2)

# process
#for uid, full_name in enumerate(sys.stdin, gid+1):
#    first, family = full_name.lower().split()[:2]
for uid, info in enumerate(handle, gid+1):
    first, family, affiliation = info[:-1].split('\t')
    full_name = " ".join([first, family])
    uname = normalize("%s%s"%(first[0].split()[0], family.split()[0]))
    uname = uname.lower()
    pwd = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, N))
    out1.write(badgeline%(full_name.strip(), uname, pwd, affiliation))#, uid, gid, os.path.join(homebase, uname)))
    out2.write(unameline%(uname, pwd, uid, gid, full_name.strip(), os.path.join(homebase, uname)))

sys.stderr.write("""Now execute
- to create badges:
 ./tsv2badges.py badges.svg %s.badges.tsv 
- to create user accounts:                 
 while read line; do echo $line; echo $line | sudo newusers; done < %s.newusers\n"""%(fn, fn))