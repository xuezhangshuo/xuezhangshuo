#!/usr/bin/env python
import csv
import re
from xuezhangshuo.course.models import *

contents = []
re_teacher = re.compile('\)\.([^ ]*)')
re_courseID = re.compile('\)(.*)\(')

with open('course_info_new_but_simple.csv', 'rb') as csvfile:
    csvfile.readline() # skip first line
    creader = csv.reader(csvfile)
    for row in creader:
        teachers = set()
        course = row[3].rstrip()
        for line in row[7].split('\n'):
            t = re_teacher.findall(line.rstrip())
            if t != []: teachers.add(t[0])
        courseID = re_courseID.findall(row[4])[0]
        year = row[-3][:4]
        contents.append( (course, courseID, year, teachers) )

# insert teachers
teachers = set([t for c, cID, y, teachers in contents for t in teachers])
for t in teachers:
    db_t = Teacher.objects.create(name=t)

# insert course-teacher associations
for c, cID, y, teachers in contents:
    db_c = Course.objects.create(courseID=cID, name=c)
    for teacher in teachers:
        db_t = Teacher.objects.get(name__exact=teacher)
        ct = CourseTeacher.objects.get_or_create(teacher=db_t, 
                                          course=db_c,
                                          year=y,
                                          rank=0,
                                          rank_cnt=0)

