from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 4 or len(postData['first_name']) > 255:
            errors['first_name'] = "Your first name must be at least 3 characters"

        if len(postData['last_name']) < 4 or len(postData['last_name']) > 255:
            errors['last_name'] = "Your last name must be at least 3 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = "The email you entered is not valid."

        if len(postData['email']) < 9 or len(postData['email']) > 255:
            errors['email_length'] = "Email must be at least 8 characters long."

        elif Users.objects.filter(email = postData['email']):
            errors['email'] = "The email you entered has already been taken! Please log in."

        if len(postData['password']) < 9 or len(postData['password']) > 255:
            errors['password'] = "Password must be at least 8 characters long."
        
        elif len(postData['pw_confirm']) < 9 or len(postData['pw_confirm']) > 255:
            errors['pw_confirm'] = "Password must be at least 8 characters long."
        elif postData['password'] != postData['pw_confirm']:
            errors['password'] = "Your passwords do not match!"
        
        if len(errors):
            errors['valid'] = False
            return errors

        else:
            new_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            create_user =  Users.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = new_pw)
            new_user = create_user.id
            return new_user

    def basic_validator2(self, postData):
        errors = {}
        user = Users.objects.filter(email = postData['email2'])
        if len(user):
            if bcrypt.checkpw(postData['password2'].encode(), user[0].password.encode()):
                return user
            else:
                errors['invalid_email'] = "The email address or password you entered was not valid."
                return errors
        else:
            errors['empty'] = "Please enter a valid email address and password."
            return errors
        
    def add_quote(self, postData, my_id):
        errors = {}
        
        if len(postData['author']) <= 3:
            errors['author'] = "The authors name must be 3 characters or longer"
        if len(postData['quote']) <= 10:
            errors['quote'] = "Your quote must be at least 10 characters long"

        if 'quote' in errors or 'author' in errors:
            return errors

        else: 
            new_quote = Quotes.objects.create(author = postData['author'], content = postData['quote'], likes = 0, user = Users.objects.get(id = my_id))
            new_quote.save()
            return errors
    
    def edit(self, postData, my_email):
        errors = {}
        

        if len(postData['first_name']) < 4 or len(postData['first_name']) > 255:
            errors['first_name'] = "Your first name must be at least 3 characters"
            errors['valid'] = False

        if len(postData['last_name']) < 4 or len(postData['last_name']) > 255:
            errors['last_name'] = "Your last name must be at least 3 characters"
            errors['valid'] = False

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = "The email you entered is not valid."
            errors['valid'] = False

        elif len(postData['email']) < 9 or len(postData['email']) > 255:
            errors['email_length'] = "Email must be at least 8 characters long."
            errors['valid'] = False

        if my_email != postData['email']:
            if Users.objects.filter(email = postData['email']):
                errors['email'] = "The email you entered has already been taken! Please choose another."
                errors['valid'] = False

        if 'valid' in errors:
            return errors
        else:
            return {}

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    my_like = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quotes(models.Model):
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    likes = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Users, related_name="quotes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
