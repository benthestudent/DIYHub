from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Project, Parts, ProjectCategories, Comment, Upvote, User, PartCategories
from .forms import Register
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as lgout
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import json
import base64
import os
import operator


def index(request):
    page = "search"
    projects = Project.objects.all()
    projectsArray = []
    account = request.user.username if request.user.is_authenticated else None
    if projects:
        for project in projects:
            projectsArray.append(
                {"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url})
    categoryArray = []
    categories = PartCategories.objects.all()
    if categories:
        for category in categories:
            partsArray = []
            parts = Parts.objects.filter(category=category)
            if parts:
                for part in parts:
                    partsArray.append({"name": part.name, "url": part.url})
            categoryArray.append({"name": category.name, "parts": partsArray})
    context = {"projects": projectsArray, "categories": categoryArray, "account": account, "page": page}
    return render(request, 'hub/DIYHUB.html', context)


def loginAndRegister(request, slug="login"):
    context = {}
    if request.method == 'POST':
        if request.POST.get("username"):
            print("Register")
            form = Register(request.POST)
            if form.is_valid():
                form.save()
                print("Account Created")
                user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
                if user is not None:
                    login(request, user)
                else:
                    context['message'] = "Login Failed"
                return redirect("/profile")
            else:
                context['message'] = "Registration Failed"
        else:
            print("Login")
            user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
            else:
                context['message'] = "Login Failed"
            return redirect("/profile")

    else:
        signup = True if slug == "signup" else None
        context = {"operation": signup}
        return render(request, 'hub/login.html', context)


def logout(request):
    lgout(request)
    return redirect("/")


def profile(request, username=None):
    account = request.user.username if request.user.is_authenticated else None
    user = request.user if request.user.is_authenticated else None
    user = User.objects.filter(username=username).first() if username is not None else user
    upvotedProjectsArray = []
    projectsArray = []
    message = ""
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            if request.POST.get("oldPassword") and request.POST.get("newPassword") and request.POST.get("newPassword1"):
                if check_password(request.POST.get("oldPassword"), user.password) and request.POST.get("newPassword") == request.POST.get("newPassword1"):
                    user.set_password(request.POST.get("newPassword"))
                    user.save()
                    message = "Password Saved"
                    print("Password Saved")
                else:
                    print("error saving new password")
            else:
                if request.POST.get("email"):
                    user.email = request.POST.get("email")
                if request.POST.get("fname"):
                    user.firstn = request.POST.get("fname")
                if request.POST.get("lname"):
                    user.lastn = request.POST.get("lname")
                if request.POST.get("phone"):
                    user.phone = request.POST.get("phone")
                if request.POST.get("bio"):
                    user.bio = request.POST.get("bio")
                user.save()
        userObj = {
            "email": user.email,
            "username": user.username,
            "firstn": user.firstn,
            "lastn": user.lastn,
            "phone": user.phone,
            "bio": user.bio
        }
        projects = Project.objects.filter(author=user)

        if projects:
            for project in projects:
                projectsArray.append({"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url})
        upvotes = Upvote.objects.filter(user=user, comment=None)

        if upvotes:
            for upvote in upvotes:
                project = upvote.project.all().first()
                upvotedProjectsArray.append(
                   {"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url})
    else:
        return redirect("/login")
    context = {"user": userObj, "projects": projectsArray, "upvotedProjects": upvotedProjectsArray, "message": message, "account": account}
    return render(request, 'hub/profile.html', context)


def createProject(request):
    page = "create"
    account = request.user.username if request.user.is_authenticated else None
    if request.method == 'POST' and request.user.is_authenticated:
        url = request.POST.get("name").replace(" ", "-")
        imgData = request.POST.get('img').replace("data:image/jpeg;base64,", "")
        projectPath = "hub/static/projects/" + url
        os.makedirs(projectPath)
        imgURL = projectPath + "/" + "project-image.png"
        print(imgURL)
        with open(imgURL, "wb") as f:
            f.write(base64.b64decode(imgData))
        partIDs = []
        parts = request.POST.get("parts").split(",")
        print("parts: " + str(parts))
        for part in parts:
            partObj = None
            partName = part.split(" x ")[1]
            try:
                partObj = Parts.objects.get(name__exact=partName)
            except Parts.DoesNotExist:
                partObj = None
                print("Does Not Exist")
            if partObj:
                partIDs.append(partObj.id)
        print("partIDs: " + str(partIDs))
        form = Project()
        form.name = request.POST.get("name")
        form.desc = request.POST.get("desc")
        form.difficulty = request.POST.get("difficulty")
        form.url = url
        form.steps = str(request.POST.get("steps"))
        form.parts = str(request.POST.get("parts"))
        form.imgPath = imgURL[imgURL.find("projects/"):]
        category = request.POST.get("category")
        cat = None
        try:
            cat = ProjectCategories.objects.get(name__exact=category)
        except ProjectCategories.DoesNotExist:
            print("Category not found, using General instead")
            cat = ProjectCategories.objects.all().first()
        form.category = cat
        form.partIDs = partIDs
        form.save()
        form.author.add(request.user)
        form.save()
    context = {"account": account, "page": page}
    return render(request, 'hub/createProject.html', context)


def project(request, slug):
    account = request.user.username if request.user.is_authenticated else None
    projectName = slug.replace("-", " ")
    project = None
    try:
        project = Project.objects.get(name__exact=projectName)
    except Project.DoesNotExist:
        return HttpResponse("No Project Found")
    if not project.author.all().first() == request.user:
        project.views += 1
        project.save()
    parts = project.parts.split(",")
    partsArray = []
    for part in parts:
        partsArray.append(part)
    category = project.category
    category = category.name

    context = {"projectName": projectName,
               "projectID": project.id,
               "desc": project.desc,
               "imgPath": project.imgPath,
               "difficulty": project.difficulty,
               "steps": project.steps,
               "parts": partsArray,
               "category": category,
               "upvotes": Upvote.objects.filter(project=project).count(),
               "views": project.views,
               "dateCreated": project.dateCreated.strftime('%D %I:%M %p'),
               "author": project.author.get().username,
               "account": account
               }
    # get comments
    commentArray = []
    comments = Comment.objects.filter(project=project)
    for comment in comments:
        upvoted = True if Upvote.objects.filter(comment=comment).first() else False
        replies = Comment.objects.filter(commentParent=comment)
        repliesArray = []
        for reply in replies:
            replyUpvoted = True if Upvote.objects.filter(comment=reply).first() else False
            repliesArray.append({"user": reply.user.username, "body": reply.body, "upvotes": reply.upvotes, "commentID": reply.id,
             "upvoted": replyUpvoted})
        commentArray.append(
            {"user": comment.user.username, "body": comment.body, "upvotes": comment.upvotes, "commentID": comment.id, "upvoted": upvoted, "replies": repliesArray})
    commentArray.sort(key=operator.itemgetter('upvotes'), reverse=True)
    context['comments'] = commentArray
    print(context['comments'])
    # check if the user has upvoted the post
    context['upvoted'] = False
    if request.user.is_authenticated:
        try:
            Upvote.objects.get(user=request.user, project=project)
            context['upvoted'] = True
        except Upvote.DoesNotExist:
            context['upvoted'] = False
        except Upvote.MultipleObjectsReturned:
            print("Error: multiple upvotes from user on one project")
            context['upvoted'] = True
    return render(request, 'hub/project.html', context)


def getParts(request):
    parts = []
    if "search" in request.GET:
        query = request.GET['search']
        print(query)
        if query:
            postresult = Parts.objects.filter(name__icontains=query)
            result = postresult
            for part in result:
                parts.append({"id": part.id, "name": part.name})
            print(parts)
        else:
            result = None
    return HttpResponse(json.dumps(parts))


def getCategories(request):
    categories = []
    if "search" in request.GET:
        query = request.GET['search']
        print(query)
        if query:
            postresult = ProjectCategories.objects.filter(name__icontains=query)
            result = postresult
            for part in result:
                categories.append({"id": part.id, "name": part.name})
            print(categories)
        else:
            result = None
    else:
        print("selected")
        result = ProjectCategories.objects.all()
        for part in result:
            categories.append({"id": part.id, "name": part.name})
        print(categories)
    return HttpResponse(json.dumps(categories))


def addComment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = Comment()
            form.userID = request.user.id
            form.body = request.POST.get("body")
            form.save()
            if request.POST.get("type") == "comment":
                try:
                    form.commentParent.add(Comment.objects.get(id=request.POST.get("elementID")))
                except Project.DoesNotExist:
                    print("Comment not found")
            elif request.POST.get("type") == "project":
                try:
                    form.project.add(Project.objects.get(id=request.POST.get("elementID")))
                except Project.DoesNotExist:
                    print("Project not found")
            form.save()
            userID = None
            comment = {"user": request.user.username, "body": request.POST.get("body"),
                       "staticPath": staticfiles_storage.url("projects/"), "commentID": form.id}
            return HttpResponse(json.dumps(comment))


def upvote(request):
    type = request.POST.get("type")
    elementID = request.POST.get("elementID")
    operation = request.POST.get("operation")
    if not request.user.is_authenticated:
        return redirect("/login")
    if operation == "downvote":
        element = Comment.objects.filter(id=elementID).first() if (type == "comment") else Project.objects.filter(id=elementID).first()
        print(element)
        vote = Upvote.objects.filter(user=request.user, comment=element).first() if (type == "comment") else Upvote.objects.filter(user=request.user, project=element).first()
        if vote:
            vote.delete()
            element.updateUpvotes()
            element.save()
        return HttpResponse("downvoted")
    upvote = Upvote()
    if type == "comment":
        comment = Comment.objects.filter(id=elementID).first()
        if not comment:
            return HttpResponse("No Such Comment")
        else:
            upvote.save()
            upvote.comment.add(comment.id)
            comment.updateUpvotes()
            comment.save()

    elif type == "project":
        project = Project.objects.filter(id=elementID).first()
        if not project:
            return HttpResponse("No Such Project")
        else:
            upvote.save()
            upvote.project.add(project.id)
            upvote.save()
            project.updateUpvotes()
            project.save()
    else:
        return HttpResponse("Not a Valid Type")
    upvote.user.add(request.user)
    upvote.save()
    print("upvoted")
    return HttpResponse("upvoted")

def filterProjects(request, filter="popular", num_of_results=25, page=1, category=None):
    startOfResults = (page - 1) * num_of_results
    projects = None
    category = ProjectCategories.objects.filter(name=category).first()
    projectsArray = []
    # return 25 projects based on number of upvotes
    if filter == "most_liked":
        if category:
            projects = Project.objects.order_by("-upvotes").filter(category=category)[startOfResults:startOfResults+num_of_results]
        else:
            projects = Project.objects.order_by("-upvotes")[startOfResults:startOfResults+num_of_results]

    if filter == "popular":
        if category:
            projects = Project.objects.order_by("-views").filter(category=category)[
                       startOfResults:startOfResults + num_of_results]
        else:
            projects = Project.objects.order_by("-views")[startOfResults:startOfResults + num_of_results]

    if projects:
        for project in projects:
            projectsArray.append(
                {"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url, "difficulty": project.difficulty})
    projects = {"projects": projectsArray}
    return HttpResponse(json.dumps(projects))

def contact(request):
    return render(request, 'hub/contact.html')

def about(request):
    return render(request, 'hub/about.html')

def getProjectsByParts(request):
    projectsArray = []
    parts = request.GET.get("parts")
    if parts:
        partQueryString = ""
        for part in parts:
            partQueryString += " " + part
        query = SearchQuery(partQueryString)
        vector = SearchVector('parts')
        projectResults = Project.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        if projectResults:
            for project in projectResults:
                projectsArray.append(
                    {"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url, "difficulty": project.difficulty})
        projects = {"projects": projectsArray}
    return HttpResponse(json.dumps(projects))