

function loadProjectsFromParts() {
	let parts = "";
	$("input[type='checkbox']").each(function() {
			if (this.checked) {
				var part = $(this).parent(".container").text().trim();
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
			url: '/getProjects',
			data: data,
			type: 'POST',
			success: function(response) {
				$(".grid a").remove();
				$(".grid h2").remove();
				$(".divider").remove();
				$(".grid-almost-makable").remove();
				refreshProjects(JSON.parse(response));
			},
			error: function(response) {
				console.log("error");
			}
		});
}

function saveProfileImg() {
	url = $("#profileImg").attr('src');
		let data = {"img": url};
        var csrftoken = getCookie('csrftoken');
		$.ajaxSetup({
    		headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
		console.log(data);
        $.ajax({
			url: '/updateProfileImg',
			data: data,
			type: 'POST',
			success: function(response) {
				console.log("success");
				console.log(response);
			},
			error: function(response) {
				console.log(response);
				return response;
			}
		});
}

function togglePartInGarage(name, userID, operation) {
	data = {"userID": userID,
            "part": name};
    var csrftoken = getCookie('csrftoken');
		$.ajaxSetup({
    		headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
	let url = "";
	if (operation === "add") {
		url = '/addPartFromGarage';
	}else {
		url = '/removePartFromGarage';
	}
    $.ajax({
			url: url,
			data: data,
			type: 'POST',
			success: function(response) {
				console.log("success");
				console.log(response);
				return 1;

			},
			error: function(response) {
				console.log(response);
				return response;
			}
		});
}


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
	if($("#part").val().includes(" and ") || $("#part").val().includes(" or ") || $("#part").val().includes("optional"))
			alert("Please input only one item per part (no 'and' or 'or' in part names). If the part is optional, don't include it in the parts list, but feel free to mention it in a step. If a part has an alternative, pick the best option and list alternatives in the steps.");
	else {
		console.log("add part button");
				// add <i class="fa fa-pencil pencil" id="editPart" style="font-size:24px"></i> for editing
				let part = "<div class=\"border rounded border-primary d-inline-flex align-items-sm-center addedPart\" style=\"width: 100%;padding: 1%;border-color: #575757;\"><input style=\"width: 10%;margin-right: 1%;padding: 5px;\" class=\"border rounded border-secondary\" type=\"text\" name=\"quantity\" value=\"" + $("#quantity").val() + "\" readonly><input style=\"width: 70%;margin-right: 1%;padding: 5px;\" class=\"border rounded border-secondary\" type=\"text\" name=\"part\" id=\"part\" value=\"" + $("#part").val() + "\" readonly><input style=\"width: 10%;margin-right: 1%;padding: 5px;\" class=\"border rounded border-secondary\" type=\"text\" name=\"part\" id=\"part\" value=\"" + $("#partCat").val() + "\" readonly><i class=\"fa fa-trash-o trash right\" style=\"font-size:24px\"></i></div>";
				$("#quantity").val("");
				$("#part").val("");
				$("#partCat").val("General");
				$('#partsDefault').remove();
				$(".supplies-container").append(part);
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
		let q = 0
		var quantity = 0;
		var partName = "";
		var category = "";
		$(this).children("input").each(function() {
			if (q === 0) {
				if (this.value) {
					quantity = this.value
				}

				q++;
			}else if(q === 1) {
				partName = this.value
				if (!partName) {
						partsCompleted = false;
				}
				q++;
				// var partArray = partName.split(",");
				// for(var i = 0; i < partArray.length; i++) {
				// 	if (!partName) {
				// 		partsCompleted = false;
				// 	}
				// 	if (quantity) {
				// 		parts += quantity + " x " + partArray[i] + " or ";
				// 	} else {
				// 		parts += partArray[i] + " or ";
				// 	}
				// }
				// parts = parts.slice(0, -4) + ","

			}else {
				category = this.value;
				if (quantity) {
					parts += quantity + " x " + partName + " -cat=" + category;
				} else {
					parts += partName + " -cat=" + category;
				}
				parts += ",";
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
	var url = $("#projectUrl").val();
	console.log(img);
	completed = 0;
	console.log("name:" + projectName + " desc:" + projectDesc + " diff:" + difficulty + " parts:" + parts + " partsCompleted:" + partsCompleted + " steps:"+ steps + " img:" + img + " cat:" + category);
	if (projectName && projectDesc && difficulty && parts && partsCompleted && steps && img && category) {
		completed = 1;
	}
	completedForLink = 0;
	if (projectName && projectDesc && parts && partsCompleted && url && img && category) {
		completedForLink = 1;
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
		"completedForLink": completedForLink,
		"urlEnd": last_part,
		"url": url
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

function readURL(input, imageElement) {
	let fileTypes = ['jpg', 'jpeg', 'png'];  //acceptable file types
	var imgData;
    if (input.files && input.files[0]) {
    	var extension = input.files[0].name.split('.').pop().toLowerCase(),  //file extension from input file
			isSuccess = fileTypes.indexOf(extension) > -1;  //is extension in acceptable types

        if (isSuccess) {
			var reader = new FileReader();

			reader.onload = function (e) {
				$(imageElement).attr('src', e.target.result);
				imgData = e.target.result;
				if (imageElement === "#profileImg") {
					saveProfileImg();
				}else { //for project image
					$('#projectImg').removeClass("invisible");
					$(".cont").removeClass("center");
				}
			}

			reader.readAsDataURL(input.files[0]);
		}
        else {
        	alert("Please select an image of type jpg, png, or jpeg.");
        }

    }
	else {
    	alert("No Image");
	}

}

function refreshProjects(projects, almost=false) {
    for(i = 0; i < projects["projects"].length; i++){
        var color;
        var styles;
        var url = projects["projects"][i].url;
        if (url.indexOf("http://") !== -1 || url.indexOf("https://") !== -1) {
			url = "external/?url=" + url;
		}
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
        var element = "<a href=\"/project/" + url + "\">\n" +
            "      <div class=\"module\">\n" +
            "\t  <div class=\"container-grid\">\n" +
            "          <img src=\"static/" + projects["projects"][i].imgPath + "\" alt=\"ProjectImage\"  onerror=\"this.onerror=null;this.src='https://s3-us-west-2.amazonaws.com/diyhub.io/ProjectImage.png';\">\n" +
            styles +
            "              <h1>" + projects["projects"][i].name + "</h1>\n" +
            "              <p>" + projects["projects"][i].shortDesc + "</p>\n" +
            "          </div>\n" +
            "</div>" +
            "    </div>" +
            "      </a>";
        console.log("Appending Element");
        if(almost){

        	$(".grid-almost-makable").append(element);
		}else {
			$(".grid-makable").append(element);
		}
    }
    if (projects["almostProjects"] && projects["almostProjects"].length > 0){
    	console.log("PROJECTS YOU CAN ALMOST MAKE");
        	$(".grid").append("<h2 class='divider'>Projects you can almost make:</h2>");
        	$(".grid").append("<div class=\"grid-almost-makable\" style=\"\n" +
				"    width: 100%;\n" +
				"    overflow: visible;\n" +
				"\"></div>");
        	refreshProjects({"projects": projects["almostProjects"]}, true);
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
			url: '/upvote',
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
				url: '/addComment',
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
	if ($(".partContainer input:checkbox:checked").length > 0)
	{
		loadProjectsFromParts();// any one is checked
	}
	else
	{
	   // none is checked
	}

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
			$(this).html("<div class='loader'></div>");
			var elem = $(this);
			var csrftoken = getCookie('csrftoken');
			var data = getProjectData();
			data.published = 0;
			$.ajaxSetup({
				headers: { "X-CSRFToken": getCookie("csrftoken") }
			});
			console.log(JSON.stringify(data))
			$.ajax({
						url: '/create',
						data: data,
						type: 'POST',
						success: function(response) {
							console.log(response.text);
							if (response.indexOf("//www.") === -1) {
								document.location.href = "/create/" + response;
							} else {
								window.location.href = response;
					}
						},
						error: function(response) {
							console.log("error");
							elem.html("Save");
						}
			});
		}
	});
	$("#publish").click(function() {
		$(this).html("<div class='loader'></div>");
		var elem = $(this);
		var csrftoken = getCookie('csrftoken');
		var data = getProjectData();
		if (data.completed) {
			data.published = 1;
			$.ajaxSetup({
				headers: {"X-CSRFToken": getCookie("csrftoken")}
			});
			console.log(JSON.stringify(data))
			$.ajax({
				url: '/create',
				data: data,
				type: 'POST',
				success: function (response) {
					console.log(response);
					if (response.indexOf("//www.") === -1) {
						document.location.href = "/project/" + response;
					} else {
						window.location.href = response;
					}
				},
				error: function (response) {
					console.log("error");
					elem.html("Publish");
					alert("Could not Publish. Error saving project. Please contact site administrator, using contact page.");
				}
			});
		}else {
			elem.html("Publish");
			alert("You have not completely filled out your project. Go back and make sure you have a name, description, image, supplies, and steps");
		}
	});

	$("#link").click(function() {
		$(this).html("<div class='loader'></div>");
		var csrftoken = getCookie('csrftoken');
		var data = getProjectData();
		if (data.completedForLink) {
			data.published = 1;
			$.ajaxSetup({
				headers: {"X-CSRFToken": getCookie("csrftoken")}
			});
			console.log(JSON.stringify(data))
			$.ajax({
				url: '/link',
				data: data,
				type: 'POST',
				success: function (response) {
					console.log(response);
						document.location.href = response;

				},
				error: function (response) {
					console.log("error");
					$(this).html("Link");
					alert("Could not Publish. Error saving project. Please contact site administrator, using contact page.");
				}
			});
		}else {
			$(this).html("Link");
			alert("You have not completely filled out your project. Go back and make sure you have a name, description, image, url, and supplies");
		}
	});

	$("#files").change(function() {
		$('#projectImg').attr('src', readURL(this, "#projectImg"));

	});

	$("#profile_files").change(function() {
		let url = readURL(this, "#profileImg");
	});

	$("#part").on("input", function (event) {
		if(!$("#partsList").length){
			$("#part").after(" <datalist id=\"partsList\"></datalist>");
		}
		$.ajax({
			url: '/getParts',
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
			url: '/getCategories',
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
			url: '/getCategories',
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
		if ($("#register-username").hasClass("valid") && $("#register-password").hasClass("valid") && $("#register-email").hasClass("valid") && $("#register-username").val() && $("#register-password").val() && $("#register-email").val() && $("#agree-to-ppp")[0].checked) {
			$(this).closest("form").submit();
		}else{
			$(".validation-error").removeClass("invisible");
		}
	});

	$("#reset-pass-button").click(function () {
		if ($("#register-password").hasClass("valid") && $("#register-password").val() && $("#reset-password-confirm").val() && $("#register-password").val() === $("#reset-password-confirm").val()) {
			$(this).closest("form").submit();
		}else{
			$(".validation-error").removeClass("invisible");
		}
	});

	$(".partContainer input[type='checkbox']").change(function() {
		if ($(this)[0].checked && $("meta[name='userID']").attr("content")) {
			let name = $(this).parent(".container").text().trim();
			let userID = $("meta[name='userID']").attr("content");
			togglePartInGarage(name, userID, "add");
		}else if (!$(this)[0].checked && $("meta[name='userID']").attr("content")) {
			let name = $(this).parent(".container").text().trim();
			let userID = $("meta[name='userID']").attr("content");
			togglePartInGarage(name, userID, "remove");
		}
		loadProjectsFromParts();
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

$(window).on("load",function(){
     $(".loader-wrapper").fadeOut("slow");
});