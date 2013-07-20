#学长说
******

###Deployment
In `xuezhangshuo` directory:

```
virtualenv venv --distribute
```

```
source venv/bin/activate
```

```
pip install Django psycopg2 gunicorn bleach
```

```
python manage.py runserver
```

### Import Course Description

1. updata schema

		$ python manage.py sqlclear course | psql xuezhangshuo
		$ python manage.py syncdb

2. regenerate pickle

		$ cd data
		$ python course_desc.py

3. import

		$ cd ..
		$ python manage.py syncdb
		$ python manage.py shell
		>>> from data import import_course_teacher
		>>> from data import import_course_desc
		>>> quit()

###Reference
[Configure PostgreSQL on Mac OS](http://ruby.zigzo.com/2012/07/07/postgresql-postgres-app-and-a-gotcha-on-mac-osx-lion/)

###Appendix
- Info extraction:

        pat=">工号\|>姓名\|>性别\|>学位\|>民族\|>毕业学校\|>职称\|>课程代码\|>课程名称\|>课号\|>学年"
        find . -type f -print | xargs grep -A 1 -h $pat > test.output

    Then use vim to do the dirty work.


