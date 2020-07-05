function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function vote(element, type){
		var operation = "upvote"
		if ($(element).html() === "Upvoted"){
			operation = "downvote"
		}
		var elementID;
		if (type === "comment"){
			elementID = $(element).parent().find("data").val();
			let votes = $(element).parent().find("#commentUpvoteCounter").html();
			if (operation === "downvote"){$(element).parent().find("#commentUpvoteCounter").html(--votes);}
			if (operation === "upvote"){$(element).parent().find("#commentUpvoteCounter").html(++votes);}
		}else if (type === "project"){
			elementID = $("meta[name='projectID']").attr("content");
			let votes = $("#projectUpvoteCounter").html();
			if (operation === "downvote"){$("#projectUpvoteCounter").html(--votes);}
			if (operation === "upvote"){$("#projectUpvoteCounter").html(++votes);}
		}
		var csrftoken = getCookie('csrftoken');
		$.ajaxSetup({
    		headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
		data = {"elementID": elementID, "type": type, "operation": operation};
		$.ajax({
			url: '/dev/upvote',
			data: data,
			type: 'POST',
			success: function(response) {
				console.log("success");
				console.log(response);
				if (response === "upvoted"){
					$(element).html("Upvoted");
					$(element).css("background-color", "#037F8C");
					$(element).css("border-color", "#037F8C");
				}else if (response === "downvoted"){
					$(element).html("Upvote");
					$(element).css("background-color", "transparent");
					$(element).css("border-color", "white");
				}

			},
			error: function(response) {
				console.log("error");
			}
		});
}

$(document).ready(function () {
    $("#commentInput").on('input', function () {
        console.log("input");
        $(this).prop('style').cssText = 'height:auto;';
        $(this).prop('style').cssText = 'height:' + $(this).prop('scrollHeight') + 'px';
    });

	$("#projectUpvote").click(function () {
		vote(this, "project");
	});
});

function createComment(element, type){
	var body = $(element).parent().parent().find("textarea").val();
	var elementID;
	if (type === "comment"){
			elementID = $(element).parent().parent().parent().prev(".comment-upvote").find("data").val();
			console.log(elementID);
	}else if (type === "project"){
			elementID = $("meta[name='projectID']").attr("content");
	}
	console.log(body);
	var data = {"body": body, "elementID": elementID, "type": type}
	$(element).parent().parent().remove();
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
		headers: { "X-CSRFToken": getCookie("csrftoken") }
	});
	$.ajax({
				url: '/dev/addComment',
				data: data,
				type: 'POST',
				success: function(response) {
					location.reload();
				},
				error: function(response) {
					console.log("error");
				}
	});
}

$(document).on("click", "#comment", function () {
	createComment(this, type="project");
});

$(document).on("click", "#replyButton", function () {
	createComment(this, type="comment");
});

$(document).on("click", "#commentUpvote", function () {
	vote(this, "comment");
});