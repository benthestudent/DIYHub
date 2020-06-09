import apyori as apriori

class Recommender:
    def __init__(self, users, max_upvotes=20, order="confidence"):  #user = {user(id), upvote_set}
        rules = []  # rule = {"item1": ..., "item2": ..., "lift": ..., "confidence": ..., "support": ... }
        self.users = users
        self.MAX_UPVOTES_PER_USER = max_upvotes
        self.rules = None
        self.order = order

    def refreshRules(self):
        #make dataset of user's upvotes
        upvoteData = []
        for user in self.users:
            upvoteData.append(self.getUpvotedProjectsFromUser(user))

        #make rules with apyori algorithm
        self.rules = apriori(transactions=upvoteData, min_support=0.003, min_confidence=0.2, min_lift=3, min_length=2, max_length=2)
        self.rules = self.formatRules(self.rules)

    def getUpvotedProjectsFromUser(self, user):
        upvotes = user.upvote_set.all()
        formattedProjects = []
        for i in range(1, self.MAX_UPVOTES_PER_USER):
            if i <= len(upvotes):
                formattedProjects.append(upvotes[i].project.first().name)
            else:
                formattedProjects.append(None)
        return formattedProjects

    def formatRules(self, results):
        lhs = [tuple(result[2][0][0])[0] for result in results]
        rhs = [tuple(result[2][0][1])[0] for result in results]
        supports = [result[1] for result in results]
        confidences = [result[2][0][2] for result in results]
        lifts = [result[2][0][3] for result in results]
        return list(zip(lhs, rhs, supports, confidences, lifts))

    def saveRules(self):
        pass

    def getRecommendations(self, user, num=25):
        recommendations = []
        #get upvotes of user
        usersUpvotes = user.upvote_set.all()
        for upvote in usersUpvotes:
            project = upvote.project.first()
            rules = Rule.objects.filter(projects=project)
            for rule in rules:
                recommendations.append(rule.projects.exclude(project).first().name)
        return recommendations[:num]



        return None