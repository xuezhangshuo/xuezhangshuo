#coding:utf8

# import base64
# import Cookie
# import email.utils
# import hashlib
# import hmac
# import logging
# import os.path
# import time
# import urllib
from django.utils import simplejson
from django.db.models import Q

import logging

from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response,redirect
from course.models import *
from account.models import *
from sutuo.models import *
from form import *

from django.contrib import auth

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
    user = request.user
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
    user = request.user
    target_user = User.objects.get(RRid=RRid)
    comments=Comment.objects.filter(user=target_user)
    return render_to_response('ProfilePage.html',locals())


def registerPage(request):
    if request.method == "GET":
        form = RegisterForm()
        return render_to_response('RegisterPage.html',{"form":form})
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = xzsUser.objects.create_user(cd['email'],cd['name'],cd['password'])
            user.save()
            return HttpResponse("success")
        else:
            return render_to_response('RegisterPage.html',{"form":form})
            







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

