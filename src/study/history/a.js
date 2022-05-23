/**
 * 
 */

/**
 * 
 */


window.view = 0;
window.like = 0;
window.comments = 0;

window.counter = 0;




//ifeng 

var ifeng_comments={};

function ifeng_comment(did){
	var data = ifeng_comments[did];
	var rep = data.comments;
	if(rep.length < data.count){
		var pnum = rep.length/10 + 1;
		var t_url=`https://comment.ifeng.com/get.php?orderby=uptimes&docUrl=ucms_${did}&format=js&job=1&p=${pnum}&pageSize=10&skey=265d2d&callback=newCommentListCallBack&_=true`;
		load_js(t_url,null);
		return;
	}
	
	
	var source = "凤凰网";
	var title = document.getElementById(did).innerText;
	
	if ( title.indexOf("原文链接")>-1){
		title = document.getElementsByTagName('h4')[0].innerText;
	}
	
	
	var comments = Array.from(rep,c =>[title, source,c.uname,c.comment_date,c.comment_contents,c.uptimes,1].join('\t') );

	navigator.clipboard.writeText(comments.join('\n'));
	alert(`${rep.length} rows copied`);
	
}

exportFunction(ifeng_comment, window, {defineAs:'ifeng_comment'});

function newCommentListCallBack(data){
	console.log("ifeng comment data");
	console.log(data);
	
	
	if(data.count==0){
		return 
	}
	var did = data.comments[0].doc_url.substring(5);
	if (!(did in ifeng_comments)){	
		comments += data.count;
		show_msg();
		
		var did = data.comments[0].doc_url.substring(5);
		ifeng_comments[did] = data;
		
		
		var link = document.getElementById(did);
		
		let txt = link.innerText;
		if(link.innerText.indexOf('原文链接') == -1){
			link = link.parentElement.nextSibling;
			txt = link.innerText;
		}

		link.innerText = txt.replace('0]',`${data.count}]`);
		
		add_subfix(did,function(){ifeng_comment(did)});
	}else{
		var d0 = ifeng_comments[did].comments;
		d0.push.apply(d0,data.comments);
		ifeng_comment(did);
	}
	
}

exportFunction(newCommentListCallBack, window, {defineAs:'newCommentListCallBack'});

function ifeng(link){
	var url = link.href;
	console.log("ifeng url:"+url);
	var ind = url.lastIndexOf("/");
	var did = url.substr(ind+1,11);
	
	link.id = did;
	
	
	add_prefix(did, '[0,0]');
	
	console.log("did of ifeng:"+did);
	var t_url=`https://comment.ifeng.com/get.php?orderby=uptimes&docUrl=ucms_${did}&format=js&job=1&p=1&pageSize=10&skey=265d2d&callback=newCommentListCallBack&_=true`;
	load_js(t_url,null);
	
	
}


// t.10jqka

function jQuery1110023103284317984418_1646209710082(data){
	let result = data['result'];
	let clk = 0;
	let pid = null;
	for(key in result){
		pid = key.split('_')[2];
		clk = result[key];
		
	}
	view += clk;
	add_prefix(pid,`[${clk},0]`)
	show_msg();
	t_jqka_comment(pid);

}

exportFunction(jQuery1110023103284317984418_1646209710082, window, {defineAs:'jQuery1110023103284317984418_1646209710082'});

function t_jqka(link){
	let url = link.href;
	let ind = url.indexOf('pid');
	let pid = url.substr(ind+4,9);
	link.id = pid;
	console.log("pid:"+pid);
	click_url = 'http://bbsclick.10jqka.com.cn/get?field=clicks&inc=1&app=sns&action=get&app=sns&return=jsonp&key=sns_post_{pid}&callback=jQuery1110023103284317984418_1646209710082&_=1646209710083'
	click_url = click_url.replace('{pid}',pid)
	load_js(click_url,null);
	
}

function tjqka_cmt_click(pid){
	var key = 'tjqka'+pid;
	var data = msg_stack[key];
	var rep = data.result.reply;
	console.log(data.result.floor);
	console.log(rep.length);
	if(data.result.floor == rep.length){
		let source = "同顺号";
		let title = document.getElementById(pid).innerText;
		
		if ( title.indexOf("原文链接")>-1){
			title = document.getElementsByTagName('h4')[0].innerText;
		}
		console.log(rep);
		let cmts = rep.flatMap( r => r.subCommentNum > 0 ? [r].concat(r.bereply): [r] );
		console.log(cmts);
		let comments = Array.from(cmts,c =>[title, source,c['nickname'],new Date(c['ctime']*1000).toJSON(),c['content'],0,1].join('\t') );
		console.log(33333);
		navigator.clipboard.writeText(comments.join('\n'));
		alert(`${cmts.length} rows copied`);
	}else{
		//request comments
		t_jqka_comment(pid);
		
	}
	

}
exportFunction(tjqka_cmt_click, window, {defineAs:'tjqka_cmt_click'});


