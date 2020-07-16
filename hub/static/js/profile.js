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

function removePartFromGarage(name, userID) {
    data = {"userID": userID,
            "part": name};
    var csrftoken = getCookie('csrftoken');
		$.ajaxSetup({
    		headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
    $.ajax({
			url: '/dev/removePartFromGarage',
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

$(document).ready(function () {
    $("button.removePart").click(function () {
        let name = $(this).prev().html();
        let userID = $("meta[name='userID']").attr("content");
        let res = removePartFromGarage(name, userID);
        console.log(res);
        $(this).parent().remove();
    });
    $("#change-password").click(function () {
        $(this).html("Change");
        if($("#oldPassword").length === 0) {
            $(this).before("<h3><strong>Old Password:</strong><input type=\"password\" name=\"oldPassword\" id=\"oldPassword\"></h3>\n" +
                "            <h3><strong>Password:</strong><input type=\"password\" name=\"newPassword\" id=\"newPassword\"></h3>\n" +
                "            <h3><strong>Repeat Password:</strong><input type=\"password\" name=\"newPassword1\" id=\"newPassword1\"></h3>");
        }else{
            if ($("#newPassword").hasClass("valid") && $("#newPassword").val() === $("#newPassword1").val() && $("#oldPassword").val()) {
			    $(this).closest("form").submit();
		    }else{
			    alert("Please make sure your new passwords match and you have entered your old password.");
		    }
        }
    });

    $("#profile_files").change(function () {
        if($("#saveProfile").length === 0) {
            $("form").append("<br><button id=\"saveProfile\">Save</button>");
        }

    });
});

 $(document).on("click", "#edit", function () {
        let name = $(this).parent().find("span").attr("id");
        let value = $(this).parent().find("span").html()
        $(this).parent().find("span").html("<input name=\"" + name + "\" id=\"" + name + "\" value='" + value + "' type=\"text\">");
        if($("#saveProfile").length === 0) {
            $(this).parent().parent().append("<br><button id=\"saveProfile\">Save</button>");
        }
        $(this).remove();
 });



 $(document).on("click", "#editBio", function () {
        let name = "bio"
        let value = $("#bio").html()
        $("#bio").html("<textarea name=" + name + " id=" + name + " rows=\"3\">" + value + "</textarea><br>");
        if($("#saveProfile").length === 0) {
            $(this).parent().parent().append("<br><button id=\"saveProfile\">Save</button>");
        }
        $(this).remove();
 });

// $(document).on("input", "#newPassword1", function () {
//         $("#change-password").attr("type", "submit");
// })

$(document).on('input','#newPassword', function() {
        console.log("typing");
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

$(document).on('input','#newPassword1', function() {
        console.log("typing");
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