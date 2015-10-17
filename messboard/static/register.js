addLoadEvent(startTime);
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
						if(validate_required(username,"please input username") == false){
							username.focus();
							return false;
						}
						else if(validate_required(pwd1,"please input password ") == false){
							pwd1.focus();
							return false;
						}
						else if(validate_required(pwd2,"please input password") == false){
							pwd2.focus();
							return false;
						}
						else if(pwd1.value != pwd2.value){
							
							alert("您输入的密码不一致！！")
							return false;
						}
					}
				}
				
function startTime(){
					var today = new Date();
					var time = today.toLocaleString();
					document.getElementById("readTime").innerHTML=time;
					t = setTimeout("startTime()",500);
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
