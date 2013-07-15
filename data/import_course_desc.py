import pickle
from xuezhangshuo.course.models import *

f = open("data/course_desc.pickle",'r')
course_desc = pickle.load(f)

for courseID in course_desc.keys():
	try:
		course = Course.objects.get(courseID=courseID)
	except:
		pass
	else:
		content = course_desc[courseID]
		CourseDescription.objects.create(course=course, content=content)
		print courseID, "imported"
f.close()