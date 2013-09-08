#学长说
******

###Development
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

******

###Production

#### 1. Apache Config

Install `mod_wsgi` which enables apache to serve python web apps, then restart

    $ sudo apt-get install libapache2-mod-wsgi
	$ sudo service apache2 restart

create the virtual host file
    
	$ sudo vi /etc/apache2/sites-available/myapp.com

which looks like:
```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName myapp.com
    ServerAlias www.myapp.com
    WSGIScriptAlias / var/www/mydomain.com/django.wsgi

    Alias /static/ /var/www/mydomain.com/static/
    <Location "/static/">
        Options -Indexes
    </Location>
</VirtualHost>
```
The wsgi file is executed when the domain gets accessed. And the `static` folder could be a soft link pointed to the one hosted under the app (or the collection via `collectstatic` command).

Then enable the site
    
	$ sudo a2ensite myapp.com 

(Note that after editing those site files, a reload is needed to make them effective)

	$ sudo service apache2 reload

#### 2. Django Config

Edit the wsgi file:
```python
import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/myprojectenv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/django_projects/MyProject')
sys.path.append('/home/django_projects/MyProject/myproject')

os.environ['DJANGO_SETTINGS_MODULE'] = 	'myproject.settings'

# Activate your virtual env
activate_env=os.path.expanduser("~/.virtualenvs/myprojectenv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```
And the `settings.py`
```python
STATIC_ROOT = '/var/www/mydomain.com/static/'
STATIC_URL = '/static/'
```
**OPTIONAL collectstatic**: if there are multiple apps and their static files are different, it's necessary to put them together and make them recognizable by apache

    $ python manage.py collectstatic

This command calls django to collect static files in each app and some other places, then store into `STATIC_ROOT` configured in `settings.py`

******

### Import Course Description

1. updata schema

		$ python manage.py sqlclear course | psql xuezhangshuo
		$ python manage.py syncdb

2. drop all tables:

        drop table course_coursedescription cascade;
        drop table course_teacher cascade;
        drop table course_course cascade;
        drop table course_courseteacher cascade;
        drop table course_comment cascade;
        drop table course_vote cascade;
        drop table course_coursedescription_contributors cascade;

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

******

###Reference
[Configure PostgreSQL on Mac OS](http://ruby.zigzo.com/2012/07/07/postgresql-postgres-app-and-a-gotcha-on-mac-osx-lion/)
[Deploy Django on Apache with Virtualenv and mod_wsgi](http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/)


******

###Appendix
- course_teacher info extraction:

        pat=">工号\|>姓名\|>性别\|>学位\|>民族\|>毕业学校\|>职称\|>课程代码\|>课程名称\|>课号\|>学年"
        find . -type f -print | xargs grep -A 1 -h $pat > test.output

    Then use vim to do the dirty work.


