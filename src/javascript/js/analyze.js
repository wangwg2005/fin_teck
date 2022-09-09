
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

function continus_date(data){
	var inds = [];
	
	for(let ind in data){
		if (date_filter(data[ind])){
			inds.push(ind);
			// r1.push(data[ind]);
			// r2.push(data[ind+1]);
		}
	}
	console.log(inds);
	var r1 = Array.from(inds, ind => data[ind]);
	var r2 = Array.from(inds, ind => data[ind+1]);
	
	return [r1,r2];
	
}

function get_by_week(data){
	for (d of data){
		if ("date" in d){
			break;
		}
		d['date']= new Date(d['日期'])
	}
	
	return data.filter(date_filter)
	
}