function cb_tjqka_comment(data){
	console.log('cb_tjqka_comment');
	console.log(data);
	var amount = data.result.amount;
	if (amount == 0){
		return
	}
	//comments += amount;
	

	var reps = data.result.reply;
	var pid = reps[0].pid;
	var key = 'tjqka'+pid;
	var cmt_all = null;
	console.log('key:'+key);
	if(key in msg_stack){
		cmt_all = msg_stack[key]
		let all_rep = cmt_all.result.reply;
		all_rep.push.apply(all_rep,data.result.reply);
	}else{
		msg_stack[key] = data;
		comments += amount;

		var link = document.getElementById(pid);
		
		let txt = link.innerText;
		if(link.innerText.indexOf('原文链接') == -1){
			link = link.parentElement.nextSibling;
			txt = link.innerText;
		}

		link.innerText = txt.replace('0]',`${data.count}]`);
		add_subfix(pid,function(){tjqka_cmt_click(pid);});
		show_msg();
		return ;
	}
	
	tjkqa_cmt_click(pid);
}
exportFunction(cb_tjqka_comment, window, {defineAs:'cb_tjqka_comment'});

function t_jqka_comment(pid){
	var url = 'http://t.10jqka.com.cn/api.php?method=newcircle.getCommentFlow&pid={pid}&limit=10&sort=down&return=jsonp&callback=cb_tjqka_comment'
	url = url.replace('{pid}',pid);
	let key = 'tjqka'+pid;
	if (key in msg_stack){
		let comments = msg_stack[key].result.reply;
		url = url+"&cid="+comments[comments.length-1]['id']
	}
	load_js(url,null);
	
}

exportFunction(t_jqka_comment, window, {defineAs:'t_jqka_comment'});

// #neteasy

var easy_comments={};

function neteasy_cmt(did){

	var data = easy_comments[did];
	console.log("neteasy comments");
	console.log(data);
	var comments = data.comments_arr;
	
	if(data.data.newListSize> comments.length){
		var offset = comments.length;
		//var comment_url = `https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/${did}/comments/newList?offset=${offset}&limit=10&showLevelThreshold=70&headLimit=1&tailLimit=2&ibc=jssdk&callback=tool1007874308744320664_1646276981501&_=1646276981502`;
		var comment_url = `https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/${did}/comments/newList?ibc=newspc&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&offset=${offset}&callback=jsonp_1652945935314&_=1652945935315`;
		load_js(comment_url,null);
		return
		
	}
	
	var source = "网易";
	var title = document.getElementById(did).innerText;
	
	if ( title.indexOf("原文链接")>-1){
		title = document.getElementsByTagName('h4')[0].innerText;
	}
	

	// let cmts = rep.flatMap( r => r.subCommentNum > 0 ? [r].concat(r.bereply): [r] );
	// console.log(cmts);
	var rep = Array.from(comments,c =>[title, source,c.user.nickname,c.createTime,c.content,c.vote,1].join('\t') );

	navigator.clipboard.writeText(rep.join('\n'));
	alert(`${rep.length} rows copied`);
		
		
}

exportFunction(neteasy_cmt, window, {defineAs:'neteasy_cmt'});

function jsonp_1652945935314(data){
	if (data.newListSize == 0){
		return 
	}
	
	var postid = null;
	console.log(data)

	
	for(let a in data.comments){
		postid = data.comments[a].postId;
	}
	
	var did = postid.split('_')[0];
	if (!(did in easy_comments)){
		comments += data.newListSize;
		show_msg();
		var obj = {"data" : data};
		easy_comments[did]= obj;
	
		obj['comments_arr']= Array.from(data.commentIds, id=> data.comments[id.split(",").slice(-1)[0]]);
		
		
		

		var link = document.getElementById(did);
		
		let txt = link.innerText;
		if(link.innerText.indexOf('原文链接') == -1){
			link = link.parentElement.nextSibling;
			txt = link.innerText;
		}

		link.innerText = txt.replace('0]',`${data.newListSize}]`);
		
		add_subfix(did,function(){neteasy_cmt(did)});
	}else{
		var cmts = easy_comments[did].comments_arr;
		
		data.commentIds.forEach((item)=>{
			cmts.push(data.comments[item.split(',').slice(-1)[0]]);			
		});
		
	//	console.log()
		neteasy_cmt(did);
	}
	
}

