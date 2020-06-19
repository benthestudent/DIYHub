import pandas as pd
# from hub.models import PartCategories, Parts, Project
parts = pd.read_csv("hub/parts.csv")
names = parts.iloc[:,0].values
urls = parts.iloc[:,1].values
categories = parts.iloc[:, 2].values

for i in range(1, len(names)):
    part = Parts()
    part.name = names[i]
    part.url = urls[i]
    part.category = getCategory(categories[i])
    part.save()

def getCategory(name):
    cat = PartCategories.objects.filter(name=name).first()
    if cat:
        return cat
    else:
        newCat = PartCategories()
        newCat.name = name
        newCat.save()
        return newCat
## load projects

projects = [
        {"header": "Squirrel Picnic Table", "desc": "Here is how to make the easiest and cutest squirrel feeder ever! This will keep squirrels out of ...", "link": "https://www.instructables.com/id/Squirrel-Picnic-Table/", "parts":  [2,3,4,5,6,7,8,9]},
        {"header": "Windchimes From Leftovers", "desc": "After replacing a section of chain link I had several pieces of leftover top rail and some fencin...", "link": "https://www.instructables.com/id/Windchimes-From-Leftovers/", "parts":  [10,11,12,13,14,15,16,17]},
        {"header": "Watering Can Planter", "desc": "This is a little project I made one afternoon when I was tinkering in the shed. I'd seen a few di...", "link": "https://www.instructables.com/id/Watering-Can-Planter/", "parts":  [18,19,20,21]},
        {"header": "Build a Raised Garden Bed", "desc": "Springtime is here and it's time for some gardening. I spent a day building a raised garden bed, ...", "link": "https://www.instructables.com/id/Build-a-Raised-Garden-Bed/","parts":  [7,8,22,23,24,25,26,27,28,29,30,31]},
        {"header": "Make a WiFi Camera Bird Box - Cheepy Cheap!", "desc": "Build your own WiFi-Camera-enabled Bird Box, cheaply, and quickly. Perfect for an After-School/Cl...", "link": "https://www.instructables.com/id/Make-a-WiFi-Camera-Bird-Box-Cheepy-Cheap/", "parts":  [2, 32,33,34,35,36]}
    ]
for project in projects:
    proj = Project()
    proj.name = project["header"]
    proj.desc = project["desc"]
    proj.url = project["link"]
    parts = ""
    partIDs = []
    for part in project["parts"]:
        pt = Parts.objects.filter(name=names[part - 2]).first()
        if pt:
            parts += pt.name + ","
            partIDs.append(pt.id)
    if len(parts) > 0:
        proj.parts = parts
        proj.partIDs = partIDs
        proj.save()
