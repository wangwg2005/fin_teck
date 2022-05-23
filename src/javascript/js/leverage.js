var template = 'https://datacenter-web.eastmoney.com/api/data/get?callback=rzrq_callback&type=RPTA_WEB_RZRQ_GGMX&sty=ALL&source=WEB&st=date&sr=-1&p={pageNo}&ps=50&filter=(scode%3D%22{sid}%22)&pageNo={pageNo}&_=1644393510392';

// DATE: "2022-05-09 00:00:00"    日期
// FIN_BALANCE_GR: -1.971953863237
// KCB: 0
// MARKET: "融资融券_深证"
// RCHANGE3DCP: 0.8242
// RCHANGE5DCP: -0.2717
// RCHANGE10DCP: -20.5628
// RQCHL: 0                融券偿还量
// RQCHL3D: 2900
// RQCHL5D: 6100
// RQCHL10D: 52700
// RQJMG: 0                 融券净卖出（股）
// RQJMG3D: -900
// RQJMG5D: 5600
// RQJMG10D: -35600
// RQMCL: 0					融券卖出量
// RQMCL3D: 2000
// RQMCL5D: 11700
// RQMCL10D: 17100
// RQYE: 22020				融券余额
// RQYL: 6000				带着余量（股）
// RZCHE: 4077362           融资净偿还额
// RZCHE3D: 7305984
// RZCHE5D: 13014271
// RZCHE10D: 52199116
// RZJME: -2143807          融资净买入额
// RZJME3D: 3264909
// RZJME5D: 7602578
// RZJME10D: 9371231
// RZMRE: 1933555    		融资买入额
// RZMRE3D: 10570893
// RZMRE5D: 20616849
// RZMRE10D: 61570347
// RZRQYE: 106593079            融资融券余额
// RZRQYECZ: 106549039			融资融券差值
// RZYE: 106571059				融资余额
// RZYEZB: 3.07811901
// SCODE: "000850"
// SECNAME: "华茂股份"
// SECUCODE: "000850.SZ"
// SPJ: 3.67                   收盘价
// SZ: 3462213727.29
// TRADE_MARKET: "深交所主板"
// TRADE_MARKET_CODE: "069001002001"
// ZDF: 1.9444                 收盘价涨跌幅 





var rzrq_data = {};	

function rzrq_callback(data){
	rzrq_data.values.push.apply(rzrq_data.values,data.result.data);	
}


function check(days,cb){
	console.log(`data length:${rzrq_data.length}`);
	
	if (rzrq_data.values.length>= days){
		rzrq_data.values.sort((a,b)=>new Date(a.DATE) - new Date(b.DATE));
		try{
			localStorage.setItem(rzrq_data.values[0].SCODE,JSON.stringify(rzrq_data));
		}catch(error){
			localStorage.clear();
			localStorage.setItem(rzrq_data.values[0].SCODE,JSON.stringify(rzrq_data));
		}
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

	
