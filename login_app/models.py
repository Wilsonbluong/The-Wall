from django.db import models
import re
import bcrypt

# Create your models here.

class userManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # check first name min length
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        # check last name min length
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        # check if email input matches typical email patterns
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = "Invalid email address!"
        # check password min length
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # check if password matches 
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Password does not match!"
        return errors
    
    def log_validator(self, postData):
        print('*'*100)
        errors = {}
        user = User.objects.filter(email=postData['email']).first()
        print('user:', user)
        if user == None:
            errors['login']= "Invalid email or password"
        elif not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['login']= "Invalid email or password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
    
class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)