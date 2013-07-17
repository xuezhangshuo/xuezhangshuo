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
import re
import json
from django.utils import simplejson
from django.db.models import Q

import logging

from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate, login
from course.models import *
from account.models import *
from sutuo.models import *
from form import *

from django.contrib import auth

def modify_course_description(request):
    user = request.user
    cid = request.REQUEST['cid']
    content = '<p>' + request.REQUEST['content'].replace('\n', "</p>\n<p>") + '</p>'
    course = Course.objects.get(courseID=cid)
    try:
        course_des_old = CourseDescription.objects.get(course=course, is_active=True)
        course_des_old.is_active = False
        course_des_new = CourseDescription(content=content, course=course)
        course_des_old.save()
        course_des_new.save()
        old_contributors = course_des_old.contributors.all()
        course_des_new.contributors = old_contributors
        if not user in old_contributors:
            course_des_new.contributors.add(user)
    except:
        course_des_new = CourseDescription(content=content, course=course)
        course_des_new.save()   
        course_des_new.contributors.add(user)
    course_des_new.save()
    response = {"content":content, 
                "contributors":[x.name+u"同学 " for x in course_des_new.contributors.all()]}
    return HttpResponse(json.dumps(response))

#FIXME: need to check whether vote repeatedly
def vote_course_teacher(request):
        course = Course.objects.get(courseID=request.REQUEST['courseID'])
        teacher = Teacher.objects.get(id=request.REQUEST['teacherID'])
        ct = CourseTeacher.objects.get(course=course, teacher=teacher)
        value = request.REQUEST['value']
        v = Vote(course_teacher=ct, user=request.user, value=value)
        v.save()
        if ct.rank_cnt != 0:
            diff =  float(value) - ct.rank
            ct.rank += diff / ct.rank_cnt
        else: 
            ct.rank = float(value)
        ct.rank_cnt += 1
        ct.save()
        return HttpResponse("success")


def coursePage(request,courseID):
    '''check login'''
    user = request.user
    
    '''make teachers list'''
    course = Course.objects.get(courseID=courseID)
    cts= CourseTeacher.objects.filter(course=course)
    try:
        courseDescription = CourseDescription.objects.get(course=course, is_active=True)
        cd_content = '<p>' + courseDescription.content.replace('\n', "</p>\n<p>") + '</p>'
    except:
        courseDescription = None
    teachers = []

    for ct in cts:
        teachers += [{'id':ct.teacher.id, 'name':ct.teacher.name,'rank':ct.rank,
         'comments':Comment.objects.filter(course_teacher=ct)}]
    teacher_Cnt = str(len(teachers))
    
    '''deal with post query'''
    if request.method == 'POST':
        '''deal with add a new comment'''
        if 'comment' in request.POST.keys() and "teacher" in request.POST.keys():
            comment_content=request.POST['comment']
            comment_teacher_name=request.POST['teacher']
            
            '''check the content length'''
            if len(comment_content)==0:
                error="不要什么什么也不写吧～"
            else:
                '''save comment'''
                comment_teacher = Teacher.objects.get(name=comment_teacher_name)
                comment_ct = CourseTeacher.objects.get(course=course,teacher=comment_teacher)
                commentNew = Comment(course_teacher=comment_ct,comment=comment_content,user=user)
                commentNew.save()
                return redirect('/'+courseID)

        # if 'vote' in request.POST.
            # '''deal with the vote'''
        # elif 'teacher_name' in request.POST.keys():
            
        #     '''find teacher courseteacher'''
        #     if notlogged:
        #         error = '你还没有登录诶～'
        #     else:
        #         teacherName = request.POST['teacher_name']
        #         try:
        #             teacher = Teacher.objects.get(name=teacherName)
        #         except Teacher.DoesNotExist:
        #             raise Http404()
        #         try:
        #             ct = CourseTeacher.objects.get(course=course,teacher=teacher)
        #         except CourseTeacher.DoesNotExist:
        #             raise Http404()
        #         '''check if the user ranked it'''
        #         if len(Vote.objects.filter(user=user,course_teacher=ct))==0:
        #             teaching_skill = int(request.POST['teaching_skill'])
        #             grades_level = int(request.POST['grades_level'])
        #             ct.teaching_skill = (ct.teaching_skill*ct.voteCnt+teaching_skill)//(ct.voteCnt+1)
        #             ct.grades_level = (ct.grades_level*ct.voteCnt+grades_level)//(ct.voteCnt+1)
        #             ct.voteCnt+=1
        #             ct.total_score = ct.teaching_skill + ct.grades_level
        #             ct.save()
        #             voteNew = Vote(course=course,teacher=teacher,course_teacher=ct,user=user,teaching_skill=teaching_skill,grades_level=grades_level)
        #             voteNew.save()
        #             return redirect('/'+courseID)
        #         else:
        #             '''make error info'''
        #             error = "你已经打过分了~"
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

RRid_pattern = re.compile(r"/(\d{8,14})/?")

def profilePage(request,id):
    '''check login'''
    user = request.user
    if id == "self":
        setting = True
        id = user.id
        settingForm = SettingForm({"name":user.name, 
                                  "gender":user.gender, 
                                  "email":user.email, 
                                  "RRid":"http://www.renren.com/%s/profile" % user.RRid})
    target_user = xzsUser.objects.get(id=id)
    comments=Comment.objects.filter(user=target_user)
    votes = Vote.objects.filter(user=target_user)
    tmp = list(votes) + list(comments)
    comments_and_votes = sorted(tmp,key=lambda x: x.datetime, reverse=True)
    
    if request.method == "POST":
        settingForm = SettingForm(request.POST)
        if settingForm.is_valid():
            cd = settingForm.cleaned_data
            user.name = cd["name"]
            user.gender = cd["gender"]
            try:
                user.RRid = RRid_pattern.search(cd["RRid"]).group(1)
            except:
                pass
            user.save()

    return render_to_response('ProfilePage.html',locals())

def changePasswordPage(request):
    user = request.user
    if request.method == "GET":
        return render_to_response("ChangePasswordPage.html",locals())
    if request.method == "POST":
        user = auth.authenticate(email=user.email, password=request.POST["old_password"])
        if user is not None:
            new_password = request.POST["new_password"]
            new_password_again = request.POST["new_password_again"]
            if (new_password == new_password_again):
                try:
                    user.set_password(new_password)
                    user.save()
                    success = "修改成功！"
                except:
                    error = "密码不符合规范"
            else:
                error = "密码不一致"
        else:
            error = "旧密码有误"
    return render_to_response("ChangePasswordPage.html",locals())


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
            user = authenticate(username=cd['email'], password=cd['password'])
            login(request, user)
            return redirect('/')
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