exportFunction(jsonp_1652945935314, window, {defineAs:'jsonp_1652945935314'});

function neteasy(link){
	var url = link.href;
	var ind = url.lastIndexOf('/');
	var did = url.substr(ind+1, 16);
	link.id = did
	
	var comment_url = `https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/${did}/comments/newList?ibc=newspc&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&offset=0&callback=jsonp_1652945935314&_=1652945935315`
	load_js(comment_url,null);
	add_prefix(did,'[0,0]')
	
}






//caixin

function caixin_cmt_cb(id){
	data = window.wrappedJSObject.comment_data;
	if("list" in data){
		cmts = data['list']
		title = data['title']
		source ='财新网'
		comments = Array.from(cmts,c =>[title, source,c['author'],c['createTime'],c['content'],c['spCount'],1].join('\t') );
		navigator.clipboard.writeText(comments.join('\n'));
		alert(comments.length+" rows copied");
	}else{
		console.log("something wrong when fetching caixin comments, unsynced!");
		console.log(data);
	}
}

exportFunction(caixin_cmt_cb, window, {defineAs:'caixin_cmt_cb'});

function caixin_comment(tids){
//	/https://filec.caixin.com/comment-sync/js/100/642/101759642.js?20220302135610
	_tmpstr = tids.substr(-3,3);
	aid ='100';
	
//	link.id = tids;
	count_link = "https://filec.caixin.com/comment-sync/js/"+aid+"/"+_tmpstr+"/"+tids+".js?"+getCCTailString();
	console.log("comment url:"+count_link)
	load_js(count_link,function(){caixin_cmt_cb(tids);});
}

exportFunction(caixin_comment, window, {defineAs:'caixin_comment'});


function caixin_count(id){
//	abc([{"count":4,"tid":101759642}])
	data = window.wrappedJSObject.comment_data;
	cnum = data['count'];
	
	console.log(data);
	
	add_prefix(id,`[0,${cnum}]`);
	tid = data['tid']
	comments += parseInt(cnum);
	if(cnum>0){
		add_subfix(id,function(){caixin_comment(tid);});
	}
	show_msg();
	
}

function getCCTailString(){
	 var myDate = new Date();
	 var mySecond = myDate.getSeconds();
	 var myCY = myDate.getFullYear();
	 var myCM = myDate.getMonth()+1;
	 var myCD = myDate.getDate();
	 var myCH = myDate.getHours();
	 var myCN = myDate.getMinutes();
	 var myCS = mySecond>10?(mySecond-mySecond%10):0;
	 return (""+myCY)+(myCM<10?("0"+myCM):(""+myCM))+(myCD<10?("0"+myCD):(""+myCD))+(myCH<10?("0"+myCH):(""+myCH))+(myCN<10?("0"+myCN):(""+myCN))+(myCS<10?("0"+myCS):(""+myCS));
}


function cls(link){
	// https://www.cls.cn/v2/comment/get_list?app=CailianpressWeb&articleid=721366&os=web&rn=50&sv=7.7.5&sign=431acfb7cc58ab3dc21e2fc7da2c6c8a
	url = link.href;
	console.log("caixin url:"+url);
	ind = url.lastIndexOf("/")
	let tids = url.substr(ind+1,9);
	_tmpstr = url.substr(ind+7,3);
	aid ='100';
	
	link.id = tids;
	count_link = "https://commentnum.caixin.com/comment-sync/js/"+aid+"/"+_tmpstr+"/"+tids+"_count.js?"+getCCTailString();
	console.log("count url:"+count_link)
	load_js(count_link,function(){caixin_count(tids);});
		
}

//jiemian

var jiemian_cmt={};

function search_content(str,start_tag,end_tag){
	var ind0 = str.indexOf(start_tag);
	var ind1 = str.indexOf(end_tag,ind0);
	return str.substring(ind0+start_tag.length,ind1);
}

