
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
	  

	  // 最后，如果执行到这里，说明用户已经拒绝对相关通知进行授权
	  // 出于尊重，我们不应该再打扰他们了
}