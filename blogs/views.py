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
    blog_chosen = request.POST.get("blogname")
    blog_content = getblog[blog_chosen]
    return render(request, "blog.html", {"blog" : blog_content })

