from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils import timezone

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from operator import itemgetter


from datetime import datetime
from .models import User, Posts, Likes, Followers


#
#---------------------------------------------------------------
#------------------  NO TOCAR ---------------------------------
#---------------------------------------------------------------
#

class postForm(forms.Form):
    """Formulario Post"""
    newPt = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "280", "placeholder": "Maximum 280 characters.", "id": "id_newPost"}), label="New Post")

class editForm(forms.Form):
    """Formulario Post"""
    newPt = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "280", "id": "editPost"}), label="Editing")


def index(request):
    if request.user.is_authenticated:
        posts = Posts.objects.all()
        likes = Likes.objects.all()

        postData = {"data": []}
        for item in posts:
            formatedPost = item.formatJSON()
            formatedPost.update({"likes": Likes.objects.filter(post_id=item.id).count()})
            iliked = Likes.objects.filter(post_id=item.id)
            iamLiked = iliked.filter(user_id=request.user.id)
            if len(iamLiked) == 1:
                formatedPost.update({"iamLiked": "yes"})
            elif len(iamLiked) == 0:
                formatedPost.update({"iamLiked": "no"})
            postData["data"].append(formatedPost)
        postData["data"] = postData["data"][::-1]

        paginas = Paginator(postData["data"], 10)
        numeroPagina = request.GET.get("page")
        pagObj = paginas.get_page(numeroPagina)

        return render(request, "network/index.html", {
            "data": pagObj,
            "formularioPost": postForm,
            "formularioEdit": editForm,
        })
    else:
        posts = Posts.objects.all()
        likes = Likes.objects.all()

        postData = {"data": []}
        for item in posts:
            formatedPost = item.formatJSON()
            formatedPost.update({"likes": Likes.objects.filter(post_id=item.id).count()})
            iliked = Likes.objects.filter(post_id=item.id)
            iamLiked = iliked.filter(user_id=request.user.id)
            if len(iamLiked) == 1:
                formatedPost.update({"iamLiked": "yes"})
            elif len(iamLiked) == 0:
                formatedPost.update({"iamLiked": "no"})
            postData["data"].append(formatedPost)
        postData["data"] = postData["data"][::-1]

        paginas = Paginator(postData["data"], 10)
        numeroPagina = request.GET.get("page")
        pagObj = paginas.get_page(numeroPagina)

        return render(request, "network/nologin.html", {
            "data": pagObj,
            "formularioPost": postForm,
            "formularioEdit": editForm,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def createpost(request):
    """Crea un post nuevo y unico"""
    if request.method == "POST":
        data = json.loads(request.body)

        if data["text"] == "":
            return JsonResponse({"error": "Post empty"}, status=400)
        else:
            postUser = Posts(
                user=request.user,
                text=data["text"],
                date=data["date"],
            )
            postUser.save()

            return JsonResponse({"message": "Posted"}, status=201)
    return JsonResponse({"message": "App Ok"}, status=200)

#
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#------------------  NO TOCAR ---------------------------------
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
################################################################

@login_required
def likedpost(request, idpost):
    """Maneja las operaciones de Like a los Posts, metodos: GET, POST, PUT."""
    if request.method == "GET":
        data = {"data": []}
        posts = Posts.objects.filter(id=idpost).values_list("id", flat=True)
        likes = Likes.objects.filter(post_id=idpost)
        IlikeThat = likes.filter(user_id=request.user.id)

        if len(IlikeThat) == 1:
            data["data"].append("yes")
        else:
            data["data"].append("no")
        return JsonResponse(data)

    elif request.method == "POST":
        data = json.loads(request.body)

        likes = Likes(
            post=Posts.objects.get(id=data["idPost"]),
            likes=data["ilike"],
            user=User.objects.get(id=request.user.id)
        )
        likes.save()
        return JsonResponse({"message": "Liked post, successfully"}, status=201)

    elif request.method == "PUT":
        dataPut = json.loads(request.body)
        liked = Likes.objects.filter(post_id=dataPut["postid"])
        userliked = liked.filter(user=request.user.id)
        userliked.delete()
        return JsonResponse({"message": "operation successfully, like"}, status=201)
    return JsonResponse({"message": "ok APp"}, status=200)


@login_required
def userview(request, username):
    dataUserPosts = {"data": []}
    iFollowYou = ""
    userid = User.objects.filter(username=username).values_list("id", flat=True)[0]
    postsUser = Posts.objects.filter(user=userid)
    likesPost = Likes.objects.all()

    follow = Followers.objects.filter(follower_id=request.user.id)
    ifollow = follow.filter(following=userid)

    if len(ifollow) == 0:
        iFollowYou = "no"
    if len(ifollow) == 1:
        iFollowYou = "yes"

    for item in postsUser:
        formateditem = item.formatJSON()

        iliked = Likes.objects.filter(post_id=item.id)
        iamLiked = iliked.filter(user_id=request.user.id)
        if len(iamLiked) == 1:
            formateditem.update({"iamLiked": "yes"})
        elif len(iamLiked) == 0:
            formateditem.update({"iamLiked": "no"})

        formateditem.update({"likes": Likes.objects.filter(post_id=item.id).count()})
        dataUserPosts["data"].append(formateditem)

    dataUserPosts["data"] = dataUserPosts["data"][::-1]

    paginas = Paginator(dataUserPosts["data"], 10)
    numPaginator = request.GET.get("page")
    pagObject = paginas.get_page(numPaginator)

    return render(request, "network/userview.html", {
        "ifollow": iFollowYou,
        "username": username,
        "ItemContent": pagObject
    })


@login_required
def posts(request):
    posts = Posts.objects.filter(user=request.user.id)
    likes = Likes.objects.all()

    getDataUser = {"data": []}

    for item in posts:
        formatItem = item.formatJSON()
        formatItem.update({"likes": Likes.objects.filter(post_id=item.id).count()})
        getDataUser["data"].append(formatItem)

    getDataUser["data"] = getDataUser["data"][::-1]

    paginas = Paginator(getDataUser["data"], 10)
    numeroPagina = request.GET.get("page")
    pagObjUser = paginas.get_page(numeroPagina)

    return render(request, "network/user.html", {
        "formularioEdit": editForm,
        "dataUser": pagObjUser
    })


@login_required
def following(request):
    dataFollow = {"data": []}

    ifollow = Followers.objects.filter(follower=request.user.id)

    for item in ifollow:
        itemformat = item.formatJSON()
        postFollowing = Posts.objects.filter(user_id=itemformat["followingID"])
        for itm in postFollowing:
            itemFormatedJSON = itm.formatJSON()
            totalLikes = Likes.objects.filter(post_id=itm.formatJSON()["id"]).count()
            ilikeThat = Likes.objects.filter(post_id=itm.formatJSON()["id"]).filter(user=request.user.id).count()
            itemFormatedJSON.update({"likes": totalLikes})
            if ilikeThat == 0:
                itemFormatedJSON.update({"iliked": "no"})
            elif ilikeThat == 1:
                itemFormatedJSON.update({"iliked": "yes"})
            dataFollow["data"].append(itemFormatedJSON)

    paginas = Paginator(dataFollow["data"], 10)
    numeroPagina = request.GET.get("page")
    pagFollow = paginas.get_page(numeroPagina)

    return render(request, "network/following.html", {
        "dataFollow": pagFollow
    })


def postedit(request, idpost):
    if request.method == "GET":
        postsPUT = Posts.objects.get(id=idpost)
        return JsonResponse({"postText": postsPUT.text})

    elif request.method == "PUT":
        data = json.loads(request.body)
        updatePost = Posts.objects.filter(id=idpost)
        updatePost.update(text=data["data"])
        updatePost.update(edited="yes")

        return JsonResponse({"message": "Edit Post -- PUT -- App Ok"}, status=200)

def createFollowing(request, following):
    if request.method == "GET":
        dataGet = {"ifollow": ""}

        followingUSer = Followers.objects.filter(following=User.objects.get(username=following))
        ifollow = followingUSer.filter(follower_id=request.user.id)

        if len(ifollow) == 0:
            dataGet["ifollow"] = "no"
        elif len(ifollow) == 1:
            dataGet["ifollow"] = "yes"

        return JsonResponse(dataGet)

    elif request.method == "POST":
        data = json.loads(request.body)

        followers = Followers(
            following=User.objects.get(username=data["userToFollow"]),
            follower=User.objects.get(pk=request.user.id)
        )
        followers.save()
        return JsonResponse({"message":"Following create"}, status=201)

    elif request.method == "PUT":
        dataPut = json.loads(request.body)

        followers = Followers.objects.filter(following=User.objects.get(username=dataPut["userFollowing"]))
        ifollowing = followers.filter(follower_id=request.user.id)
        ifollowing.delete()

        return JsonResponse({"message": "Deleted Following"}, status=201)
