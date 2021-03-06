var sortMethod = "popular";
$(document).ready(function() {
    $("#popularSort").click(function () {
        $(".grid a").remove();
        sortMethod = "popular";
        resultsPerPage = $("#resultsPerPage").val();

        filterProjects("popular", resultsPerPage, getUserID());
    });
    $("#likedSort").click(function () {
        $(".grid a").remove();
        sortMethod = "most_liked";
        resultsPerPage = $("#resultsPerPage").val();
        filterProjects("most_liked", resultsPerPage, getUserID());
    });
    $("#resultsPerPage").change(function () {
        $(".grid a").remove();
        filterProjects(sortMethod, $(this).val(), getUserID());
    });
});

function filterProjects(method, projectsPerPage=25, userID=false) {
    let url;
    // the following lines are if there is a userID in the filter but i don't think thats actually ever used
    // if (userID){
    //     url = "/filterProjects/" + method + "/" + userID + "/" + projectsPerPage.toString();
    // }else {
    //     url = "/filterProjects/" + method + "/" + projectsPerPage.toString();
    // }
    url = "/filterProjects/" + method + "/" + projectsPerPage.toString();
    $.get(url).done(function (data) {
        refreshProjects(JSON.parse(data));
    });

}
function getUserID() {
    if ($("meta[name='userID']")[0]) {
        return $("meta[name='userID']")[0].content;
    }else {
        return false;
    }
}

function refreshProjects(projects) {

    //console.log(projects["projects"]);
    for(i = 0; i < projects["projects"].length; i++){
        var color;
        var styles;
        if (projects["projects"][i].difficulty === 1) {
            color = "#14aa30";
        }
        else if (projects["projects"][i].difficulty === 2) {
            color = "#43d540";
        }
        else if (projects["projects"][i].difficulty === 3) {
            color = "#b8b82e";
        }
        else if (projects["projects"][i].difficulty === 4) {
            color = "#FE7F2F";
        }
        else if (projects["projects"][i].difficulty === 5) {
            color = "#FE2F2F";
        }
        if (projects["projects"][i].difficulty) {
            styles = "<div class=\"overlay\" style=\"background-color: " + color + "\">"
        }else {
            styles = "<div class=\"overlay\">"
        }
        var element = "<a href=\"project/" + projects["projects"][i].url + "\">\n" +
            "      <div class=\"module\">\n" +
            "\t  <div class=\"container-grid\">\n" +
            "          <img src=\"/static/" + projects["projects"][i].imgPath + "\" alt=\"ProjectImage\" onerror=\"this.onerror=null;this.src='https://s3-us-west-2.amazonaws.com/diyhub.io/ProjectImage.png';\">\n" +
            styles +
            "              <h1>" + projects["projects"][i].name + "</h1>\n" +
            "              <p>" + projects["projects"][i].shortDesc + "</p>\n" +
            "<span>" + projects["projects"][i].views + "<i class=\"fa fa-eye\"></i> <span id=\"projectUpvoteCounter\">" + projects["projects"][i].upvotes + "</span> <i class=\"fa fa-thumbs-up\"></i></span>" +
            "          </div>\n" +
            "</div>" +
            "    </div>" +
            "      </a>";
        console.log(element);
        $(".grid-makable").append(element);
    }
}