function jiemian_cmt_parse(raw_data){
	var content = search_content(raw_data,"<p>","</p>");
	var author = search_content(raw_data,"author-name\">","</a>");
	var date = search_content(raw_data,"date\">","</span>");
	var zan_str0 = search_content(raw_data,"赞</a>","</em>");
	var zan = parseInt(search_content(zan_str0,"(",")"));
	
	return {"author":author,"time":date,"content":content,"zan":zan};
	
	
}
function jQuery110205181590232451436_1646189516259(data){
	var cmt_raw = data.rs.split('comment-post').slice(1);
	var comments = Array.from(cmt_raw,jiemian_cmt_parse);
	var id_str = search_content( cmt_raw[1],"addCommentReply",")");
	id_str = search_content(id_str,",",",");
	var cmts = jiemian_cmt[id_str];
	cmts.push.apply(cmts,comments);
	if (data.count >cmts.length){
		jiemia_comment(id_str,cmts.length/10+1);		
	}else{
		var title = document.getElementById(did).innerText;
	
		if ( title.indexOf("原文链接")>-1){
			title = document.getElementsByTagName('h4')[0].innerText;
		}
		var souce = "";
		var rep = Array.from(cmts,c =>[title, source,c.author,c.time,c.content,c.zan,1].join('\t') );

		navigator.clipboard.writeText(rep.join('\n'));
		alert(`${rep.length} rows copied`);
	}
}


function jiemia_comment(aid,pnum=0){
	url ="https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid=${aid}&page=${pnum}&comment_type=1&per_page=10&callback=jQuery110205181590232451436_1646189516259&_=1646189516271";
	load_js(url,null);
}


function jQuery110207437911404529669_1645755126519(data){
	console.log(data);
	cnum = data['tongjiarr']['count']
	lnum = data['tongjiarr']['ding']
	vnum = data['tongjiarr']['hit']
	
	if(!vnum){
		vnum = 0;
	}
	
	if(vnum.lastIndexOf("w")>-1){
		vnum = parseFloat(vnum.substr(0,vnum.length-1))*10000;
	}else{
		vum = parseInt(vnum);
	}
	
	comments += cnum;
	view += vnum;
	like += lnum;
	
	id = msg_stack['jiemian'];
	add_prefix(id,`[${vnum},${cnum}]`);
	add_subfix(id,function(){jiemian_comment(id)})
	show_msg();
}

//https://apiv2.sohu.com/api/topic/load?callback=jQuery1124042227311849443017_1645757027159&page_size=10&topic_source_id=mp_524722504&page_no=1&hot_size=5&media_id=114988&topic_category_id=8&topic_title={title}&topic_url={url}&source_id=mp_524722504&_=1645757027177

exportFunction(jQuery110207437911404529669_1645755126519, window, {defineAs:'jQuery110207437911404529669_1645755126519'});

function jiemian(link){
	url_tmp = 'https://a.jiemian.com/index.php?m=article&a=getArticleP&aid={id}&callback=jQuery110207437911404529669_1645755126519&_=1645755126520'
	url = link.href
	ind = url.lastIndexOf("/");
	var id = url.substr(ind+1,7);
	link.id = id;
	msg_stack['jiemian']=id;
	load_js(url_tmp.replace('{id}',id),null);
	
}



function jsonp_1645687539166(data){
	console.log(data);
	cnum = data["result"]["count"]["show"];
	newsid = data['result']['news']['newsid'].substr(6);
	console.log("newsid:",newsid);
	window.comments +=cnum;
	
	add_prefix(newsid,`[0,${cnum}]`);
	show_msg();
}


exportFunction(jsonp_1645687539166, window, {defineAs:'jsonp_1645687539166'});

function sina(link){
	//https://finance.sina.com.cn/roll/2021-03-27/doc-ikknscsk2447699.shtml
	var cmt_url ='https://comment.sina.com.cn/page/info?version=1&format=json&channel=cj&newsid=comos-{newsid}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&uid=unlogin_user&callback=jsonp_1645687539166&_=1645687539166';
	var url = link.href;
	
	var ind = url.indexOf("doc-i");
	
	if(ind == -1){
		console.log('the sina url does not match pattern , ignore it');
		return ;
	}
	
	var id = url.substr(ind+5,14);
	link.id=id;
	console.log("sina id:"+id);
	query_url = cmt_url.replace("{newsid}",id)
	
	load_js(query_url,null);
	
}

function add_prefix(id,prefix){
	console.log("add prefix for "+id);
	let link = document.getElementById(id);
	
	let txt = "";
	if(link.innerText.indexOf('原文链接') == -1){
		link = link.parentElement.nextSibling;
		txt = link.innerText;
	}else{
		txt='原文链接'
	}

	link.innerText = prefix + txt;
	link.style.color='red';
}


//sohu

