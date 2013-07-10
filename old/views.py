#coding:utf8


RENREN_APP_API_KEY = "7df9e81ce8a14f64a4f1112cb0cc80d8"
RENREN_APP_SECRET_KEY = "33545b373da24dfba715eadf7e53db3c"


RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"
REDIRECT_URI = "http://www.xuezhangshuo.net/login/"

import base64
import Cookie
import email.utils
import hashlib
import hmac
import logging
import os.path
import time
import urllib
from django.utils import simplejson
from django.db.models import Q

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)
import logging

from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response,redirect
from course.models import *
from sutuo.models import *
from form import *

def coursePage(request,courseID):
    '''check login'''
    if('RRid' in request.session.keys()):
        notlogged=False
        user = User.objects.get(RRid=request.session['RRid'])
    else:
        notlogged=True
    
    '''make teachers list'''
    course = Course.objects.get(courseID=courseID)
    cts= CourseTeacher.objects.filter(course=course)
    teachers = []
    for ct in cts:
        teachers += [{'name':ct.teacher.name,'recommend':ct.recommend}]
    teacher_num = str(len(teachers))
    
    '''make comment list'''
    comments = Comment.objects.filter(course=course)
    #print comments
    
    '''deal with post query'''
    if request.method == 'POST':
        '''deal with add a new comment'''
        if 'comment' in request.POST.keys():
            comment_content=request.POST['comment']
            
            '''check the content length'''
            empty = False
            if len(comment_content)==0:
                empty = True
                for i in range(0,int(request.POST['teacher_num'])):
                    if ('recommend'+str(i) in request.POST.keys() and request.POST['recommend'+str(i)]):
                        empty=False
            if empty:
                error="不要什么什么也不写吧～"
            else:
                '''save comment'''
                commentNew = Comment(course=course,comment=comment_content,user=user)
                commentNew.save()
                for i in range(0,int(request.POST['teacher_num'])):
                    if ('recommend'+str(i) in request.POST.keys() and request.POST['recommend'+str(i)]):
                        teacher_name = request.POST['teacher_name'+str(i)]
                        teacher=Teacher.objects.get(name=teacher_name)
                        ct = CourseTeacher.objects.get(course=course,teacher=teacher)
                        commentNew.teacher.add(teacher)
                        commentNew.course_teacher.add(ct)
                        ct.recommend +=1
                        ct.save()
                commentNew.save()
                return redirect('/'+courseID)
                
            '''deal with the vote'''
        elif 'teacher_name' in request.POST.keys():
            
            '''find teacher courseteacher'''
            if notlogged:
                error = '你还没有登录诶～'
            else:
                teacherName = request.POST['teacher_name']
                try:
                    teacher = Teacher.objects.get(name=teacherName)
                except Teacher.DoesNotExist:
                    raise Http404()
                try:
                    ct = CourseTeacher.objects.get(course=course,teacher=teacher)
                except CourseTeacher.DoesNotExist:
                    raise Http404()
                '''check if the user ranked it'''
                if len(Vote.objects.filter(user=user,course_teacher=ct))==0:
                    teaching_skill = int(request.POST['teaching_skill'])
                    grades_level = int(request.POST['grades_level'])
                    ct.teaching_skill = (ct.teaching_skill*ct.voteCnt+teaching_skill)//(ct.voteCnt+1)
                    ct.grades_level = (ct.grades_level*ct.voteCnt+grades_level)//(ct.voteCnt+1)
                    ct.voteCnt+=1
                    ct.total_score = ct.teaching_skill + ct.grades_level
                    ct.save()
                    voteNew = Vote(course=course,teacher=teacher,course_teacher=ct,user=user,teaching_skill=teaching_skill,grades_level=grades_level)
                    voteNew.save()
                    return redirect('/'+courseID)
                else:
                    '''make error info'''
                    error = "你已经打过分了~"
                
    return render_to_response('CoursePage.html',locals())
    
def votePage(request,courseID,teacherName):
    '''find the teacher and course'''
    try:
        course = Course.objects.get(courseID=courseID)
    except Course.DoesNotExist:
        raise Http404()
    try:
        teacher = Teacher.objects.get(name=teacherName)
    except Teacher.DoesNotExist:
        raise Http404()
    try:
        ct = CourseTeacher.objects.get(course=course,teacher=teacher)
    except CourseTeacher.DoesNotExist:
        raise Http404()
    '''show the vote page'''
    return render_to_response('VotePage.html',locals())
    


