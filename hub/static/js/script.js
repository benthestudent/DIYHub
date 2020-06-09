
function addStep() {
			let step = "<div class=\"step add-step\"><input type=\"text\" name=\"step\" value=\"" + $("#stepName").val() + "\" readonly><div class=\"description\"><textarea rows=\"7\" readonly>" + $("#stepDescription").val() + "</textarea></div><i class=\"fa fa-pencil edit-step\" id=\"editStep\" style=\"font-size:24px\"></i><i class=\"fa fa-trash-o remove-step\" style=\"font-size:24px\"></i></div>";
			$(".steps").prepend(step);
			$("#stepName").val("");
			$("#stepDescription").val("");
			return false;
}

function addPart() {

			if(!isNaN($('#quantity').val())) {
				// add <i class="fa fa-pencil pencil" id="editPart" style="font-size:24px"></i> for editing
				let part = "<div class=\"addedPart\"><input type=\"text\" name=\"quantity\" value=\"" + $("#quantity").val() + "\" readonly><input type=\"text\" name=\"part\" id=\"part\" value=\"" + $("#part").val() + "\" readonly><i class=\"fa fa-trash-o trash right\" style=\"font-size:24px\"></i></div>";
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
		$(this).parent().remove();
});

function getProjectData() {
	var projectName = $("#projectName").val();
	var projectDesc = $("#descEditor").children("div").html()
	var difficulty = $("input:checked").val();
	var parts = "";
	var steps = "";
	$(".addedPart").each(function() {
		q = true
		$(this).children("input").each(function() {
			if (q) {
				parts += this.value + " x ";
				q = false;
			}else {
				parts += this.value + ",";
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
		stepDesc = $(this).children(".description").children("#stepEditor").children("div").html()
		steps += "<div class='stepDesc'>" + stepDesc + "</div>"
		steps += "</div>";
	});
	var input = $("#upload-photo");
	var img = $("#projectImg").attr('src');
	var category = $("#category").val();
	console.log(img);
	return {
		"name": projectName,
		"desc": projectDesc,
		"difficulty": difficulty,
		"parts": parts,
		"steps": steps,
		"img": img,
		"category": category
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

$(document).ready(function() {
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
		var csrftoken = getCookie('csrftoken');
		var data = getProjectData();
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
					},
					error: function(response) {
						console.log("error");
					}
		});
	});
	$("#publish").click(function() {
		var csrftoken = getCookie('csrftoken');
		var data = getProjectData();
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
					},
					error: function(response) {
						console.log("error");
					}
		});
	});

	$("#upload-photo").change(function() {
		$('#projectImg').attr('src', readURL(this));
	});

	$("#part").on("input", function (event) {
		if(!$("#partsList").length){
			$("#part").after(" <datalist id=\"partsList\"></datalist>");
		}
		$.get({
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
		$.get({
			url: '/getCategories',
			data: {"search": $("#category").val()},
			success: function (response) {
				parts = JSON.parse(response)
				$("#categories").empty();
				parts.forEach(function (item) {
					$("#categories").append('<option value="' + item.name + '" >');

				})

			},
		});

	});

	$("#category").change(function() {
		$("#categories").remove();
	});

	$("#category").focus(function () {
		$.get({
			url: '/getCategories',
			data: {},
			success: function (response) {
				cats = JSON.parse(response)
				$("#categories").empty();
				cats.forEach(function (item) {
					$("#categories").append('<option value="' + item.name + ' (#'+ item.id + ' )" >');

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
});