function add_subfix(id,cb){
	let link = document.getElementById(id);
	let a = document.createElement('a');
	
	a.innerHTML="提取评论 | ";
	a.onclick=cb;
	a.id='sf'+id;

	link.parentNode.insertBefore(a,link);
	console.log("add_subfix for "+id);
	
}


/**
 * { 
 * 
 * }
 */
sohu_comments={};

function jQuery1124042227311849443017_1645757027159(data){
	var source_id = data['jsonObject']['source_id'];
	var total_pnum = data['jsonObject']['total_page_no'];
	var com_total = sohu_comments[source_id]['comments'];
	com_total.push.apply(com_total,data['jsonObject']['comments']);
	
	console.log("current page:");
	console.log(sohu_comments);
	console.log("total page number:",total_pnum);
	console.log(total_pnum == sohu_comments[source_id]['pnum'])
	if (total_pnum == sohu_comments[source_id]['pnum']){
		delete sohu_comments[source_id];
		console.log("del");
		let link = document.getElementById(source_id);
		title = link.innerText;
		if ( title.indexOf("原文链接")>-1){
			title = document.getElementsByTagName('h4')[0].innerText;
		}		
		source = '搜狐';
		
		comments = Array.from(com_total,comment => [title,source,comment['passport']['nickname'],new Date(comment['create_time']).toJSON(),comment['content'].replaceAll("\n",""),comment['support_count'],1].join('\t'))
		console.log("sohu comments:");
		console.log(comments);
		navigator.clipboard.writeText(comments.join('\n'));
		alert(com_total.length+" rows copied");
		
	} else{
		sohu_comments[souce_id]['pnum'] +=1;
		sohu_cmt(souce_id);
	}
	
}

exportFunction(jQuery1124042227311849443017_1645757027159, window, {defineAs:'jQuery1124042227311849443017_1645757027159'});

function sohu_cmt(id){
	let link = document.getElementById(id);
	
	
	u = link.href;
	ind = url.lastIndexOf('a');
	ids = url.substr(ind+2).split("_");
	
	let source_id = id;
	let media_id = ids[1]
	let title = link.innerText;
	
	if ( title.indexOf("原文链接")>-1){
		title = document.getElementsByTagName('h4')[0].innerText;
	}
	
	
	let pnum =1;
	if (source_id in sohu_comments){
		pnum = sohu_comments[source_id]['pnum'];
	}else{
		sohu_comments[source_id]= {'pnum':pnum,'comments':[]};
	}
	
	
	var url_tmp = 'https://apiv2.sohu.com/api/topic/load?callback=jQuery1124042227311849443017_1645757027159&page_size=10&topic_source_id={source_id}&page_no={pnum}&hot_size=5&media_id={media_id}&topic_category_id=8&topic_title={title}&topic_url={url}&source_id={source_id}&_=1645757027177';
	var url = url_tmp.replace('{title}',title);
	url = url.replaceAll('{source_id}',source_id);
	
	url = url.replace('{media_id}',media_id);
	
	url = url.replace('{url}',u);
	
	url = url.replace('{pnum}',pnum);
	
	
	load_js(url);
	
}

exportFunction(sohu_cmt, window, {defineAs:'sohu_cmt'});

function jQuery1124013150625997824106_1645606580912(data){


	result = data['jsonObject']['result'];
	
	ks = Array.from( Object.keys(result));
	console.log(result);
	ks.forEach(function(k,index){
		
		let j = result[k]['comments']


		comments += j;
		
		let i = msg_stack['sohu'].shift();
		
		view += i;
		if(j>0){
			add_subfix(k,function(){sohu_cmt(k);return false;})
		}
		
		add_prefix(k, `[${i}, ${j}]`)
	});
	
	show_msg();
}

exportFunction(jQuery1124013150625997824106_1645606580912, window, {defineAs:'jQuery1124013150625997824106_1645606580912'});




function jQuery112408639754397897942_1645670484268(vnum){
	console.log("sohu view:"+vnum);
	msg_stack["sohu"].push(vnum);
	
}

exportFunction(jQuery112408639754397897942_1645670484268, window, {defineAs:'jQuery112408639754397897942_1645670484268'});

