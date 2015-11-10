

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
		var dele_by_id = thiswords.id;
		var myInput = document.createElement("input");
		myInput.type = "text";
		myInput.name = "dele_by_id";
		myInput.value = dele_by_id;
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

function validate_required(field,alerttxt){
					with(field){
						if(value == null || value == ""){
							alert(alerttxt);
							return false;
						}
						else{
							return true;
						}
					}
				}
				
function validate_form(thisform){
					with(thisform){
						if(validate_required(username,"请输入用户名！") == false){
							username.focus();
							return false;
						}
						else if(validate_required(pwd1,"请输入密码！") == false){
							pwd1.focus();
							return false;
						}
						else if(validate_required(pwd2,"请输入密码！") == false){
							pwd2.focus();
							return false;
						}
						else if(pwd1.value != pwd2.value){
							
							alert("您输入的密码不一致！！")
							return false;
						
						}
						else{
							return true;
						}
					}
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