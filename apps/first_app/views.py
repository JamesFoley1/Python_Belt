from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def index(request):
    request.session.clear()
    return render(request, 'first_app/index.html')

def quotes(request):
    context = {
        'quote' : Quotes.objects.all()
    }
    return render(request, 'first_app/quotes.html', context)

def user(request, id):
    context = {
        'user': Users.objects.get(id=id),
    }
    print(type(context['user'].quotes.all()))
    print(context['user'].quotes.all())
    return render(request, 'first_app/user.html', context)

def edit_user(request):
    context = {
        'user': Users.objects.get(id = request.session['user_id'])
    }
    return render(request, 'first_app/edit_user.html', context)

def register(request):
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['email'] = request.POST['email']
    request.session['password'] = request.POST['password']
    request.session['pw_confirm'] = request.POST['pw_confirm']
    if request.method == "POST":
        result = Users.objects.basic_validator(request.POST)
        if isinstance(result, dict):
            for tags, value in result.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/')
        else:
            request.session['isvalid'] = True
            request.session['user_id'] = result
            request.session['first_name'] = Users.objects.get(id = result).first_name
        return redirect('/quotes')

def login(request):
    if request.method == "POST":
        user = Users.objects.basic_validator2(request.POST)
        if 'invalid_email' in user or 'empty' in user:
            for tags, value in user.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/')
        else:
            request.session['isvalid'] = True

            request.session['user_id'] = user[0].id
            request.session['first_name'] = user[0].first_name
            return redirect('/quotes')

def add_quote(request):
    if request.method == "POST":
        my_id = request.session['user_id']
        new_quote = Users.objects.add_quote(request.POST, my_id)
        if 'author' in new_quote or 'quote' in new_quote:
            for tags, value in new_quote.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/quotes')
    return redirect('/quotes')

def like(request, id):
    like = Quotes.objects.get(id = id)
    liker = Users.objects.get(id = request.session['user_id'])
    print(liker.my_like)
    if liker.my_like == False:
        liker.my_like = True
        print(liker.my_like)
        like.likes += 1
        like.save()
        liker.save()
        return redirect('/quotes')
    elif liker.my_like == True:
        liker.my_like = False
        like.likes -= 1
        like.save()
        liker.save()
        return redirect('/quotes')
        
    

def edit(request, id):
    if request.method == 'POST':
        my_id = request.session['user_id']
        my_email = Users.objects.get(id=id).email
        edit_user = Users.objects.edit(request.POST, my_email)
        if 'valid' in edit_user:
            for tags, value in edit_user.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/user/edit')
        else:
            edit = Users.objects.get(id = id)
            edit.first_name = request.POST['first_name']
            edit.last_name = request.POST['last_name']
            edit.email = request.POST['email']
            edit.save()
        return redirect('/user/edit')

def destroy(request, id):
    delete = Quotes.objects.get(id = id).delete()
    return redirect('/quotes')