from django.db import models
import re
from datetime import  datetime
# Create your models here.
class UserManager(models.Manager):
    def basic_validator_register(self,postData):
        errors = {}

            # first name validation
        if len(postData['form_first_name']) < 2 :
            errors['first_name'] = 'First Name should be at lest 2 character'

            # last name validaion
        if len(postData['form_last_name']) < 2 :
            errors['last_name_alpha'] = 'Last name should be at least 2 character'

            # email Validation
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['form_email']):
            errors['email'] = 'Invalid email Address!'

            # password validation
        if  len(postData['form_password']) < 7:
            errors['password'] = 'Password should be more than 7 character'
        if not postData['form_password'] == postData['form_confirm_pw']:
            errors['confirm_password'] = 'Confirm Password not match Password'
        return errors
    
    def basic_validator_login(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['registered_email']):
            errors['email'] = 'Invalid Email Address!'
        return errors

class ShowManager(models.Manager):
    def basic_validator_show(self, postData):
        errors = {}
        if len(postData['title']) < 3 :
            errors["title"] = "Title should be at least 3 characters "
        if len(postData['network']) < 3:
            errors['network'] = "Network should be at least 3 characters "
        if len(postData['description']) < 3:
            errors['description'] = "Description should be at least 3 characters "

        # if len(postData['release_date']) == '': 
        #     errors['release_date'] = "Enter the Release date  "
        try:
            datetime_object = datetime.strptime(postData['release_date'], '%Y-%m-%d')
            if datetime.timestamp(datetime_object) >= datetime.timestamp(datetime.now()):
                errors['release_date'] = "Release date should be in the past "
        except:
            errors['release_date'] = "Enter the Release date  "
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=70 , unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Show(models.Model):
    title = models.CharField(max_length = 255)
    network = models.CharField(max_length = 255)
    release_date = models.DateField()
    comment = models.TextField()
    user = models.ForeignKey(User,related_name='shows',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    objects = ShowManager()

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User,related_name='user_comments',on_delete=models.CASCADE)
    show = models.ForeignKey(Show,related_name='show_comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

def create_user(postData,password):
    user_first_name = postData['form_first_name']
    user_last_name = postData['form_last_name']
    user_email = postData['form_email']
    user_password = password
    User.objects.create(first_name = user_first_name, last_name = user_last_name , email = user_email, password = user_password)

def get_user_by_email(postData):
    registered_user = User.objects.filter(email = postData['registered_email'])
    return registered_user
    
def get_user_by_id(user_id):
    user = User.objects.get(id = user_id)
    return user

def get_show_by_title(postData):
    show = Show.objects.filter(title = postData['title'])
    return show

def create_show(postData,user_id):
    show_title = postData['title']
    show_network = postData['network']
    show_release_date = postData['release_date']
    show_description = postData['description']
    show_created_by =get_user_by_id(user_id) 
    Show.objects.create(title = show_title,network = show_network,
                        release_date = show_release_date,
                        comment = show_description,
                        user = show_created_by)

def get_show_by_id(show_id):
    show = Show.objects.get(id = show_id)
    return show
    
def delete_show(show_id):
    show = Show.objects.get(id = show_id)
    show.delete()

def check_show_title_unique(postData,show_id):
    show = get_show_by_id(show_id)
    if show.title == postData['title']:
        return False
    return True

def create_show_comment(postData,user_id):
    user_comment = postData['comment']
    comment_by = get_user_by_id(user_id)
    show_comment = get_show_by_id(postData['show_id'])
    Comment.objects.create(comment = user_comment,user = comment_by,show = show_comment)

def delete_show_comment(comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

def update_show(postData,show_id):
    show = get_show_by_id(show_id)
    show_title = postData['title']
    show_network = postData['network']
    show_release_date = postData['release_date']
    show_description = postData['description']
    # update on database
    show.title = show_title
    show.network = show_network
    show.release_date = show_release_date
    show.comment = show_description
    show.save()
