from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Project, Parts, ProjectCategories, Comment, Upvote, User, PartCategories
from .forms import Register
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as lgout
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils import timezone
import rstr
import json
import base64
import os
import operator
import datetime
from urllib.parse import quote, unquote, quote_plus

def index(request):
    page = "search"
    projects = Project.objects.filter(published=1)
    projectsArray = []
    account = request.user.username if request.user.is_authenticated else None
    projectsArray = getProjectsFromQuery(projects)
    categoryArray = []
    categories = PartCategories.objects.all()
    if categories:
        for category in categories:
            if category.id != 0: # category 0 will be unset category, meaning part must be reviewed
                partsArray = []
                parts = Parts.objects.filter(category=category)
                if parts:
                    for part in parts:
                        partsArray.append({"name": part.name, "url": part.url})
                categoryArray.append({"name": category.name, "parts": partsArray})
    context = {"projects": projectsArray, "categories": categoryArray, "account": account, "page": page}
    return render(request, 'hub/DIYHUB.html', context)

def createPart(name, cat=1):
    part = Parts()
    part.name = name
    cat = PartCategories.objects.filter(id=cat).first()
    if cat:
        part.category = cat
    part.save()
    return part

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
                    context['message'] = {"text": "Login Failed", "color": "red"}
                return redirect("profile")
            else:
                context['message'] = {"text": "Registration Failed", "color": "red"}
        else:
            print("Login")
            user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                context['message'] = {"text": "Login Failed", "color": "red"}
        return render(request, 'hub/login.html', context)

    else:
        signup = True if slug == "signup" else None
        context = {"operation": signup}
        return render(request, 'hub/login.html', context)


def logout(request):
    lgout(request)
    return redirect("index")


def profile(request, username=None):
    account = request.user.username if request.user.is_authenticated else None
    user = request.user if request.user.is_authenticated else None
    user = User.objects.filter(username=username).first() if username is not None else user
    upvotedProjectsArray = []
    projectsArray = []
    message = {}
    user_by_name = User.objects.filter(username=username).first()
    if request.user.is_authenticated or user_by_name:
        if request.method == "POST" and not user_by_name:
            user = request.user
            if request.POST.get("oldPassword") and request.POST.get("newPassword") and request.POST.get("newPassword1"):
                if check_password(request.POST.get("oldPassword"), user.password) and request.POST.get("newPassword") == request.POST.get("newPassword1"):
                    user.set_password(request.POST.get("newPassword"))
                    user.save()
                    message = {"text": "Password Saved", "color": "green"}
                    print("Password Saved")
                else:
                    message = {"text": "Password Change Failed. Old Password is incorrect or new passwords do not match", "color": "red"}
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
        user = user_by_name if user_by_name else user
        userObj = {
            "email": user.email,
            "username": user.username,
            "firstn": user.firstn,
            "lastn": user.lastn,
            "phone": user.phone,
            "bio": user.bio
        }
        projects = Project.objects.filter(author=user).exclude(published=0)

        projectsArray = getProjectsFromQuery(projects)
        upvotes = Upvote.objects.filter(user=user, comment=None)

        if upvotes:
            for upvote in upvotes:
                project = upvote.project.all().first()
                upvotedProjectsArray.append(
                   {"name": project.name, "desc": project.desc, "imgPath": project.imgPath, "url": project.url})
    else:
        return redirect("loginAndRegister")
    context = {"user": userObj, "projects": projectsArray, "upvotedProjects": upvotedProjectsArray, "message": message, "account": account}
    if user_by_name:
        return render(request, 'hub/profilePage.html', context)
    return render(request, 'hub/profile.html', context)

