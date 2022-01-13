from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from blogs.models import comment,reader,article
from datetime import date

# Create your views here.


def index(request):

    blog_heads = []
    blog_data = article.objects.all()
    for article_row in blog_data:
        blog_heads.append((article_row.title, article_row.name))

    if request.user.is_authenticated:

        context = user_fetchcontextinator(request.user.username)
        context['blog_heads'] = blog_heads
        return render(request, "index.html", context = context)

    else:

        loggedin = False
        return render(request, "index.html", {"blog_heads" : blog_heads, "loggedin" : loggedin})


def user_fetchcontextinator(thename, get_desc = False):

    # getting users' rows from reader model
    user_data = reader.objects.all()

    context = {}

    # catching the user stats if request's name is matched with user row's name
    for user_row in user_data:
        if user_row.username == thename:
            context['level'] = user_row.level
            context['comments'] = user_row.no_of_comments
            context['saved'] = json2list(user_row.saved_articles)
            context['loggedin'] = True
            if get_desc:
                context['description'] = user_row.description
            context['edit_desc'] = False

    return context


def getblog(blogname, retrieve_content = True):
    blog_data = article.objects.all()
    for article_row in blog_data:
        if article_row.name == blogname :
            if retrieve_content:
                return article_row.content
            else:
                return article_row.title


def json2list(thejsonstring):
    # takes a json string, extracts values from it, evaluates it, returns them in the form of list

    """
    tbd- upload page for articles and a retrieval system
        - add a saved json in reader model, make comments' hash code using datetime and add them to 
        - add a hashcode entry in the model of both comment and article, so that associated comments can be loaded in the template
        - add reader created datetime, last login datetime, no of logins, no of saved, and profile photo url in reader model 
        - add upvotes and user's name in comments model
        - add an article id using datetime in model and use it to save to reader's saved json
        - make migrations
        - evaluate and update level accordingly every time the user logs in
        - add comments section, upvote button, save article button (if logged in) in the blog html
        - update user last login and add no_of_logins in reader object every time the user logs in or comments something
        - take photo from user, send it from template to view,
            compress it, upload it on vps as a request and take a photo url as a response
            , add the photo link to reader's object dp for the user, process it, and 
        - let the user upload an article if the level has reached writer
    """
    return []


def blog(request):
    # check if user is logged in, show the effect in the visibility of login / sign up button
    # give the username and level variable to template where it should be displayed with the logout button 
    # (it should be a log out rather than logged in if already logged in)
    #...

    if request.user.is_authenticated:
        loggedin = True
    else:
        loggedin = False

    blog_name = request.POST.get("blogname")
    blog_title = getblog(blog_name, retrieve_content = False)
    comment = request.POST.get("comment")
    blog_content = getblog(blog_name)
    if comment:
        messagestr = "Your comment has been posted"
        messages.add_message(request, messages.INFO, messagestr)
        # store the comment variable by model here

    # give a comment lists in the template
    # and somehow manage to return title from index template as well, so that view can recieve it and give it to blog's template
    # or, just get the corresponding title from database using a function
    # giving the blog name as well for save button's sake in the future
    return render(request, "blog.html", {"blog" : blog_content, "blog_title" : blog_title, "blog_name" : blog_name, "loggedin" : loggedin})


def log_in(request):
    # send the user to dashboard if already logged in
    # handle login post
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, "login.html", {"loggedin" : False})


def create_account(request):

    # send the user to dashboard if they are logged in..

    if request.method == "POST":
        recieved_name = request.POST.get('name')
        recieved_email = request.POST.get('email')
        user = User.objects.create_user(recieved_name, recieved_email, request.POST.get('password'))
        user.save()
        new_reader_obj = reader(username = recieved_name, email_address = recieved_email)
        new_reader_obj.save()
        messagestr = "The account has been created, please proceed to log in section by clicking the button down below"
        messages.add_message(request, messages.INFO, messagestr)
        return render(request, "create_account.html", {"loggedin" : False})
    else:
        if request.user.is_authenticated:
            return redirect("/dashboard")
        elif request.user.is_anonymous:
            return render(request, "create_account.html", {"loggedin" : False})
        else:
            return redirect('/login')


def log_out(request):
    # log out the user and send them to home page with a message
    logout(request)
    messagestr = "You have been successfully logged out"
    messages.add_message(request, messages.INFO, messagestr)
    return render(request, "log_out.html")


def contact(request):
    # give the contact and about info here with a feedback section
    return render(request, "contact.html")


def dashboard(request):

    # return the user to login screen if they are anonymous or show them their stats if they are found in reader model

    if request.method == "POST" and request.POST.get("edit_desc") == "False":
        recieved_name = request.POST.get('name')
        # will check if this auth object even exists or not
        user = authenticate(request, username = recieved_name, password = request.POST.get('password'))

        if user is not None:
            login(request, user)
            context = user_fetchcontextinator(recieved_name, get_desc = True)
            return render(request, "dashboard.html", context = context)
        else:
            # user doesn't exist, send a message and reload the login page
            messagestr = "Your attempt to login has failed, please try again"
            messages.add_message(request, messages.INFO, messagestr)
            return redirect('/login')

    else:

        # this block executes when user randomly types in dashboard in url
        if request.user.is_authenticated:
            context = user_fetchcontextinator(request.user.username, get_desc = True)

            # the case when user has clicked edit description, ie, True value of edit_desc
            if request.method == "POST" and request.POST.get("edit_desc") == "True":
                context['edit_desc'] = True
            elif request.method == "POST" and request.POST.get("edit_desc") == "new":
                new_desc = request.POST.get("desc")
                reader.objects.update_or_create(username = request.user.username, defaults={"description" : new_desc})

            return render(request, "dashboard.html", context = context)
        elif request.user.is_anonymous:
            return redirect("/create-account")
        else:
            return redirect('/login')
