function addStep() {
			let stepID = "stepDesc" + $(".add-step").length.toString();
			var appendElem = ".added";
			var stepName = $("#stepName").val()
			var stepContent = $("#stepEditor").children("div").html()
			if($(".saved").length > 0){
				stepName = "";
				stepContent = "";
				appendElem = ".steps"
			}else{
				if (stepName === "" || stepContent === "<p><br></p>"){
					alert("Step may not be empty");
					return
				}
			}
			let step = "<div class=\"step add-step\">"
				+ "<input name=\"step\" type=\"text\" style=\"margin:auto;width: 70%;font-family: Montserrat, sans-serif;margin-bottom: 2%;font-weight: bold;\" placeholder=\"Name of Step\" value=\"" + stepName + "\">"
				+ "<div class='description' style='width: 70%; margin: auto; color: black;'><div id=\"" + stepID + "\" class=\"editor\">" + stepContent + "</div></div>"
				+ "<div class='step-buttons'>"
				+ "<i class=\"fa fa-trash-o remove-step\" style=\"font-size:24px\"></i></div></div>";
			if($(".saved").length > 0){

			}
			$(appendElem).append(step);


			$("#stepEditor").children("div").html("")
			var quill = new Quill('#' + stepID,
				{
					modules: {
					toolbar: [
					  [{ header: [1, 2, false] }],
					  ['bold', 'italic', 'underline'],
					  ['image', 'code-block']
					]
				  	},
					  scrollingContainer: '#scrolling-container',
					  theme: 'snow',
					  placeholder: 'What happens in this step?'
				});
			$("#stepName").val("");
			$("#stepEditor").val("");
			return false;
}

function addPart() {
			console.log("add part button");
			if(!isNaN($('#quantity').val())) {
				// add <i class="fa fa-pencil pencil" id="editPart" style="font-size:24px"></i> for editing
				let part = "<div class=\"border rounded border-primary d-inline-flex align-items-sm-center addedPart\" style=\"width: 100%;padding: 1%;border-color: #575757;\"><input style=\"width: 10%;margin-right: 1%;padding: 5px;\" class=\"border rounded border-secondary\" type=\"text\" name=\"quantity\" value=\"" + $("#quantity").val() + "\" readonly><input style=\"width: 80%;margin-right: 1%;padding: 5px;\" class=\"border rounded border-secondary\" type=\"text\" name=\"part\" id=\"part\" value=\"" + $("#part").val() + "\" readonly><i class=\"fa fa-trash-o trash right\" style=\"font-size:24px\"></i></div>";
				$("#quantity").val("");
				$("#part").val("");
				$('#partsDefault').remove();
				$(".supplies-container").append(part);
			}else {
				alert("Quantity must be a number");
			}
			return false;
}

//The next three functions handle the edit, save and delete icons for the parts list
$(document).on("click", "i.pencil", function() {
		$(this).prev('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).prev('input').prev('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).removeClass("fa-pencil");
		$(this).removeClass("pencil");
		$(this).addClass("check")
		$(this).addClass("fa-check");
});

$(document).on("click", "i.check", function() {
		$(this).prev('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).prev('input').prev('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).removeClass("fa-check");
		$(this).removeClass("check");
		$(this).addClass("pencil")
		$(this).addClass("fa-pencil");
});

$(document).on("click", "i.trash", function() {
		console.log("trash");
		$(this).parent().remove();
});


//The next three functions handle the edit, save and delete icons for the steps list
$(document).on("click", "i.edit-step", function() {
		$(this).parent().find('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).prev('div').find('textarea').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).removeClass("fa-pencil");
		$(this).removeClass("edit-step");
		$(this).addClass("save-step")
		$(this).addClass("fa-check");
});

$(document).on("click", "i.save-step", function() {
		$(this).parent().find('input').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).prev('div').find('textarea').prop('readonly', function (i, r) {
			return !r;
		});
		$(this).removeClass("fa-check");
		$(this).removeClass("save-step");
		$(this).addClass("edit-step")
		$(this).addClass("fa-pencil");
});

$(document).on("click", "i.remove-step", function() {
		console.log("trash");
		$(this).parent().parent().remove();
});

// comment, reply, and upvote functions
$(document).on("click", "#comment", function () {
	createComment(this, type="project");
});

$(document).on("click", "#replyButton", function () {
	createComment(this, type="comment");
});

$(document).on("click", "#commentUpvote", function () {
	vote(this, "comment");
});

