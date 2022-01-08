from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


blog_titles = ["OS Review", "Bias", "Chernobyl"]


# make a model and get the blog from it in the future
# put a list of lines in the context and traverse through it
getblog = dict(zip(blog_titles,
["""
Windows bad
Linux good

    - written by Aryan Sidhwani at 23:00 ist delhi
""",
"""
I have no bias

    - written by a biased Aryan Sidhwani at 23:00 ist, New Delhi
""",
"""
Boom

    - written by Aryan Sidhwani at 23:00 IST, New Delhi
"""
]
))

def index(request):
    return render(request, "index.html", {"blog_titles" : blog_titles})


def blog(request):
    # check if user is logged in, show the effect in the visibility of login / sign up button
    # give the username and level variable to template where it should be displayed with the logout button 
    # (it should be a log out rather than logged in if already logged in)
    #...


    blog_chosen = request.POST.get("blogname")
    comment = request.POST.get("comment")
    blog_content = getblog[blog_chosen]
    if comment:
        messagestr = "Your comment has been posted"
        # store the comment variable by model here

    # give a comment lists in the template
    return render(request, "blog.html", {"blog" : blog_content, "blog_title" : blog_chosen})


def login(request):
    # send the user to dashboard if already logged in
    return render(request, "login.html")


def create_account(request):
    # kick the user to dashboard if they are logged in..
    return render(request, "create_account.html")


def log_out(request):
    # log out the user and send them to home page with a message
    return render(request, "log_out.html")


def contact(request):
    # give the contact and about info here with a feedback section
    return render(request, "contact.html")


def dashboard(request):
    # return the user to login screen if they are anonymous or show them their stats if they are found in reader model
    return render(request, "dashboard.html")