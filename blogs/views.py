from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from blogs.models import comment,reader,article
from datetime import date
from time import time

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

    context = {}

    # getting users' rows from reader model
    user_row = reader.objects.get(username = thename)

    context['level'] = user_row.level
    context['comments'] = user_row.no_of_comments
    saved_list = eval(user_row.saved_articles)
    context['saved_article_dictitems'] = dict(zip(saved_list, list([article.objects.get(name = x).title for x in saved_list]) )).items()
    context['loggedin'] = True
    context['loggedout'] = False
    if get_desc:
        context['description'] = user_row.description
    context['edit_desc'] = False
    context['email'] = user_row.email_address

    return context


def getblog(blogname, retrieve_content = True):
    article_row = article.objects.get(name = blogname)
    if retrieve_content:
        contentlist = eval(article_row.content)
#        contentstr = ""
#        for myline in contentlist:
#            contentstr += myline
        return contentlist
    else:
        return article_row.title


def json2list(thejsonstring):
    # started off as a functional function, now is a dummy function

    """
    tbd- upload page for articles and a retrieval system
        - a footer in template
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
            compress it, upload it on cdn / bucket as a request and take a photo url as a response
            , add the photo link to reader's object dp for the user, process it, and 
        - let the user upload an article if the level has reached writer
        - a service for forgot password
    """

    pass


def blog(request):
    # check if user is logged in, show the effect in the visibility of login / sign up button
    # give the username and level variable to template where it should be displayed with the logout button 
    # (it should be a log out rather than logged in if already logged in)
    #...

    mydict = request.POST.dict()
    #print(mydict)
    # the above line put the values in a list for some reason

#    mydict = {}
#    for key in request.POST:
#        mydict[key] = request.POST[key]



    commentstr = mydict.get("comment")
    
    blog_name_and_title = mydict['blognameandtitle'].split(" ")
    """

    This was executed when the input was a radio form, and nothing was selected, but now its just by buttons
    and noe user can't click on a button if the article isn't selected because clicking the button itself marks  the input checked

    except KeyError:
        # this key can only not exist when the user types in this url randomly
        # or clicks the go to blog button without selection
        messages.error(request, 'Please select a blog before going to the blog!')
        return render(request, 'noselection.html')
    """
    blog_title = " ".join(blog_name_and_title[1:])
    blog_name = blog_name_and_title[0]
    
    if request.user.is_authenticated:
        loggedin = True
        blog_dne_savedlist = True
        blog_saved = False
        
        # get the reader's row and find if this blog is already saved
        myrow = reader.objects.get(username = request.user.username)
        recieved_saved_articles = eval(myrow.saved_articles)
        if blog_name in recieved_saved_articles:
            blog_saved = True
            blog_dne_savedlist = False
            # what we want is that if user hasn't saved the article, the save article form block shows
            # also, we don't want both the button and saved! remark if user isn't even authed up
    else:
        # no remark or button if no auth
        blog_dne_savedlist = True
        blog_saved = False
        loggedin = False
        

    if eval(mydict["saveit"]):
        # the case when user presses save the article button

        # picking the reader row and then editing it
        myrow = reader.objects.get(username = request.user.username)
        recieved_saved_articles = eval(myrow.saved_articles)
        recieved_saved_articles.append(blog_name)
        myrow.saved_articles = str(recieved_saved_articles)
        myrow.save()

        # drop a message that the article is saved
        messagestr = "The article has been saved"
        messages.add_message(request, messages.INFO, messagestr)

    comment_obj_list = list(comment.objects.filter(blogname = blog_name))

    # tbd - handle the scenario where user enters blog url randomly, put a if post: maybe
    #blog_title = getblog(blog_name, retrieve_content = False)
    # -- no need, I got it from context, both index and blog save templates, so, its before the condition
    blog_content = getblog(blog_name)
    if commentstr:
        messagestr = "Your comment has been posted"
        messages.add_message(request, messages.INFO, messagestr)
        # storing the comment variable by model here
        user_name = request.user.username
        if user_name == "":
            user_name = "Anonymous"
        new_comment_obj = comment(blogname = blog_name, author = user_name, comment_id = str(time()), content = commentstr)
        new_comment_obj.save()
        comment_obj_list.append(new_comment_obj)

    comment_dir_list = []
    for comment_obj in comment_obj_list:
        comment_dir_list.append(vars(comment_obj))

    # give a comment lists in the template
    # and somehow manage to return title from index template as well, so that view can recieve it and give it to blog's template
    # or, just get the corresponding title from database using a function
    # giving the blog name as well for save button's sake in the future
    return render(request, "blog.html", {
        "blog" : blog_content,
        "blog_title" : blog_title,
        "blog_name" : blog_name,
        "loggedin" : loggedin,
        "blog_dne_savedlist" : blog_dne_savedlist,
        "blog_saved" : blog_saved,
        "comments" : comment_dir_list
    })
    


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
    context = {}
    if request.user.is_authenticated:
        thename = request.user.username
        context = user_fetchcontextinator(thename)
        context['username'] = thename
    else:
        context['loggedin'] = False
        context['loggedout'] = True
        
    return render(request, "contact.html", context = context)


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
