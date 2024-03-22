from django.db import models
from django.contrib.auth.models import User


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    selected_plan = models.TextField()
    max_posts = models.IntegerField(default=10)
    premium_features = models.BooleanField(default=False)

# Subscription Model


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_post = models.IntegerField(default=5)

    def __str__(self):
        return self.name

# Blog Post Model


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='static/images/', blank=True, null=True)
    category = models.CharField(max_length=50)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# UserProfile Model


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_status = models.TextField()
    active_subscription = models.BooleanField(default=False)
    max_post = models.IntegerField(default=5)

    def __str__(self):
        return self.user.username
