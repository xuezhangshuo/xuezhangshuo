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

###Reference
[Configure PostgreSQL on Mac OS](http://ruby.zigzo.com/2012/07/07/postgresql-postgres-app-and-a-gotcha-on-mac-osx-lion/)

###Appendix
- Info extraction:

        pat=">工号\|>姓名\|>性别\|>学位\|>民族\|>毕业学校\|>职称\|>课程代码\|>课程名称\|>课号\|>学年"
        find . -type f -print | xargs grep -A 1 -h $pat > test.output

    Then use vim to do the dirty work.
- Load into PostgreSQL via `python manage.py shell`:

        import sys
        sys.path.append('absolute/path/to/current/data-folder')
        import rotedb_more_but_old
        # or import rotedb_new_but_simple
        # only one of them, since they are not compatible 



### TO DO LIST
finish before 7.14 11:59:59
1.login logout register :edfward
	bug
	autologin after register when redirect to homwpage
2.course page :zhoutall
	vote
	comment
	course_description
3.personal profile :quarkjokerrrrrrr
	personal infomation
    change info
	个人动态

