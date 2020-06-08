$(document).ready(function () {
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
})

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