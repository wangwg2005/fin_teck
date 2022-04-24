var template = 'https://datacenter-web.eastmoney.com/api/data/get?callback=rzrq_callback&type=RPTA_WEB_RZRQ_GGMX&sty=ALL&source=WEB&st=date&sr=-1&p={pageNo}&ps=50&filter=(scode%3D%22{sid}%22)&pageNo={pageNo}&_=1644393510392';

var rzrq_data = {};	

function rzrq_callback(data){
	rzrq_data.values.push.apply(rzrq_data.values,data.result.data);	
}


function check(days,cb){
	console.log(`data length:${rzrq_data.length}`);
	
	if (rzrq_data.values.length>= days){
		rzrq_data.values.sort((a,b)=>new Date(a.DATE) - new Date(b.DATE));
		
		localStorage.setItem(rzrq_data.values[0].SCODE,JSON.stringify(rzrq_data));
		cb.call(null,rzrq_data.values);
	}
}

function fetch_rzrq(sid,days,cb){
	rzrq_data = JSON.parse(localStorage.getItem(sid));
	date_str = new Date().toJSON().substr(0,10);
	if (rzrq_data == null){
		rzrq_data = {'date':date_str,values : []};
	}else{
		if( rzrq_data.date == new Date().toJSON().substr(0,10)){
			cb.call(null,rzrq_data.values);
			return;
		}else{
			rzrq_data.date=date_str;
			rzrq_data.values = [];
		}
	}
	var fsize = 50;
	var url =  template.replace('{sid}',sid);
	
	for ( var i =1 ;i <= Math.ceil(days/fsize) ; i++){
		u = url.replaceAll('{pageNo}',i);
		load_js(u,function(){check(days,cb);});		
	}
	
}

	
