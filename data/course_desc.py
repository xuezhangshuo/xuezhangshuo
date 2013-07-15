import re
re_courseID = re.compile('^\w\w\d\d\d$')

description = {}

with open('course_desc_raw.txt') as f:
    for line in f:
        line = line.rstrip()
        if re_courseID.match(line):
            key = line
            description[key] = ""
        elif line != "":
            description[key] += line+"\n"

# optional print
# for k in description:
#     print k,"\n",description[k],"#######"

# optional pickle
import pickle
pkd_f = open('./course_desc.pickle', 'wb')
pickle.dump(description, pkd_f)
pkd_f.close()
