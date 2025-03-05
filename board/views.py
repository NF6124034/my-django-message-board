from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import models

from django.core.mail import mail_admins

def message_list(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            
            # 🔔 寄信通知管理員
            mail_admins(
                subject='📢 有新留言',
                message=f'{request.user.username} 留言：「{message.message}」'
            )

            return redirect('/')
    else:
        form = MessageForm()

    query = request.GET.get('q')
    sort = request.GET.get('sort', 'newest')

    if query:
        messages_list = Message.objects.filter(message__icontains=query)
    else:
        messages_list = Message.objects.all()

    if sort == 'oldest':
        messages_list = messages_list.order_by('created_at')
    elif sort == 'likes':
        messages_list = messages_list.annotate(like_count=models.Count('likes')).order_by('-like_count')
    else:
        messages_list = messages_list.order_by('-created_at')

    paginator = Paginator(messages_list, 5)
    page_number = request.GET.get('page')
    messages = paginator.get_page(page_number)

    return render(request, 'board/message_list.html', {'form': form, 'messages': messages, 'query': query, 'sort': sort})




@login_required
def delete_message(request, id):
    message = get_object_or_404(Message, id=id)
    if message.user != request.user:
        return redirect('/')
    message.delete()
    return redirect('/')

@login_required
def edit_message(request, id):
    message = get_object_or_404(Message, id=id)
    if message.user != request.user:
        return redirect('/')
    if request.method == 'POST':
        message.name = request.POST.get('name')
        message.message = request.POST.get('message')
        message.save()
        return redirect('/')
    
    return render(request, 'board/edit_message.html', {'message': message})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 註冊完自動登入
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'board/register.html', {'form': form})

@login_required
def like_message(request, id):
    message = get_object_or_404(Message, id=id)
    if request.user in message.likes.all():
        message.likes.remove(request.user)  # 如果已經按讚，再按就取消讚
    else:
        message.likes.add(request.user)  # 如果沒按讚，就新增讚
    return HttpResponseRedirect(reverse('message_list'))


@login_required
def profile(request):
    my_messages = Message.objects.filter(user=request.user)
    liked_messages = request.user.liked_messages.all()
    return render(request, 'board/profile.html', {
        'my_messages': my_messages,
        'liked_messages': liked_messages,
    })