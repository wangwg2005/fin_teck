
function notify(title, body) {
	  // 先检查浏览器是否支持
	  if (!("Notification" in window)) {
	    alert("This browser does not support desktop notification");
	  }
	  
	  // 检查用户是否同意接受通知
	  else if (Notification.permission === "granted") {
	    // If it's okay let's create a notification
	    var notification = new Notification(title,{"body":body});
	  }

	  // 否则我们需要向用户获取权限
	  else if (Notification.permission !== "denied") {
	    Notification.requestPermission().then(function (permission) {
	      // 如果用户接受权限，我们就可以发起一条消息
	      if (permission === "granted") {
	         var notification = new Notification(title,{"body":body});
	      }
	    });
	  }
	  
}

function load_js(url , callback ){
    var script = document.createElement('script');
	fn = callback || function(){};
    script.type = 'text/javascript';
    script.onload = fn;
    
    console.log("loading js from "+url);

    script.src = url;
    document.getElementsByTagName('head')[0].appendChild(script);
}