@ensure_csrf_cookie
def createProject(request, projectID=0):
    if not request.user.is_authenticated:
        return redirect("loginAndRegister")
    page = "create"
    account = request.user.username if request.user.is_authenticated else None
    context = {"account": account, "page": page}
    if projectID and request.user.is_authenticated:
        project = Project.objects.filter(id=projectID, author=request.user).first()
        if project:
            # editing project
            parts = project.parts.split(",")
            partsArray = []
            for part in parts:
                part = part.split(" x ")
                if len(part) == 2:
                    partsArray.append({"quantity": part[0], "name": part[1]})
            steps = formatSteps(project.steps)
            context["project"] = {
                "name": project.name,
                "desc": project.desc,
                "difficulty": project.difficulty,
                "parts": partsArray,
                "steps": steps,
                "img": project.imgPath,
                "category": project.category.name,
                "published": project.published
            }
    if request.method == 'POST' and request.user.is_authenticated:
        published = request.POST.get("published")
        if published:
            name = request.POST.get("name")
            form = None
            projectID = request.POST.get("urlEnd") if request.POST.get("urlEnd") != "create" else None
            if projectID:
                form = Project.objects.filter(id=projectID).first()
            else:
                form = Project.objects.filter(name=name).first()
            print("id: {}, form: {}, urlEnd: {}".format(projectID, str(form), request.POST.get("urlEnd")))

            if not form:
                form = Project()
                form.save()
        name = request.POST.get("name")
        formattedName = name
        if name:
            formattedName = formattedName.replace("/", "-")
            formattedName = quote_plus(formattedName)
            formattedName = formattedName.replace("+", "_")
        imgData = request.POST.get('img')
        imgData = imgData.replace("data:image/jpeg;base64,", "") if imgData else imgData
        imgData = imgData.replace("data:image/png;base64,", "") if imgData else imgData
        imgURL = form.imgPath
        if not 'static/' in str(imgData)[0:10] and imgData: # if img has a / in, its probably a domain
            projectPath = "projects/project_" + str(form.id)
            projectPath = "/opt/bitnami/apps/django/django_projects/static/" + projectPath
            # projectPath = staticfiles_storage.url(projectPath)
            try:
                os.makedirs(projectPath)
            except FileExistsError:
                print("Using already made path")
            imgURL = projectPath + "/" + "project-image.png"
            print(imgURL)
            with open(imgURL, "wb") as f:
                f.write(base64.b64decode(imgData))
        partIDs = []
        parts = request.POST.get("parts")
        parts = parts.split(",") if parts else []
        print("parts: " + str(parts))
        partNames = []
        for part in parts:
            partObj = None
            partName = part.split(" x ")[1]
            try:
                partObj = Parts.objects.get(name__exact=partName)
            except Parts.DoesNotExist:
                partObj = None
                print("Does Not Exist. Creating Part")
                partObj = createPart(partName) # create part if not found
            if partObj:
                partIDs.append(partObj.id)
                partNames.append(partName)
        print("partIDs: " + str(partIDs))

        form.name = request.POST.get("name")
        form.desc = request.POST.get("desc")
        form.difficulty = request.POST.get("difficulty")
        form.steps = str(request.POST.get("steps"))
        form.parts = str(request.POST.get("parts"))
        imgURL = imgURL.replace("/opt/bitnami/apps/django/django_projects/", "")
        imgURL = imgURL[imgURL.find("projects/"):] if imgURL else ""
        form.imgPath = imgURL
        form.published = int(published)
        form.partNames = partNames
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
        url = str(form.id)
        form.url = url
        form.author.add(request.user)
        form.save()
        return HttpResponse(url)
    categories = []
    result = ProjectCategories.objects.all()
    for part in result:
        categories.append({"name": part.name})
    context["categories"] = categories
    return render(request, 'hub/newCreateProject.html', context)

