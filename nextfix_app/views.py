from django.shortcuts import render , redirect
from . import models
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request,'index.html')


def shows_page(request):
    if 'user_id' in request.session:
        context = {
            'user': models.get_user_by_id(request.session['user_id']),
            'shows': models.Show.objects
        }
        return render(request,'shows_page.html',context)
    return redirect('/')


def registration_form(request):
    if request.method == 'POST':
        # validation form
        register_error = models.User.objects.basic_validator_register(request.POST)
        if len(register_error) > 0:
            for key, value in register_error.items():
                messages.error(request, value,extra_tags='registration_error')
            return redirect('/')
        # hash password using bcrypt 
        password = request.POST['form_password']
        # should save pw_hash in the database
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # handel the unique email error 
        try:
            models.create_user(request.POST,pw_hash)
        except:
            messages.error(request,'Do you already have an account?',extra_tags='registration_error')

    return redirect('/')

def login_form(request):
    if request.method == 'POST':
        login_error = models.User.objects.basic_validator_login(request.POST)
        if len(login_error) > 0:
            for key, value in login_error.items():
                messages.error(request, value,extra_tags='login_error')
            return redirect('/')
        # get the registered user from DB
        registered_user = models.get_user_by_email(request.POST)
        if registered_user:
            logged_user = registered_user[0]
            # check the password
            if bcrypt.checkpw(request.POST['registered_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect(shows_page)
            else:
                messages.error(request,'The User Email or Password is Incorrect',extra_tags='login_error')
                return redirect('/')
        else:    
            messages.error(request,'The User Email or Password is Incorrect',extra_tags='login_error')
        
            
    return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def add_show(request):
    if 'user_id' in request.session:
        return render(request,'add_new_show.html')
    return redirect('/')

def create_new_show(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            new_show_error = models.Show.objects.basic_validator_show(request.POST)
            if len(new_show_error) > 0:
                for key, value in new_show_error.items():
                    messages.error(request, value,extra_tags='show_error')
            show = models.get_show_by_title(request.POST)
            print(show)
            if show:
                messages.error(request,'Show is Already Recommend',extra_tags='show_error')
                return redirect(add_show)
            models.create_show(request.POST,request.session['user_id'])
    return redirect(shows_page)

def delete_show(request,show_id):
    if 'user_id' in request.session:
        models.delete_show(show_id)
        return redirect(shows_page)
    return redirect('/')

def edit_show(request,show_id):
    if 'user_id' in request.session:
        context = {
            'show':models.get_show_by_id(show_id)
        }
        return render(request,'edit_show.html',context)
    return redirect('/')

def post_edit_show(request,show_id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            edit_show_error = models.Show.objects.basic_validator_show(request.POST)
            if len(edit_show_error) > 0:
                for key, value in edit_show_error.items():
                    messages.error(request, value,extra_tags='edit_show_error')
            if models.check_show_title_unique(request.POST,show_id):
                messages.error(request,'Show is Already Recommend',extra_tags='edit_show_error')
                return redirect('/shows/edit/'+str(show_id))
            return redirect(shows_page)
    return redirect('/')

def show_details(request,show_id):
    if 'user_id' in request.session:
        context = {
            'show':models.get_show_by_id(show_id),
            'comments': models.Comment.objects
        }
    return render(request,'show_details.html',context)

def add_show_comment(request):
    if 'user_id' in request.session:
        show_id = request.POST['show_id']
        
        models.create_show_comment(request.POST,request.session['user_id'])
        return redirect('/shows/'+show_id)
    return redirect('/')

def delete_show_comment(request,show_id,comment_id):
    if 'user_id' in request.session:
        models.delete_show_comment(comment_id)
        return redirect('/shows/'+str(show_id))
    return redirect('/')