function sohu(link){
	var url=link.href;
	
	var query_link = 'https://apiv2.sohu.com/api/comment/count?client_id=cyqemw6s1&topic_source_id={source_id}&callback=jQuery1124013150625997824106_1645606580912&_=1645606580913';
//	https://apiv2.sohu.com/api/topic/load?callback=jQuery1124014277987438054995_1645601800477&page_size=10&topic_source_id=mp_457629712&page_no=1&hot_size=5&media_id=639898&topic_category_id=15&topic_title=突发！昔日千亿白马股面临股民集体索赔，中国版集体诉讼开启？公司最新回应&topic_url=https://www.sohu.com/a/457629712_639898&source_id=mp_457629712&_=1645601800484
	var ind = url.lastIndexOf('a');
	var ids = url.substr(ind+2).split("_")
	var source_id = "mp_"+ids[0]
	link.id = source_id;
	
	
	var  view_link = 'https://v2.sohu.com/public-api/articles/{source_id}/pv?callback=jQuery112408639754397897942_1645670484268&_=1645670484269';
	var view_link = view_link.replace("{source_id}",ids[0]);
	
	query_link = query_link.replace('{source_id}',source_id);
	
	load_js(view_link,function(){load_js(query_link)});
	
	
	
}

function load_js(url,cb){
	console.log("loading js from "+ url);

	 var hm = document.createElement("script");
	 hm.src = url;
	 fn = cb || function(){};
	 hm.type = 'text/javascript';
	 hm.onload = fn;
	 document.getElementsByTagName('head')[0].appendChild(hm);
}

function show_msg(){
	console.log('view='+view+',like='+like+',comments='+comments);
	let su = document.getElementById('sumup');
	su.innerText = `汇总 [${view}, ${comments}]`;
	navigator.clipboard.writeText([view,comments].join('\t'));
}

msg_stack={};
msg_stack["sohu"] = [];

function showFace(m){
    var o = 0;

    for (const [e, t] of Object.entries(m)) {
    	if ("result" !== e) {
            2 == e.split("|")[0] && (o = t)
        }
    }
    
    var i = o * o + 5;
    o > 10 && (i = 10 * o + 5),
    o > 50 && (i = 5 * o + 255),
    o > 100 && (i = 2 * o + 555),
    
    msg_stack["jqka_like"]=i;

   
    window.like += i;

	ind = url.lastIndexOf('c');
	let nid=url.substr(ind+1,9);
	
	add_prefix(pid, `[${clk_cnt}, ${cmt_cnt}]`)
	
    show_msg();
}

var jqka_id =new Set();

// function jqka_postpross(id){
	// console.log("jqka id"+id);
	// if(jqka_id.has(id)){
		// return
	// }
	// jqka_id.add(id);
	// console.log(id);

	
	// cnum=msg_stack['jqka_cnum'];
	
	// if (!cnum){
		// cnum = 0;
	// }
	// like = msg_stack['jqka_like'];
	
	// console.log("jqka cnum:"+cnum);
	// console.log("jqka like:"+like);
	
	
	// add_prefix(id,`[0, ${cnum}]` );

	
// }


// exportFunction(showFace, window, {defineAs:'showFace'});

function formate_date(date){
	var s=date.getFullYear()+"";
	var m=date.getMonth()+1;
	if (m<10){
		s+="0";
	}

	s += m;
	
	
	var d=date.getDate();
	
	if (d<10){
		s+="0";
	}
	
	s += d;
	
	var hour =  date.getHours();
	if( hour < 10 ){
		s += 0;
	}
	s += hour;
	
	var minu = date.getMinutes();
	
	if( minu < 10 ){
		s += 0;
	}
	
	s += minu;
	
	console.log("date str:"+s);
	
	return s;
	
}

function loadMoreComment(data){
	console.log("more comment for jqka");
	console.log(data);
	
	if(data.result == null){
		jqka_comment();
	}
	
	var replies = data['result']['reply'];
	var pid = replies[replies.length -1]['pid'];
	
	var key = 'jqka'+pid;
	
	console.log(msg_stack[key]);
	var reps = msg_stack[key]['result']['reply'];
	for (rep of replies){
		reps.push(rep);
		rep['lev'] = 1;
			if('bereply' in rep){
				for(berep of rep['bereply']){
					berep['lev']=2;
					reps.push(berep);
				}
			}
	}
	
	load_comment_like(pid);

}

exportFunction(loadMoreComment, window, {defineAs:'loadMoreComment'});


function jQuery183044525564682981034_1646379322252(data){
	var likes = data['result'];
	console.log("jqka comment likes");
	console.log(data);
	var obj = null;
	var pid = null;
	for(key in likes){
		let keys = key.split('_');
		if(obj == null){
			obj = msg_stack['jqka'+keys[0]]['result']['reply'];
			pid = keys[0];
		}
		let rep = obj.filter(a => a['id']==keys[1]);
		rep[0]['likes'] = likes[key];	
	}
	
	console.log(obj);
	
	jqka_comment(pid);
}