def homePage(request):
    '''check login'''
    if('RRid' in request.session.keys()):
        user = User.objects.get(RRid=request.session['RRid'])
        
    comments = Comment.objects.order_by("-datetime")[0:10]
        
    if ('query' in request.GET.keys()):
        query = request.GET['query']
        items = Course.objects.filter(name__contains=query)
        #print items
        return render_to_response('SearchResults.html',locals())
    else:
        #commentList=Comment.objects.order_by('-datetime')[0:10]
        form = SearchForm()
        return render_to_response('HomePage.html',locals())
        
def profilePage(request,RRid):
    '''check login'''
    if('RRid' in request.session.keys()):
        user = User.objects.get(RRid=request.session['RRid'])
    target_user = User.objects.get(RRid=RRid)
    comments=Comment.objects.filter(user=target_user)
    return render_to_response('ProfilePage.html',locals())
    

def loginPage(request):
    args = dict(client_id=RENREN_APP_API_KEY, redirect_uri=REDIRECT_URI)
    if('error' in request.GET.keys()):
        return request
    if('code' in request.GET.keys()):
        '''Obtain access token from Resouce Service'''
        verification_code = request.GET['code']
        # response_state = self.request.get("state")
        # logging.info("returning state is :" + response_state)
        args["client_secret"] = RENREN_APP_SECRET_KEY
        args["code"] = verification_code
        args["grant_type"] = "authorization_code"
        logging.info(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args))
        response = urllib.urlopen(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args)).read()
        logging.info(response)
        access_token = _parse_json(response)["access_token"]
        logging.info("obtained access_token is: " + access_token)
        
        '''Obtain session key from the Resource Service.'''
        session_key_request_args = {"oauth_token": access_token}
        response = urllib.urlopen(RENREN_SESSION_KEY_URI + "?" + urllib.urlencode(session_key_request_args)).read()
        logging.info("session_key service response: " + str(response))
        session_key = str(_parse_json(response)["renren_token"]["session_key"])
        logging.info("obtained session_key is: " + session_key)
        
        '''Requesting the Renren API Server obtain the user's base info.'''
        params = {"method": "users.getInfo", "fields": "name,tinyurl"}
        api_client = RenRenAPIClient(session_key, RENREN_APP_API_KEY, RENREN_APP_SECRET_KEY)
        response = api_client.request(params);
        
        if type(response) is list:
            response = response[0]
        
        user_id = response["uid"]#str(access_token).split("-")[1]
        name = response["name"]
        avatar = response["tinyurl"]
        
        try:
            user = User.objects.get(RRid=unicode(user_id))
            user.access_token=access_token
            user.name=unicode(name)
            user.avatar=unicode(avatar)
        except User.DoesNotExist:
            user = User(name=unicode(name), RRid=unicode(user_id),avatar=unicode(avatar),access_token=access_token)
            user.save()
        request.session['RRid']=user_id
        
        return redirect('/')
    else:
        args["response_type"] = "code"
        #args["scope"] = "publish_feed email status_update"
        #args["state"] = "1 23 abc&?|."
        return redirect(
            RENREN_AUTHORIZATION_URI + "?" +
            urllib.urlencode(args))

def APIdocPage(request):
    '''check login'''
    if('RRid' in request.session.keys()):
        user = User.objects.get(RRid=request.session['RRid'])
    return render_to_response('APIdocPage.html',locals())

def guestbookPage(request):
    '''check login'''
    if('RRid' in request.session.keys()):
        user = User.objects.get(RRid=request.session['RRid'])
    messageList = Message.objects.order_by('-datetime')[0:10]

    '''deal with post query'''
    if request.method == 'POST':
        '''deal with add a new comment'''
        if 'content' in request.POST.keys():
            message_content=request.POST['content']
            
            '''check the content length'''
            if len(message_content)==0:
                error="不要什么什么也不写吧～"
            elif len(message_content)>400:
                error="这个好像太长了。。。"
            else:
                '''save comment'''
                reciever = User.objects.get(id=1)
                messageNew = Message(content=message_content,sender=user,reciever=reciever)
                messageNew.save()
                return redirect('/guestbook')
    return render_to_response('GuestbookPage.html',locals())

def sutuoPage(request):
    if request.method == 'POST':
        try:
            query = request.POST['name_or_studentID']
        except KeyError:
            pass 
        else: 
            if query:
                sutuoItems = SutuoItem.objects.filter(name__contains=query) | SutuoItem.objects.filter(studentID=query)
                result = True
    return render_to_response('SutuoPage.html',locals())
    