@ensure_csrf_cookie
def linkProject(request, projectID=0):
    account = request.user.username if request.user.is_authenticated else None
    context = {"account": account}
    if projectID and request.user.is_authenticated:
        project = Project.objects.filter(id=projectID, author=request.user).first()
        if project:
            # editing project
            parts = project.parts.split(",")
            partsArray = []
            for part in parts:
                part = part.split(" x ")
                if len(part) == 2:
                    partsArray.append({"quantity": part[0], "name": part[1]})
            steps = formatSteps(project.steps)
            context["project"] = {
                "name": project.name,
                "desc": project.desc,
                "difficulty": project.difficulty,
                "parts": partsArray,
                "steps": steps,
                "img": project.imgPath,
                "category": project.category.name,
                "published": project.published,
                "url": project.url
            }
    if request.method == 'POST' and request.user.is_authenticated:
        published = request.POST.get("published")
        if published:
            name = request.POST.get("name")
            form = None
            projectID = request.POST.get("urlEnd") if request.POST.get("urlEnd") != "link" else None
            if projectID:
                form = Project.objects.filter(id=int(projectID)).first()
            else:
                form = Project.objects.filter(name=name).first()
            print("id: {}, form: {}, urlEnd: {}".format(projectID, str(form), request.POST.get("urlEnd")))

        if not form:
            form = Project()
            form.save()
        name = request.POST.get("name")
        formattedName = name
        if name:
            formattedName = formattedName.replace("/", "-")
            formattedName = quote_plus(formattedName)
            formattedName = formattedName.replace("+", "_")
        imgData = request.POST.get('img')
        imgData = imgData.replace("data:image/jpeg;base64,", "") if imgData else imgData
        imgData = imgData.replace("data:image/png;base64,", "") if imgData else imgData
        imgURL = form.imgPath
        if not 'static/' in str(imgData)[0:10] and imgData: # if img has a / in, its probably a domain
            projectPath = "projects/project_" + str(form.id)
            projectPath = "/opt/bitnami/apps/django/django_projects/static/" + projectPath
            # projectPath = staticfiles_storage.url(projectPath)
            try:
                os.makedirs(projectPath)
            except FileExistsError:
                print("Using already made path")
            imgURL = projectPath + "/" + "project-image.png"
            print(imgURL)
            with open(imgURL, "wb") as f:
                f.write(base64.b64decode(imgData))
        partIDs = []
        parts = request.POST.get("parts")
        parts = parts.split(",") if parts else []
        print("parts: " + str(parts))
        partNames = []
        for part in parts:
            partObj = None
            partName = part.split(" x ")[1]
            try:
                partObj = Parts.objects.get(name__exact=partName)
            except Parts.DoesNotExist:
                partObj = None
                print("Does Not Exist. Creating Part")
                partObj = createPart(partName) # create part if not found
            if partObj:
                partIDs.append(partObj.id)
                partNames.append(partName)
        print("partIDs: " + str(partIDs))

        form.name = request.POST.get("name")
        form.desc = request.POST.get("desc")
        form.parts = str(request.POST.get("parts"))
        imgURL = imgURL.replace("/opt/bitnami/apps/django/django_projects/", "")
        imgURL = imgURL[imgURL.find("projects/"):] if imgURL else ""
        form.imgPath = imgURL
        form.published = int(published)
        form.partNames = partNames
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
        url = request.POST.get("url")
        form.url = url
        form.author.add(request.user)
        form.save()
        return HttpResponse(url)
    categories = []
    result = ProjectCategories.objects.all()
    for part in result:
        categories.append({"name": part.name})
    context["categories"] = categories
    return render(request, 'hub/linkProject.html', context)


def project(request, slug):
    account = request.user.username if request.user.is_authenticated else None
    projectName = ""
    project = None
    try:
        project = Project.objects.get(url__exact=slug)
    except Project.DoesNotExist:
        page = "create"
        account = request.user.username if request.user.is_authenticated else None
        context = {"account": account, "page": page}
        context["message"] = {"text": "We can find this project, would you like to create one?", "color": "red"}
        return render(request, "hub/newCreateProject.html", context)
    projectName = project.name
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
            form.user = request.user
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
        return redirect("loginAndRegister") #CHECK# we need to make it so it redirects back


def upvote(request):
    type = request.POST.get("type")
    elementID = request.POST.get("elementID")
    operation = request.POST.get("operation")
    if not request.user.is_authenticated:
        return redirect("loginAndRegister")
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
            projects = Project.objects.order_by("-upvotes").filter(category=category).exclude(published=0)[startOfResults:startOfResults+num_of_results]
        else:
            projects = Project.objects.order_by("-upvotes").exclude(published=0)[startOfResults:startOfResults+num_of_results]

    if filter == "popular":
        if category:
            projects = Project.objects.order_by("-views").filter(category=category).exclude(published=0)[
                       startOfResults:startOfResults + num_of_results]
        else:
            projects = Project.objects.order_by("-views").exclude(published=0)[startOfResults:startOfResults + num_of_results]

    projects = {"projects": getProjectsFromQuery(projects)}
    return HttpResponse(json.dumps(projects))

def contact(request):
    account = request.user.username if request.user.is_authenticated else None
    context = {"account": account}
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        country = request.POST.get("country")
        subject = request.POST.get("subject")
        message = "From: " + name + ", Email: " + email + "\n"
        message += "Country: " + country + "\n"
        message += subject
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        fromEmail = 'diyhub.io@gmail.com'
        toEmail = 'benthefreelancer@gmail.com'
        send_mail('Contact Form Message: ' + now, message, fromEmail, [toEmail], fail_silently=False)
        context["message"] = {"text": "Message Sent", "color": "green"}
        return render(request, 'hub/contact.html', context)
    return render(request, 'hub/contact.html', context)

def about(request):
    account = request.user.username if request.user.is_authenticated else None
    context = {"account": account}
    return render(request, 'hub/about.html', context)

