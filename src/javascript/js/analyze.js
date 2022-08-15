
var fday = 3;

function date_filter(date){
	var d = date.date;
	return d.getDay()==fday & d.getDate()>21 & d.getDate()<=28;
	
}

function convert_date(data){
	for (d of data){
		if ("date" in d){
			break;
		}
		d['date']= new Date(d['日期'])
	}
	return data;
	
}

function get_by_week(data,day){
	for (d of data){
		if ("date" in d){
			break;
		}
		d['date']= new Date(d['日期'])
	}
	
	return data.filter(date_filter)
	
}

