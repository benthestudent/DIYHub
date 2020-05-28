
function addStep() {
			let step = "<div class=\"step add-step\"><input type=\"text\" name=\"step\" value=\"Name of Step\"><div class=\"description\"><textarea placeholder=\"What happens in this step?\" rows=\"7\"></textarea></div></div>";
			$(".steps").append(step);
			return false;
}

function addPart() {
			let part = "<div class=\"part add-part\"><input type=\"text\" name=\"part\" value=\"Search for a Part\"><i class=\"fa fa-search\"></i><i class=\"fa fa-plus-circle right\" onclick=\"addPart()\" style=\"font-size:24px\"></i></div>";
			$(".supplies-container").append(part);
			return false;
}