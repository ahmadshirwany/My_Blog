from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import commentsform, NewUserForm
from .models import Post
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .serializers import PostSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from os import getenv
import smtplib
import ssl
from email.message import EmailMessage


# Create your views here.
class PostLanguageViewSet(APIView):

    def get(self, request):
        Posts = Post.objects.all()
        post_serializer = PostSerializer(Posts, many=True)
        return Response(post_serializer.data)


class UserViewSet(APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)
    # serializer_class = PostSerializer
    # queryset = Post.objects.all()[0]


def get_date(posts):
    return posts['date']


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("starting-page")


# def starting_page (request):
#  lates_posts= Post.objects.all().order_by('-Date')[:3]
#  return render(request,"blog/index.html",{ "posts":lates_posts})
# all_posts= Post.objects.all()
class send_email(View):
    def post(self, request):
        if request.method == 'POST':
            try:
                name = request.POST.get('name')
                email = request.POST.get('email')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                sender_email = getenv("sender_email")
                password = getenv('email_pasword')
                receiver_email = getenv("receiver_email")
                subject = "   ".join([subject, name, email])
                em = EmailMessage()
                em['From'] = sender_email
                em['To'] = receiver_email
                em['Subject'] = subject
                em.set_content(message)
                con = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', '465', context=con) as smtp:
                    try:
                        smtp.login(sender_email, password)
                        smtp.sendmail(sender_email, receiver_email, em.as_string())
                    except Exception as e:
                        print(e)
                    finally:
                        smtp.quit()
            except Exception as e:
                # Print any error messages to stdout
                print(e)

                # try:
            #     send_mail(
            #         subject+" "+name,
            #         message,
            #         email,
            #         ['shirwanupwork@gmail.com'],
            #         fail_silently=False,
            #     )
            # except:
            #     return redirect("starting-page")
            messages.success(request, 'Email sent successfully!')
            return redirect("starting-page")


class starting_page(View):
    template_name = "blog/index.html"
    model = Post
    ordering = {"-Date"}
    context_object_name = "posts"

    def get(self, request):
        Posts = Post.objects.all().order_by('post_id')
        context = {
            "posts": Posts
        }
        if request.user.is_authenticated:
            context['user_status'] = True
            context['user'] = request.user
        else:
            context['user_status'] = False
        return render(request=request, template_name="blog/index.html",
                      context=context)

    def post(self, request):
        if request.user.is_authenticated:
            Posts = Post.objects.all().order_by('post_id')
            user_status = True
            context = {
                "posts": Posts,
                "user": request.user,
                "user_status": user_status
            }
            return render(request=request, template_name="blog/index.html", context=context)
        else:
            Posts = Post.objects.all().order_by('post_id')
            user_status = False
            context = {
                "posts": Posts,
                "user_status": user_status
            }
            messages.error(request, "Invalid username or password.")
            return render(request=request, template_name="blog/login-page.html", context=context)


class Posts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = {"-Date"}
    context_object_name = "all_posts"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['all_posts'] = Post.objects.all()
        request = self.request
        if request.user.is_authenticated:
            context['user_status'] = True
            context['user'] = request.user.username
        else:
            context['user_status'] = False
        return context


# def Posts (request):
#  return render(request,"blog/all-posts.html",{"all_posts":all_posts})

# def post_detail(request,slug):
#  # identified_post = next(post for post in all_posts if post['slug'] == slug)
#  identified_post = Post.objects.get(slug=slug)
#  return render(request,'blog/post-detail.html',{"post": identified_post,"post_tags":identified_post.tag.all()})
class Login_view(View):
    model = User
    template_name = 'blog/registration.html'

    def get(self, request):
        context = {
            "form": AuthenticationForm(),
        }
        return render(request, 'blog/login-page.html', context)

    def post(self, request):
        print("enter")
        if request.method == "POST":
            print('its a post request')
        form = AuthenticationForm(data=request.POST)
        print(form.errors)
        print(str(request.POST))
        if form.is_valid():
            print('valig login')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('login')
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("starting-page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print('not valid login')
            messages.error(request, "Invalid username or password.")
        context = {
            "form": AuthenticationForm(),
        }
        return render(request, 'blog/login-page.html', context)


class Signup_view(View):
    model = User
    template_name = 'blog/registration.html'

    def get(self, request):
        context = {
            "form": NewUserForm(),
        }
        return render(request, 'blog/registration.html', context)

    def post(self, request):
        form_submit = NewUserForm(request.POST)
        print(form_submit.errors)
        if form_submit.is_valid():
            newuser = form_submit.save()
            newuser.save()
            login(request, newuser)
            print("successful")
            messages.success(request, "Registration successful.")
            return redirect("starting-page")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        print("unsuccessful")
        return render(request=request, template_name="blog/registration.html", context={"form": form_submit})


class post_detail(View):
    template_name = 'blog/post-detail.html'
    model = Post

    def is_stored_post(self, request, post_id):
        stored_post = request.session.get("stored_posts")
        if stored_post is not None:
            is_save_for_later = post_id in stored_post
        else:
            is_save_for_later = False
        return is_save_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "post_tag": post.tag.all(),
            "comments": post.comments.all().order_by("-id"),
            "save_for_later": self.is_stored_post(request, post.id)
        }
        if request.user.is_authenticated:
            context['user_status'] = True
            context['user'] = request.user
            form = commentsform(initial={'username': request.user.username, 'user_email': request.user.email})
            form.fields['username'].widget.attrs['readonly'] = True
            form.fields['user_email'].widget.attrs['readonly'] = True
            context['comments_form'] = form
        else:
            context['user_status'] = False
            context['comments_form'] = commentsform()
        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = commentsform(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        context = {
            "post": post,
            "post_tag": post.tag.all(),
            "comments_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "save_for_later": self.is_stored_post(request, post.id)
        }
        if request.user.is_authenticated:
            context['user_status'] = True
            context['user'] = request.user
        else:
            context['user_status'] = False
        return render(request, 'blog/post-detail.html', context)


class readlater_view(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            post = Post.objects.filter(id__in=stored_posts)
            context["posts"] = post
            context["has_posts"] = True
        return render(request, "blog/stored-post.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
