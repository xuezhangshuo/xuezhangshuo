# coding=utf-8
from xuezhangshuo.course.models import *
from collections import defaultdict

with open('data/course_info_more_but_old.txt') as f:
    for line in f:
        items = defaultdict(str)
        for k,v in [ i.split(':',1) for i in line.split('@') ]:
            items[k] = v
        staff_id, teacher_name, gender  = items['工号'].lower(), items['姓名'], items['性别']
        course_id, course_name, year = items['课程代码'], items['课程名称'], items['学年'][:4]
        db_t, created = Teacher.objects.get_or_create(name=teacher_name,
                                             gender='M' if gender == '男' else 'F',
                                             staffID=staff_id)
        # print staff_id # use this to locate where it stops
        if course_id == '': continue
        db_c, created = Course.objects.get_or_create(name=course_name, courseID=course_id)
        db_ct, created = CourseTeacher.objects.get_or_create(teacher=db_t, course=db_c,
                                                             year=int(year), rank=0, rank_cnt=0)
                                                    
