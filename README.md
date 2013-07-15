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
pip install Django psycopg2 gunicorn
```

```
python manage.py runserver
```

### Import Course Description

1. updata schema

```
$ psql xuezhangshuo
xuezhangshuo=# drop table course_coursedescription cascade;
xuezhangshuo=# \q
$ python manage.py syncdb
```

2. regenerate pickle

```
$ cd data
$ python course_desc.py
```

3. import

``` 
$ cd ..
$ python manage.py syncdb
$ python manage.py shell
>>> from data import import_course_teacher
>>> from data import import_course_desc
>>> quit()
```

###Reference
[Configure PostgreSQL on Mac OS](http://ruby.zigzo.com/2012/07/07/postgresql-postgres-app-and-a-gotcha-on-mac-osx-lion/)

###Appendix
- Info extraction:

        pat=">工号\|>姓名\|>性别\|>学位\|>民族\|>毕业学校\|>职称\|>课程代码\|>课程名称\|>课号\|>学年"
        find . -type f -print | xargs grep -A 1 -h $pat > test.output

    Then use vim to do the dirty work.

### TO DO LIST
***finish before 7.14 11:59:59 ***

- login logout register :edfward
    - bug
    - autologin after registering when redirect to homwpage
- course page :zhoutall
    - vote
    - comment
    - course_description
- personal profile :quarkjokerrrrrrr
    - personal infomation
    - change info
    - 个人动态

