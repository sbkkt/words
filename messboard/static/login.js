addLoadEvent(startTime);

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