exportFunction(jQuery183044525564682981034_1646379322252, window, {defineAs:'jQuery183044525564682981034_1646379322252'});


function load_comment_like(pid){
	let data = msg_stack['jqka'+pid];
	let replies = data['result']['reply'];
	console.log("loading likes for comment : replies");
	console.log(replies);
	let keys = Array.from(replies.filter(a=> !('likes' in a)),rep=>rep['likeskey']).join(',');
	let url = 'http://bbsclick.10jqka.com.cn/getlist?app=sns&field=likes&key={ids}&log=0&callback=jQuery183044525564682981034_1646379322252&_=1646379329746'
	url = url.replace("{ids}",keys);
	load_js(url,null);
}

exportFunction(load_comment_like, window, {defineAs:'load_comment_like'});

function jqka_comment(pid){
	
	var key = 'jqka'+pid;
	if(!(key in msg_stack)){
		return;
	}
	
	var data = msg_stack[key];

	var cnum = data['info']['cnum'];
	var replies = data['result']['reply'];
	var rep_len = replies.length;

	
	console.log("cnum:"+cnum);
	console.log("current comments:"+rep_len);
	if(cnum > rep_len && rep_len %5 == 0){
		let cid = 0;
		for(let i = rep_len-1; i>0; i--){
			if (replies[i]['lev'] ==1){
				cid = replies[i]['id'];
				break;
			}
		}		
		let url = 'http://t.10jqka.com.cn/api.php?method=newcircle.getCommentFlow&pid={pid}&cid={cid}&limit=10&sort=down&return=jsonp&callback=loadMoreComment'
		url = url.replace('{pid}',pid);
		url = url.replace('{cid}',cid);
		load_js(url,null);
		return;
	}
	console.log(data['info']['tid']);
	let link = document.getElementById( data['info']['tid']);
	let title = link.innerText;
	if ( title.indexOf("原文链接")>-1){
		title = document.getElementsByTagName('h4')[0].innerText;
	}
	let source = '同花顺';
	let comments = Array.from(replies, rep => [title, source, rep['nickname'],new Date(parseInt(rep['ctime'])*1000).toJSON(),rep['content'],rep['likes'],rep['lev']].join('\t'));
	navigator.clipboard.writeText(comments.join('\n'));
	alert(rep_len +" rows comments copied");
}

exportFunction(jqka_comment, window, {defineAs:'jqka_comment'});

var jqka_seq=new Set();

//jqka
function getHotCommentList(data){
	var cnum = 0;
	
	if (!data){
		console.log("no comment jqka");
		msg_stack["jqka_cnum"]=0;
	}else{
	
		let seq = data['info']['seq'];
		
		
		if(jqka_seq.has(seq)){
			return
		}
		
		jqka_seq.add(seq)
		

		
		console.log("jqka comment list");
		console.log(data);
		msg_stack["jqka_cnum"] = data['info']['cnum'];
		cnum = data['info']['cnum'];
		let pid =data['info']['tid'];
		
		let reps = [];
		let replies = data['result']['reply'];
		
		for(rep of replies){
			reps.push(rep);
			rep['lev'] = 1;
			if('bereply' in rep){
				for(berep of rep['bereply']){
					berep['lev']=2;
					reps.push(berep);
				}
			}
		}
	
		console.log('seq:'+seq);
		let link = document.getElementById(seq);
		link.id = pid;
		if(cnum>0){
			add_subfix(pid,function(){load_comment_like(pid);});
		}
		
	
		let txt = link.innerText;
		if(link.innerText.indexOf('原文链接') == -1){
			link = link.parentElement.nextSibling;
			txt = link.innerText;
		}

		link.innerText = txt.replace('0]',`${cnum}]`);
		
		
		msg_stack['jqka'+pid]={'info':data['info'],'result':{'reply':reps}};
	}
	
	comments += cnum;
	
	show_msg();
}



function jqka(link){
	
	url = link.href;
	
	
	console.log('jqka:'+url);
	ind = url.lastIndexOf('/');
	
	if(url.substr(ind+1,1)=='c'){
		ind +=1;
	}
	
	
	var nid=url.substr(ind+1,9);
	
	link.id = nid;
	
	add_prefix(nid,'[0,0]');
	
	
	var ARTINFO = {
			seq: nid,
			tday: formate_date(new Date()),
			pid: '',
			userid: '',
			cid: ''  //最后一条评论的ID
		};

	
	let u1='http://comment.10jqka.com.cn/hotcommentv2/' + ARTINFO.seq.substring(0, 3) + '/' + ARTINFO.seq + '.' + ARTINFO.tday + '.txt';
	console.log('requesting:'+u1);
	load_js(u1,null);
	
	// let u2= 'http://comment.10jqka.com.cn/faceajax.php?type=add&jsoncallback=showFace&faceid=2&seq=' + ARTINFO.seq;
	// console.log('requesting:'+u1);
	// load_js(u2,function(){jqka_postpross(nid);});
		
}


