from django.http import HttpResponse
from django.shortcuts import render
from .models import Project, Parts, ProjectCategories, Comment
from .forms import Register
from django.contrib.auth import authenticate, login, logout
import json

def index(request):
    return render(request, 'hub/DIYHUB.html')


def loginAndRegister(request):
    if request.method == 'POST':
        if request.POST.get("email"):
            print("Register")
            form = Register(request.POST)
            if form.is_valid():
                form.save()
                print("Account Created")
                return HttpResponse("Registered")
            else:
                return HttpResponse("Registration Failed")
        else:
            print("Login")
            user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
            else:
                return HttpResponse("Registration Failed")
            return HttpResponse("logged in")

    else:
        return render(request, 'hub/login.html')

def logout(request):
    logout(request)
    return HttpResponse(True)


def profile(request):
    return render(request, 'hub/profile.html')


def createProject(request):
    if request.method == 'POST':
        url = request.POST.get("name").replace(" ", "-")
        imgData = request.POST.get('img').replace("data:image/jpeg;base64,", "")
        imgURL = url + ".png"
        print(imgURL)
        # with open(imgURL, "wb") as f:
        #     f.write(base64.b64decode(imgData))
        partIDs = []
        parts = request.POST.get("parts").split(",")
        print("parts: " + str(parts))
        for part in parts:
            partObj = None
            partName = part.split(" x ")[1]
            partName = partName.split(" (#")[0]
            try:
                partObj = Parts.objects.get(name__exact=partName)
            except Parts.DoesNotExist:
                partObj = None
                print("Does Not Exist")
            if partObj:
                partIDs.append(partObj.id)
        print("partIDs: "+ str(partIDs))
        form = Project()
        form.name = request.POST.get("name")
        form.desc = request.POST.get("desc")
        form.difficulty = request.POST.get("difficulty")
        form.url = url
        form.steps = str(request.POST.get("steps"))
        form.parts = str(request.POST.get("parts"))
        form.imgPath = str(imgURL)
        category = request.POST.get("category").split(" (#")[0]
        cat = None
        try:
            cat = ProjectCategories.objects.get(name__exact=category)
        except ProjectCategories.DoesNotExist:
            print("Category not found, using General instead")
            cat = ProjectCategories.objects.all().first()
        form.category = cat
        form.partIDs = partIDs
        form.save()
    return render(request, 'hub/createProject.html')


def project(request, slug):
    context = {"projectName": slug}
    # #get comments
    # thisProject = None #get project
    # comments = Comment.objects.get(project=thisProject)
    # comments = []
    # for comment in comments:
    #     comments.append({"user": comment.user.username, "body": comment.body})
    # context = {"projectName": slug, "comments": comments}
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
        form = Comment()
        #form.userID =
        form.body = request.POST.get("body")
        form.save()
        userID = None
        comment = {"user": userID,"body": request.POST.get("body")}
        return HttpResponse(comment)