function getProjectData() {
	var projectName = $("#projectName").val();
	var projectDesc = $("#descEditor").children("div").html()
	if (!projectDesc){projectDesc = "";}
	var difficulty = $("input:checked").val();
	var parts = "";
	var steps = "";
	var partsCompleted = true;
	var url = $(location).attr('href');
    var partsOfUrl = url.split("/");
    var last_part = partsOfUrl[partsOfUrl.length-1];

	$(".addedPart").each(function() {
		q = true
		$(this).children("input").each(function() {
			if (q) {
				var quantity = 0
				if (this.value) {
					quantity = this.value
				}
				parts += quantity + " x ";
				q = false;
			}else {
				var partName = this.value
				if (!partName) {
					partsCompleted = false;

				}
				parts += partName + ",";
			}
		});

	});
	parts = parts.slice(0, -1);
	console.log(parts);
	$(".step").each(function() {
		steps += "<div class=\"steps-container\">";
		$(this).children("input").each(function() {
			steps += "<h2>" + this.value + "</h2>";
		});
		steps += "<hr>";
		// <img src="{% static 'img/stepImage.png' %}" alt="Step Image">
		stepDesc = $(this).find(".description").children("div").children("div").html();
		if (!stepDesc){stepDesc="";}
		steps += "<div class='stepDesc'>" + stepDesc + "</div>"
		steps += "</div>";
	});
	var input = $("#files");
	var img = $("#projectImg").attr('src');
	var category = $("#category").val();
	console.log(img);
	completed = 0;
	if (projectName && projectDesc && difficulty && parts && partsCompleted && steps && img && category) {
		completed = 1;
	}
	return {
		"name": projectName,
		"desc": projectDesc,
		"difficulty": difficulty,
		"parts": parts,
		"steps": steps,
		"img": img,
		"category": category,
		"completed": completed,
		"urlEnd": last_part
	};
}

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

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
        	$('#projectImg').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }else {
    	alert("No Image")
	}
}

function refreshProjects(projects) {

    console.log(projects["projects"]);
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
            "          <img src=\"static/" + projects["projects"][i].imgPath + "\" alt=\"ProjectImage\" >\n" +
            styles +
            "              <h1>" + projects["projects"][i].name + "</h1>\n" +
            "              <p>" + projects["projects"][i].desc + "</p>\n" +
            "          </div>\n" +
            "</div>" +
            "    </div>" +
            "      </a>";
        console.log(element);
        $(".grid").append(element);

    }
    if (projects["almostProjects"].length > 0){
        	$(".grid").append("<h2 class='divider'>Projects you can almost make:</h2>");
        	refreshProjects({"projects": projects["almostProjects"]});
		}
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


