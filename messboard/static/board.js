addLoadEvent(startTime)

function startTime(){
					var today = new Date();
					var time = today.toLocaleString();
					document.getElementById("readTime").innerHTML=time;
					t = setTimeout("startTime()",500);
				}

function delewords(thiswords){
		
		var myForm = document.createElement("form");
		myForm.method = "post";
		myForm.action = "board";
		var dele_by_time = thiswords.id;
		var myInput = document.createElement("input");
		myInput.type = "text";
		myInput.name = "dele_by_time";
		myInput.value = dele_by_time;
		myForm.appendChild(myInput);
		document.body.appendChild(myForm);
		myForm.submit();
		document.body.removeChild(myForm);
					
}
				
function addLoadEvent(func){
	var oldonload = window.onload;
	if(typeof oldonload != 'function'){
		onload = func;
	}
	else{
		window.onload = function(){
			oldonload();
			func();
		}
	}
}