'''API'''
def APIvote(request):
    '''check login'''
    if('RRid' in request.session.keys()):
        notlogged=False
        user = User.objects.get(RRid=request.session['RRid'])
    else:
        notlogged=True

    success = 0
    error = ''

    if notlogged:
        error = '未登录'
    else:
        try:
            '''find course, teacher, courseteacher'''
            courseID = request.REQUEST['courseID']
            course = Course.objects.get(courseID=courseID)
            teacherName = request.REQUEST['teacher_name']
            teacher = Teacher.objects.get(name=teacherName)
            ct = CourseTeacher.objects.get(course=course,teacher=teacher)
            '''check if the user ranked it'''
            if len(Vote.objects.filter(user=user,course_teacher=ct))==0:
                teaching_skill = int(request.REQUEST['teaching_skill'])
                grades_level = int(request.REQUEST['grades_level'])
                ct.teaching_skill = (ct.teaching_skill*ct.voteCnt+teaching_skill)//(ct.voteCnt+1)
                ct.grades_level = (ct.grades_level*ct.voteCnt+grades_level)//(ct.voteCnt+1)
                ct.voteCnt+=1
                ct.total_score = ct.teaching_skill + ct.grades_level
                ct.save()
                voteNew = Vote(course=course,teacher=teacher,course_teacher=ct,user=user,teaching_skill=teaching_skill,grades_level=grades_level)
                voteNew.save()
                success = 1
            else:
                '''make error info'''
                error = "重复打分"
        except Exception,e:
            error = '参数错误'
    return HttpResponse(simplejson.dumps({'success':success, 'error':error}))
    
def APImakeComment(request):
    '''check login'''
    if('RRid' in request.session.keys()):
        notlogged=False
        user = User.objects.get(RRid=request.session['RRid'])
    else:
        notlogged=True

    success = 0
    error = ''
    '''deal with add a new comment'''
    if not notlogged:
        try:
            comment_content=request.REQUEST['comment']

            '''check the content length'''
            empty = False
            if len(comment_content)==0:
                empty = True
                for i in range(0,int(request.REQUEST['teacher_num'])):
                    if ('recommend'+str(i) in request.REQUEST.keys() and request.REQUEST['recommend'+str(i)]):str
                    empty=False
            if empty:
                error="空内容"
            else:
                '''save comment'''
                courseID = request.REQUEST['courseID']
                course = Course.objects.get(courseID=courseID)
                commentNew = Comment(course=course,comment=comment_content,user=user)
                commentNew.save()
                if 'teacher_num' in request.REQUEST.keys():
                    for i in range(0,int(request.REQUEST['teacher_num'])):
                        if ('recommend'+str(i) in request.REQUEST.keys() and request.REQUEST['recommend'+str(i)]):
                            teacher_name = request.REQUEST['teacher_name'+str(i)]
                        teacher=Teacher.objects.get(name=teacher_name)
                        ct = CourseTeacher.objects.get(course=course,teacher=teacher)
                        commentNew.teacher.add(teacher)
                        commentNew.course_teacher.add(ct)
                        ct.recommend +=1
                        ct.save()
                commentNew.save()
                success = 1
        except Exception,e:
            error = '参数错误'
    else:
        error='未登录'
    return HttpResponse(simplejson.dumps({'success':success, 'error':error}))

def APIgetCourseTeacherScorePage(request):
    scoreDict = {}
    error = ''
    try:
        courseID = request.REQUEST['courseID']
        course = Course.objects.get(courseID=courseID)

        '''make teachers list'''
        course = Course.objects.get(courseID=courseID)
        cts= CourseTeacher.objects.filter(course=course)
        for ct in cts:
            scoreDict[ct.teacher.name] = {'teaching_skill':ct.teaching_skill, 'grades_level':ct.grades_level, 'total_score':ct.total_score}
    except Exception,e:
        error = '参数错误'
    result = {'scores':scoreDict, 'error':error}
    resultJson = simplejson.dumps(result)
    return HttpResponse(resultJson)


def APIgetCourseCommentPage(request):
    commentList = []
    error = ''
    try:
        courseID = request.REQUEST['courseID']
        course = Course.objects.get(courseID=courseID)

        '''make comments list'''
        comments = Comment.objects.filter(course=course)
        for comment in comments:
            commentList.append({'user_name':comment.user.name, 'comment':comment.comment, 'datetime':comment.datetime.isoformat()})
    except Exception, e:
        error = '参数错误'
    result = {'comment':commentList, 'error':error }
    resultJson = simplejson.dumps(result)
    return HttpResponse(resultJson)