function eastmoney(link){
	url = link.href;
	console.log("eastmoney:"+url)
	let pid=url.substr(url.length-23,18);
	link.id =  pid;
	let u1='https://gbapi.eastmoney.com/abstract/api/PostShort/NewsArticleBriefInfo?postid={pid}&type=1&version=80008000&product=guba&plat=web&deviceid=0d2798cab1716439a343c9965c20c59d&callback=emcb&_=1643013450740'
	u1=u1.replace('{pid}',pid)
	load_js(u1);
}

function emcb(data){
	console.log(data);
	let re=data['re'][0];
	
	let pid = re['post_sourceid_id'];
	
	
	let cmt_cnt = re['post_comment_count'];
	let clk_cnt = re['post_click_count'];
	let like_cnt = re['post_like_count'];

	
	
	comments += cmt_cnt;
	view += clk_cnt;
	like += like_cnt;
	
	add_prefix(pid, `[${clk_cnt}, ${cmt_cnt}]`)
	
//	let link = document.getElementById(pid);
//	
//	if(link.innerText.indexOf('原文链接') == -1){
//		link = link.parentElement.nextSibling;
//	}
//	
//	link.innerText = `[${clk_cnt}, ${cmt_cnt}]` +link.innerText;
//	link.style.color='red';
	
	
	show_msg();
}

exportFunction(emcb, window, {defineAs:'emcb'});

exportFunction(getHotCommentList, window, {defineAs:'getHotCommentList'});

var urls = new Set();

function classify(link){
	var url = link.href;
	
	// var ind = url.indexOf('?');
	// var key = url;
	// if(ind>-1){
		// key = url.substring(0,ind);
	// }
	// if( urls.has(key)){
		// console.log("replicated url:"+url);
		// let t = link.parentElement.nextSibling;
		// t.innerText = '重复已忽略|' +t.innerText;
		// t.style.color='yellow';
		// return;
		
	// }else{
		// urls.add(key);
	// }
	counter += 1;
	console.log("classify :"+url);
	if ((url.indexOf('news.10jqka.com.cn/')>-1 || url.indexOf('stock.10jqka.com.cn/')>-1 ) && url.indexOf("iphone")<0){
		return jqka(link);
	}else if (url.indexOf('t.10jqka.com.cn')>-1){
		return t_jqka(link);
	}else if(url.indexOf('finance.eastmoney.com/a')>-1 || url.indexOf('stock.eastmoney.com/a')>-1 || url.indexOf('field.10jqka.com.cn')>-1){
		return eastmoney(link);
	}else if(url.indexOf('www.sohu.com')>-1){
		return sohu(link);		
	//}else if(url.indexOf("finance.sina.com.cn/stock")>-1 || url.indexOf("finance.sina.com.cn/roll")>-1){
	}else if(url.indexOf("finance.sina.com.cn") > -1){
		return sina(link);
	}else if (url.indexOf('finance.ifeng.com')>-1){
		return ifeng(link);
	}else if(url.indexOf("www.jiemian.com")>-1){
		return jiemian(link);
	}else if (url.indexOf("www.caixin.com")>-1){
		return cls(link);
	}else if(url.indexOf('www.163.com')>-1){
		return neteasy(link);
	}else{
		counter -= 1;
	}
	
	return null;
}


function get_current_page(){
	let link = document.querySelector('h6 > span > a');
	console.log("current page:"+link.href)
	classify(link);
}


function retrive_msg(){
	
	get_current_page();
	
	let t = document.querySelectorAll('.left > a');
	t.forEach( link => classify(link));
	
	
}

function add_button(){

	let sim = document.getElementsByTagName('h6');
	
	if(sim.length==0){
		console.log("not find similar element");
		return null;
	}
	
	let link = document.createElement('a');
	link.innerText = '汇总';
	link.title = '拷贝评论';
	link.id = 'sumup';
	link.onclick=retrive_msg;
	
	sim[0].appendChild(link);
	console.log("button added");

}


window.addEventListener('load', event => {
	add_button();
});






