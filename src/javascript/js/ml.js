function batch_ml(x,y,offset){
	var data_len = x.length;
	var result = new Array(data_len);
	result.fill("-");
	
	var upper =  new Array(data_len);
	upper.fill("-");
	var lower =  new Array(data_len);
	lower.fill("-");
	for (let i = offset ; i< y.length; i++){
		let lr = linearRegression(y.slice(i-offset,i), x.slice(i-offset,i));
		let v = lr['slope'] * x[i] + lr["intercept"];
		
		result[i] = v;
		upper[i] =(v + 2*lr["se"]);
		lower[i] = (v - 2*lr["se"] );
	
	}
	
	return [result,upper,lower];
	
}


function compute_cycle_by_median(a){
	var range = 33;
	
	var arr = a.slice(-range);
	
	var avg = arr.reduce(add)/range;
	arr = Array.from(arr, p => p-avg);
	console.log("latest data");
	console.log(arr);
	var cnt = 0;
	for(let i =1;i<33;i++){
		let m = 0;
		if (arr[i]*arr[i-1]<0){
			m = 1;
		}
		cnt = cnt << 1 | m;
	}
	
	var hcycle = 0;
	
	var ind = 0;
	var lens = new Array();
	while (ind<32){
		let len = 0;
		while((ind+ ++len<32) & !(( cnt>> ind + len)& 1));
		if (ind + len <32){
			lens.push(len);
			
		}
		ind += len+1;		
	}
	
	lens.sort( (a,b)=> b-a);
	console.log(lens);
	if (lens.length ==1){
		return lens[0]*2;
	}else if (lens.length>1){
		return lens[0]+lens[1];
	}else{
		return -1;
	}
	
	
}


function model_by_ci(X,Y, pos , mlen,sigma,ci){
	
	for(let len= mlen;len++; len<X.length){
	
		let start = pos - len + 1;
		
		let x = X.slice(start,len);
		let y = Y.slice(start,len);
		
		let lr = linearRegression(x, y);
		
		
		
	}
	
	
	
}



function compute_cycle_by_max(a){
	var min_cycle = 8;
	var arr = a.slice(-33);
	var origin = a.slice(-33)
	arr.sort();
	var big = arr.slice(0,11)
	console.log("big");
	console.log(big);
	var inds = Array.from(big, v => origin.indexOf(v));
	var lens = new Array();
	console.log(inds);
	// var current_ind= 0;
	// for(let i = 0; i < 11; i++){
		
	// }
	
}

function diff(a, order = 1){
	var len = a.length;
	result = []
	for (let i = order; i<len ;i++){
		result[i-order]=a[i]-a[i-order]
	}
	
	return result
	
}


function linearRegression(y,x){ 
     let lr = {}; 
     let n = y.length; 
     let sum_x = 0; 
     let sum_y = 0; 
     let sum_xy = 0; 
     let sum_xx = 0; 
     let sum_yy = 0; 

     for (var i = 0; i < n; i++) { 

      sum_x += x[i]; 
      sum_y += y[i]; 
      sum_xy += (x[i]*y[i]); 
      sum_xx += (x[i]*x[i]); 
      sum_yy += (y[i]*y[i]); 
     } 

     lr['slope'] = (n * sum_xy - sum_x * sum_y)/(n*sum_xx - sum_x * sum_x); 
     lr['intercept'] = (sum_y - lr.slope * sum_x)/n; 
     
     let y_pred=Array.from(x, x=> x*lr['slope']+lr['intercept'])
     
     let mse=0
     for( let i =0 ;i< n ;i++ ){
    	 mse += Math.pow(y[i]-y_pred[i],2)
    	 
     }
     
     lr['se']= Math.sqrt(mse/n)
     
     
     // lr['r2'] = Math.pow((n*sum_xy - sum_x*sum_y)/Math.sqrt((n*sum_xx-sum_x*sum_x)*(n*sum_yy-sum_y*sum_y)),2); 

     return lr; 
} 

var add = (a,b)=> a+b;


function std(a){	
	var sum_a = a.reduce(add)/a.length;
	
	
	var diff_sqr = Array.from(a,x=> Math.pow(x-sum_a,2));
	var mse = diff_sqr.reduce(add)/a.length;
	return Math.sqrt(mse);
	
}
function rolling_std(a,slide_window){
	var offset = a.length - slide_window +1;
	var stds= new Array();
	for(let i = 0 ;i< offset;i++){
		b = a.slice(i,i+slide_window);
		stds[i] = std(b);
	}
	
	return stds;
	
}

function rolling_mean(a, slid_window){
	var n = a.length - slid_window + 1;
	
	var result =  new Array();
	
	delta = 0;
	offset = slid_window - 1
	for (let i=0;i < offset ;i++){
		delta+=a[i];
	}
	
	for(let i = 0; i< n; i++){
		delta += a[ i + offset];
		result[i] = delta/slid_window;
		delta -= a[i]
	}
	
	return result;
	
}

function rolling_sum( a, slid_window){
	
	let n = a.length - slid_window + 1;
	
	let result =  new Array();
	
	delta = 0;
	offset = slid_window - 1;
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


function compute_x(a){
	if (a[2]-a[1]>0){
		return +a[5];
//	}else if(a[2] == a[1]){
//		return 0;
	}else{
		return -a[5]
	}
}



function calculateValue(m5, day){
	
	x = Array.from(m5, compute_x);
	for(let i =1;i<x.length;i++){
		x[i]=x[i-1]+x[i];
	}
	
	y = Array.from(m5, a=> parseFloat(a[2]));
		
	let slid_window=day*48;
	
	let result=new Array(day*48);
	result.fill("-");
	
	let upper=new Array(day*48);
	upper.fill("-");
	
	let lower=new Array(day*48);
	lower.fill("-");
	
	
	time1 = new Date().getTime();
	for(let i =slid_window; i< 800 ;i++){
		let lr = linearRegression(y.slice(i-slid_window,i), x.slice(i-slid_window,i));
		let v = lr['slope'] * x[i] + lr["intercept"];

		result.push(v);
		upper.push(v + 2*lr["se"]);

		lower.push(v - 2*lr["se"] );
		
	}
	time2 = new Date().getTime();
	time_diff= time2-time1;
	console.log("caculating "+day+" day value costs "+time_diff+"ms");
	
	let t = {"mean":result,"upper":upper,"lower":lower};
	return t;
}