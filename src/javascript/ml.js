function linearRegression(y,x){ 
     var lr = {}; 
     var n = y.length; 
     var sum_x = 0; 
     var sum_y = 0; 
     var sum_xy = 0; 
     var sum_xx = 0; 
     var sum_yy = 0; 

     for (var i = 0; i < n; i++) { 

      sum_x += x[i]; 
      sum_y += y[i]; 
      sum_xy += (x[i]*y[i]); 
      sum_xx += (x[i]*x[i]); 
      sum_yy += (y[i]*y[i]); 
     } 

     lr['slope'] = (n * sum_xy - sum_x * sum_y)/(n*sum_xx - sum_x * sum_x); 
     lr['intercept'] = (sum_y - lr.slope * sum_x)/n; 
     lr['r2'] = Math.pow((n*sum_xy - sum_x*sum_y)/Math.sqrt((n*sum_xx-sum_x*sum_x)*(n*sum_yy-sum_y*sum_y)),2); 

     return lr; 
} 

function rolling_sum( a, slid_window){
	
	let n = a.length - slid_window + 1;
	
	let result =  new Array();
	
	delta = 0;
	offset = slid_window - 1
	for (let i=0;i < offset ;i++){
		delta+=a[i];
	}
	
	for(let i = 0; i< n; i++){
		delta += a[ i + offset];
		result[i] = delta;
		delta -= a[i]
	}
	
	return result;
	
}



function rolling_lm(y,x, slid_window){ 
     let lr = {}; 
     let n = y.length- slid_window+1; 
     
     let sum_x = rolling_sum(x,slid_window);
     let sum_y = rolling_sum(y, slid_window);
     let sum_xx = rolling_sum(Array.from(x, a => a*a),slid_window);
     let sum_yy = rolling_sum(Array.from(y, a => a*a),slid_window);
     let sum_xy = rolling_sum(Array.from([...Array(n).keys()], i=> x[i]*y[i]),slid_window)
     

	 
	 let lr_list= new Array();
	 
	 for (let i =0;i<n+1;i++){

	     lr['slope'] = (slid_window * sum_xy[i] - sum_x[i] * sum_y[i])/(slid_window*sum_xx[i] - sum_x[i] * sum_x[i]); 
	     lr['intercept'] = (sum_y[i] - lr.slope * sum_x[i])/slid_window; 
	     lr['r2'] = Math.pow((slid_window*sum_xy[i] - sum_x[i]*sum_y[i])/Math.sqrt((slid_window*sum_xx[i]-sum_x[i]*sum_x[i])*(slid_window*sum_yy[i]-sum_y[i]*sum_y[i])),2);
	     lr_list[i]=lr
	 }

     return lr_list; 
} 