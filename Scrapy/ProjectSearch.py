import jellyfish

project = {'name': "Project", 'parts': ['wire', 'led light', '3.5v battery']}
parts = ['red wire', 'blue 22 gauge wire', 'LED', '9v battery']

def projectMatch(project):
    for part in project["parts"]:
        for pt in parts:
            pt = pt.split(" ")
            for word in pt:
                print(jellyfish.jaro_distance(word, part))

projectMatch(project)