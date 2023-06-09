from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Post, Comment, FriendsList
from .forms import PostForm, CommentForm
from account.models import Account, Profile
from account.forms import (
    ProfilePicUpdateForm,
    UserUpdateForm,
    ProfileLocationForm,
    AboutForm,
    ExperienceForm,
    EducationForm,
    SkillForm,
)


@login_required
def home(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        post_form.instance.author = request.user
        comment_form = CommentForm(request.POST)
        comment_form.instance.author = request.user
        
        if request.POST.get('post_id', False) != False:
            post_id = request.POST.get('post_id', False)
            comment_form.instance.post = get_object_or_404(Post, id=post_id)
        
        if post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect(reverse("launch_weblog_home"))
        
        if comment_form.is_valid():
            comment_form.save()
            return redirect("launch_weblog_home")
        
    else:
        post_form = PostForm()
        comment_form = CommentForm()

    comments = Comment.objects.all().order_by('time')
    user = request.user

    try:
        friends_list = FriendsList.objects.get(friend_list_holder=user)
    except FriendsList.DoesNotExist:
        friends_list = FriendsList(friend_list_holder=user)
        friends_list.save()

    context = {
        'posts': Post.objects.all().order_by('-time'),
        'post_form': post_form,
        'comments': comments,
        'comment_form': comment_form,
        'profiles': Profile.objects.all().order_by('-time'),
        'friends_list': friends_list.friends.all(),
    }

    return render(request, 'weblog/HOME.html', context)


def base(request):
    return render(request, 'weblog/Base.html')


@login_required
def profile(request, email):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_pic_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        location_form = ProfileLocationForm(request.POST, instance=request.user.profile)
        about_form = AboutForm(request.POST, instance=request.user.profile)
        experience_form = ExperienceForm(request.POST, instance=request.user.profile)
        education_form = EducationForm(request.POST, instance=request.user.profile)
        skill_form = SkillForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and location_form.is_valid():
            user_form.save()
            location_form.save()
            return redirect('user-posts')

        if about_form.is_valid():
            about_form.save()
            return redirect('user-posts')

        if experience_form.is_valid():
            experience_form.save()
            return redirect('user-posts')

        if education_form.is_valid():
            education_form.save()
            return redirect('user-posts')

        if skill_form.is_valid():
            skill_form.save()
            return redirect('user-posts')

        if request.POST.get('user_id', False) != False:
            user_id = request.POST.get('user_id', False)
            user = request.user

            try:
                friends_list = FriendsList.objects.get(friend_list_holder=user)
            except FriendsList.DoesNotExist:
                friends_list = FriendsList(friend_list_holder=user)
                friends_list.save()

            friends_list.add_friend(user_id)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_pic_form = ProfilePicUpdateForm(instance=request.user.profile)
        location_form = ProfileLocationForm(instance=request.user.profile)
        about_form = AboutForm(instance=request.user.profile)
        experience_form = ExperienceForm(instance=request.user.profile)
        education_form = EducationForm(instance=request.user.profile)
        skill_form = SkillForm(instance=request.user.profile)

        user = request.user

        try:
            friends_list = FriendsList.objects.get(friend_list_holder=user)
        except FriendsList.DoesNotExist:
            friends_list = FriendsList(friend_list_holder=user)
            friends_list.save()

    user = get_object_or_404(Account, email=email)
    user_id = user.id

    context = {
        'user_form': user_form,
        'profile_pic_form': profile_pic_form,
        'location_form': location_form,
        'about_form': about_form,
        'experience_form': experience_form,
        'education_form': education_form,
        'skill_form': skill_form,
        'posts': Post.objects.filter(author=user).order_by('-time'),
        'author_profile': Post.objects.filter(author=user).first,
        'comments': Comment.objects.all().order_by('time'),
        'friends_connected': friends_list.is_connected(user_id),
        'friends_list': friends_list.friends.all(),
    }

    return render(request, 'weblog/profile.html', context)


@login_required
def news(request):
    return render(request, 'weblog/News.html')