'''dev_backdoor'''
def dev_login(request):
    request.session['RRid']='270383879'
    return redirect('/')
    
    
'''Tools'''

class RenRenAPIClient(object):
    def __init__(self, session_key = None, api_key = None, secret_key = None):
        self.session_key = session_key
        self.api_key = api_key
        self.secret_key = secret_key
    def request(self, params = None):
        """Fetches the given method's response returning from RenRen API.

        Send a POST request to the given method with the given params.
        """
        params["api_key"] = self.api_key
        params["call_id"] = str(int(time.time() * 1000))
        params["format"] = "json"
        params["session_key"] = self.session_key
        params["v"] = '1.0'
        sig = self.hash_params(params);
        params["sig"] = sig
        
        post_data = None if params is None else urllib.urlencode(params)
        
        #logging.info("request params are: " + str(post_data))
        
        file = urllib.urlopen(RENREN_API_SERVER, post_data)
        
        try:
            s = file.read()
            logging.info("api response is: " + s)
            response = _parse_json(s)
        finally:
            file.close()
        if type(response) is not list and response["error_code"]:
            logging.info(response["error_msg"])
            raise RenRenAPIError(response["error_code"], response["error_msg"])
        return response
    def hash_params(self, params = None):
        hasher = hashlib.md5("".join(["%s=%s" % (self.unicode_encode(x), self.unicode_encode(params[x])) for x in sorted(params.keys())]))
        hasher.update(self.secret_key)
        return hasher.hexdigest()
    def unicode_encode(self, str):
        """
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str
    
class RenRenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


def set_cookie(response, name, value, domain=None, path="/", expires=None):
    """Generates and signs a cookie for the give name/value"""
    logging.info("set cookie as " + name + ", value is: " + value)
    timestamp = str(int(time.time()))
    value = base64.b64encode(value)
    signature = cookie_signature(value, timestamp)
    cookie = Cookie.BaseCookie()
    cookie[name] = "|".join([value, timestamp, signature])
    cookie[name]["path"] = path
    if domain: cookie[name]["domain"] = domain
    if expires:
        cookie[name]["expires"] = email.utils.formatdate(
            expires, localtime=False, usegmt=True)
    response.headers._headers.append(("Set-Cookie", cookie.output()[12:]))


def parse_cookie(value):
    """Parses and verifies a cookie value from set_cookie"""
    if not value: return None
    parts = value.split("|")
    if len(parts) != 3: return None
    if cookie_signature(parts[0], parts[1]) != parts[2]:
        logging.warning("Invalid cookie signature %r", value)
        return None
    timestamp = int(parts[1])
    if timestamp < time.time() - 30 * 86400:
        logging.warning("Expired cookie %r", value)
        return None
    try:
        return base64.b64decode(parts[0]).strip()
    except:
        return None


def cookie_signature(*parts):
    """Generates a cookie signature.

    We use the renren app secret since it is different for every app (so
    people using this example don't accidentally all use the same secret).
    """
    hash = hmac.new(RENREN_APP_SECRET_KEY, digestmod=hashlib.sha1)
    for part in parts: hash.update(part)
    return hash.hexdigest()


'''old page'''
def classPage(request,courseID,teacher):
    '''check login'''
    if('RRid' in request.session.keys()):
        notlogged=False
        user = User.objects.get(RRid=request.session['RRid'])
    else:
        notlogged=True
        
    #判断是否存在该页面
    # try:
        # course = Course.objects.get(courseID=courseID)
    # except Course.DoesNotExist:
        # raise Http404()
    # try:
        # teacher = Teacher.objects.get(name=teacher)
    # except Teacher.DoesNotExist:
        # raise Http404()
        
    # try:
        ct=CourseTeacher.objects.get(teacher__name=teacher, course__courseID=courseID)
        # return HttpResponse(course.name+teacher.name)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                commentNew = Comment(course_teacher=ct,teacher=ct.teacher,course=ct.course,name=cd['name'],comment=cd['comment'],stars=int(cd['rate']),pro=0,con=0,score=0)
                commentNew.save()
                
        commentList= Comment.objects.filter(course_teacher=ct).order_by('-datetime') #FIXME
        teacher = ct.teacher
        course = ct.course
        # print str(commentList)
        form = CommentForm()
        return render_to_response('ClassPage.html',locals())
            
    # except:
        raise Http404()
        
def hello(request):
    return HttpResponse("Hello world")
    
