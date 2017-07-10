from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from blog.models import Article,Comment
from django.contrib.auth import authenticate,login,logout
from blog.forms import SignupForm , SigninForm , BlogForm ,CommentForm
from django.contrib.auth import get_user_model
from django.core.paginator import  Paginator
import logging
# Create your views here.

def blog_view(request,blog_number = '1'):#主页面{数字}
    blog = Article.objects.order_by("-modiify_date")
    page_number = int(blog_number)
    page = Paginator(blog,5)
    page = page.page(page_number)
    previous = page.has_previous()
    next = page.has_next()
    page_list = page.object_list
    return render(request, 'index.html', {'page':page,'page_list':page_list,'pre':previous,'next':next})

def page_view(request, page_number ='1'):#博客文章{数字}
    page_id = int(page_number)
    if request.method == 'POST':
        form = CommentForm(data=request.POST,auto_id='%s')
        if form.is_valid():
            content = form.cleaned_data['content']
            if not request.user.is_authenticated():
                 return redirect('/signin')
            username = request.user.username
            time = datetime.datetime.now()
            comment_n = Comment.objects.create(article_id=page_id, username=username, create_date=time, content=content)
            comment_n.save()
            return redirect('/page/'+str(page_id))
    else:
        try:
            blog = Article.objects.get(id=page_id)
            comment_e = Comment.objects.filter(article_id=page_id)
        except Article.DoesNotExist:
            return render(request , 'error,html',{})
        except Comment.DoesNotExist:
            comment_e = '无人评论'
        form =CommentForm()
    return render(request, 'page.html' , {'blog':blog,'comment':comment_e,'form':form})


def blog_index(request):
    return redirect('/1')

def signup(request):
    if request.method =='POST':
        form = SignupForm(data=request.POST,auto_id='%s')
        if form.is_valid():
            UserModel = get_user_model()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.create_user(username=username, password=password)
            user.save()
            auth = authenticate(username=username, password=password)
            login(request,auth)
            return redirect('/')
    else :
        form = SignupForm()
    return render(request,'signup.html', {'form':form})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(data=request.POST,auto_id='%s')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('/')
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def edit_num(request, page_id = '0'):
    if not request.user.is_authenticated():
        return redirect('/')
    page_id = int(page_id)
    if request.method == 'POST':
        form = BlogForm(data=request.POST,auto_id='%s')
        if form.is_valid():
            title = form.cleaned_data['title']
            summary = form.cleaned_data['summary']
            content =  form.cleaned_data['content']
            time = datetime.datetime.now()
            if not page_id == 0:
                Article.objects.filter(id=page_id).update(title=title, summary = summary ,content = content,modiify_date=time ,is_show =True )
            else:
                article=Article.objects.create(title=title, summary = summary ,content = content,create_date=time,modiify_date=time ,is_show =True )
                article.save()
            return redirect('/')
    else:
        if not page_id == 0:
            blog = Article.objects.get(id=page_id)
            data={'title':blog.title,'summary':blog.summary,'content':blog.content}
            form = BlogForm(data=data)
        else:
            form = BlogForm()
    return render(request,'edit.html',{'form':form,'p_id':page_id})


def edit(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method  == 'POST' :
        form = BlogForm(data=request.POST , auto_id='%s')
        if form.is_valid():
            title = form.cleaned_data['title']
            summary = form.cleaned_data['summary']
            content =  form.cleaned_data['content']
            time = datetime.datetime.now()
            article=Article.objects.create(title=title, summary = summary ,content = content,create_date=time,modiify_date=time ,is_show =True )
            article.save()
            return redirect('/')
    else:
        form = BlogForm()
    return render(request,'edit.html',{'form':form})

def delete(request,page_id):
    page_id = int(page_id)
    Article.objects.filter(id=page_id).delete()
    return redirect('/')
