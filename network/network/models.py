from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Posts(models.Model):
    class Meta:
        verbose_name_plural = "Posts"

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User")
    text = models.CharField(max_length=280, blank=True)
    date = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now=True)
    edited = models.CharField(max_length=3, default="no")

    def formatJSON(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "date": self.date,
            "timestamp": self.timestamp,
            "edited": self.edited
        }


    def __str__(self):
        return f"ID:{self.id}, User:{self.user}, Text: {self.text}, Date: {self.date}, Timestamp: {self.timestamp}, Edited: {self.edited}"

    def validText(self):
        return self.text != "" and self.hearted != "" and self.date != ""


class Likes(models.Model):
    class Meta:
        verbose_name_plural = "Likes"

    post = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True, related_name="Post")
    likes = models.IntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userliked")

    def formatJSON(self):
        return {
            "id": self.id,
            "postid": self.post.id,
            "timestamp": self.post.timestamp,
            "likes": self.likes,
            "userliked": self.user.username,
            "userlikedID": self.user.id
        }

    def __str__(self):
        return f"ID: {self.id}, Post-ID: {self.post.id}, Likes: {self.likes}, UserLiked: {self.user.username}"

    def validate(self):
        return self.likes >= 0




class Followers(models.Model):
    class Meta:
        verbose_name_plural = "Followers"

    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Follower")
    timestamp = models.DateTimeField(auto_now=True)


    def formatJSON(self):
        return {
            "id": self.id,
            "following": self.following.username,
            "followingID": self.following.id,
            "follower": self.follower.username,
            "followerID": self.follower.id,
            "timestamp": self.timestamp
        }


    def __str__(self):
        return f"{self.id}, {self.follower} --> {self.following}, Since: {self.timestamp}"

    def validate(self):
        return self.following != self.follower