def getProjectsByParts(request):
    projectsArray = []
    projects = {}
    if request.method == "POST":
        parts = request.POST.get("parts")
        parts = parts.split(",")
        if parts:
            partQueryString = ""
            for part in parts:
                partQueryString += " " + part
            query = SearchQuery(partQueryString)
            vector = SearchVector('parts')
            projectResults = Project.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').exclude(partNames__contained_by=parts).exclude(published=0)
            projects["almostProjects"] = getProjectsFromQuery(projectResults)
            projectResults = Project.objects.filter(partNames__contained_by=parts).exclude(published=0)
            print(parts)

            projects["projects"] = getProjectsFromQuery(projectResults)
            print(projects)
    return HttpResponse(json.dumps(projects))

def discovery(request):
    page = "discover"
    projects = Project.objects.filter(published=1)
    projectsArray = []
    account = request.user.username if request.user.is_authenticated else None
    projectsArray = getProjectsFromQuery(projects)
    context = {"projects": projectsArray, "account": account, "page": page}
    return render(request, 'hub/discovery.html', context)

def getProjectsFromQuery(projects):
    projectsArray = []
    if projects:
        for project in projects:
            desc = removeElements(project.desc, ["<h1>", "</h1>", "<strong>", "</strong>", "<em>", "</em>", "<u>", "</u>", "<ul>", "</ul>", "<li>", "</li>"])
            shortDesc = desc[:150] + "... " if len(desc) > 150 else desc
            print("debug: getting the shorter desc: {}".format(shortDesc))
            projectsArray.append(
                {"name": project.name, "desc": desc, "shortDesc": shortDesc ,"imgPath": project.imgPath, "url": project.url,
                 "difficulty": project.difficulty, "upvotes": Upvote.objects.filter(project=project).count(), "views": project.views, "published": project.published})

    return projectsArray

def removeElements(initial, elements):
    for element in elements:
        initial = initial.replace(element, "")
    return initial

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                print("send mail to reset")
                token = gen_token()
                while User.objects.filter(passwd_reset_token=token).first():
                    token = gen_token()
                user.passwd_reset_token = token
                user.passwd_reset_token_timestamp = timezone.now()
                user.save()
                mail_context = {
                    'protocol': 'http',
                    'domain': 'diyhub.io',
                    'uid': user.id,
                    'token': token
                }
                html_message = render_to_string('hub/forgotPassword_email.html', context=mail_context)
                plain_message = strip_tags(html_message)
                fromEmail = 'diyhub.io@gmail.com'
                toEmail = email
                send_mail("Reset Password", plain_message, fromEmail, [toEmail], fail_silently=False, html_message=html_message)
                return render(request, "hub/forgotPassword_done.html")
            else:
                print("Not a recognized email")
                context = {"message": {"text": "Email not recognized", "color": "red"}}
                return render(request, "hub/forgotPassword.html", context)
    return render(request, 'hub/forgotPassword.html')


def resetPassword(request, uidb64=None, token=None):
    if uidb64 and token:
        user = User.objects.filter(passwd_reset_token=token).first()
        if user:
            now = timezone.now()
            token_timestamp = user.passwd_reset_token_timestamp
            if (now - token_timestamp).days == 0:
                if request.method == "POST":
                    if request.POST.get("newPassword") == request.POST.get("newPassword2"):
                        user.set_password(request.POST.get("newPassword"))
                        user.passwd_reset_token = None
                        user.save()
                        login(request, user)
                        return render(request, "hub/resetPassword_complete.html")
                else:
                    return render(request, "hub/resetPassword.html", context={'validlink': True, 'uid': uidb64, 'token': token})
    return render(request, 'hub/resetPassword.html', context={'validlink': False, 'uid': None, 'token': None})

def comingSoon(request):
    return render(request, 'hub/comingSoon.html')

def formatSteps(steps):
    steps = steps.split('<div class="steps-container">')[1:]
    for i in range(0, len(steps)):
        steps[i] = steps[i][:-6]
        name = steps[i].split("<div class='stepDesc'>")[0]
        name = name.replace("<h2>", "") if name else name
        name = name.replace("</h2><hr>", "") if name else name
        print(steps[i].split("<div class='stepDesc'>"))
        desc = steps[i].split("<div class='stepDesc'>")[1]
        desc = desc[:-6] if len(desc) > 6 else desc

        steps[i] = {"name": name, "desc": desc}
    return steps

def gen_token():
    return rstr.xeger(r'[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}')