$(document).ready(function() {
	//comments and upvotes
	 $("#commentInput").on('input', function () {
        console.log("input");
        $(this).prop('style').cssText = 'height:auto;';
        $(this).prop('style').cssText = 'height:' + $(this).prop('scrollHeight') + 'px';
    });

	$("#projectUpvote").click(function () {
		vote(this, "project");
	});


	$(".toggle").click(function() {
		console.log("toggled");
		if(this.checked) {
			console.log("checked")
			$(this).parent().parent().find(".partContainer").removeClass("notExpanded").addClass("expand");
		}else {
			$(this).parent().parent().find(".partContainer").removeClass("expand").addClass("notExpanded");
		}
	});
	$("#save").click(function() {
		if($("#projectName").val() === ""){
			alert("Your Project Must Be Named Before Saving")
		}else {
			var csrftoken = getCookie('csrftoken');
			var data = getProjectData();
			data.published = 0;
			$.ajaxSetup({
				headers: { "X-CSRFToken": getCookie("csrftoken") }
			});
			console.log(JSON.stringify(data))
			$.ajax({
						url: '/dev/create',
						data: data,
						type: 'POST',
						success: function(response) {
							console.log(response.text);
							if (response.indexOf("//www.") === -1) {
								document.location.href = "/dev/create/" + response;
							} else {
								window.location.href = response;
					}
						},
						error: function(response) {
							console.log("error");
						}
			});
		}
	});
	$("#publish").click(function() {
		var csrftoken = getCookie('csrftoken');
		var data = getProjectData();
		if (data.completed) {
			data.published = 1;
			$.ajaxSetup({
				headers: {"X-CSRFToken": getCookie("csrftoken")}
			});
			console.log(JSON.stringify(data))
			$.ajax({
				url: '/dev/create',
				data: data,
				type: 'POST',
				success: function (response) {
					console.log(response);
					if (response.indexOf("//www.") === -1) {
						document.location.href = "/dev/project/" + response;
					} else {
						window.location.href = response;
					}
				},
				error: function (response) {
					console.log("error");
					alert("Could not Publish. Error saving project. Please contact site administrator, using contact page.");
				}
			});
		}else {
			alert("You have not completely filled out your project. Go back and make sure you have a name, description, image, supplies, and steps");
		}
	});

	$("#files").change(function() {
		$('#projectImg').attr('src', readURL(this));
		$('#projectImg').removeClass("invisible");
		$(".cont").removeClass("center");
	});

	$("#part").on("input", function (event) {
		if(!$("#partsList").length){
			$("#part").after(" <datalist id=\"partsList\"></datalist>");
		}
		$.ajax({
			url: '/dev/getParts',
			data: {"search": $("#part").val()},
			success: function (response) {
				parts = JSON.parse(response)
				$("#partsList").empty();
				parts.forEach(function (item) {
					$("#partsList").append('<option value="' + item.name + '" >');

				})

			},
		});

	});

	$("#part").change(function() {
		$("#partsList").remove();
	});

	$("#category").on("input", function (event) {
		if(!$("#categories").length){
			$("#category").after(" <datalist id=\"categories\"></datalist>");
		}
		$.ajax({
			url: '/dev/getCategories',
			data: {"search": $("#category").val()},
			success: function (response) {
				cats = JSON.parse(response)
				console.log(cats);
				$("#categories").empty();
				cats.forEach(function (item) {
					$("#categories").append('<option value="' + item.name + '" >');

				})

			},
		});

	});

	$("#category").change(function() {
		$("#categories").remove();
	});

	$("#category").focus(function () {
		$.ajax({
			url: '/dev/getCategories',
			data: {},
			success: function (response) {
				cats = JSON.parse(response)
				$("#categories").empty();
				cats.forEach(function (item) {
					$("#categories").append('<option value="' + item.name + '" >');

				})

			},
		});
	});


	//Login and Register Form validation
	$('#register-username').on('input', function() {
		var input=$(this);
		var is_name=input.val();
		if(is_name && is_name.length >= 3){
			input.removeClass("invalid").addClass("valid")
		}
		else{
			input.addClass("invalid").removeClass("valid")
		}
	});

	$('#register-email').on('input', function() {
		var input=$(this);
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
		var is_email=re.test(input.val());
		if(is_email){
			input.removeClass("invalid").addClass("valid")
		}
		else{
			input.addClass("invalid").removeClass("valid")
		}
	});

	$('#register-password').on('input', function() {
		var input=$(this);
		var password=input.val();
		var special_chars = ['.','!','#','$','%','&','*','+','/','=','?','^','_','`','{','|','}','~']
		if(password && password.length >= 6 && special_chars.some(v => password.includes(v))){
			input.removeClass("invalid").addClass("valid")
		}
		else{
			input.addClass("invalid").removeClass("valid")
		}
	});

	$("#create-account-button").click(function () {
		if ($("#register-username").hasClass("valid") && $("#register-password").hasClass("valid") && $("#register-email").hasClass("valid") && $("#register-username").val() && $("#register-password").val() && $("#register-email").val()) {
			$(this).closest("form").submit();
		}else{
			$(".validation-error").removeClass("invisible");
		}
	});
	$("input[type='checkbox']").change(function() {
		let parts = "";
		$("input[type='checkbox']").each(function() {
			if (this.checked) {
				var part = $(this).parent(".container").text().trim()
				if (part !== undefined) {
					parts += part + ",";
				}
			}
		});
		data = {"parts": parts.slice(0, -1)};
		console.log(data);
		$.ajaxSetup({
			headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
		$.ajax({
			url: '/dev/getProjects',
			data: data,
			type: 'POST',
			success: function(response) {
				console.log(response);
				$(".grid a").remove();
				$(".grid h2").remove();
				refreshProjects(JSON.parse(response));
			},
			error: function(response) {
				console.log("error");
			}
		});
	});

	$("input:radio[name='difficulty']").change(function () {
		console.log("label clicked");
		if($(".label-clicked").length > 0){
			if($(this).parent().hasClass("label-clicked")){
				$(this).parent().toggleClass("label-clicked");
			}else {
				$(".label-clicked").removeClass("label-clicked");
				$(this).parent().addClass("label-clicked");
			}

		}else {
			$(this).parent().addClass("label-clicked");
		}
	});
});

