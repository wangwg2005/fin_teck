

var codes=['000030.SZ',  '000623.SZ', '000631.SZ', '000661.SZ',  '000686.SZ', '000718.SZ', '000766.SZ', '000800.SZ', '000875.SZ', '000928.SZ', '002118.SZ', '002501.SZ', '600110.SH', '600333.SH', '600360.SH',  '600742.SH',  '600867.SH', '600881.SH',  '601929.SH', '603559.SH']

var i=0;
var counter=codes.length;

var page = require('webpage').create();
page.settings.userAgent ="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
//	page.viewportSize = { width: 1920, height: 1080 };
page.clipRect = { top: 0, left: 0, width: 1200, height: 768 };


function capture(tabInd){
	
}

function download(ind){
	code=codes[ind].substring(0,6)
	page.open('http://data.10jqka.com.cn/market/rzrqgg/code/'+code+"/", function() {
		page.includeJs("https://code.jquery.com/jquery-3.4.1.min.js", function() {
		    
//		    	 page.render(code+'tab1.png');
		    	
		       
		        page.evaluate(function() {
		        	tabs=document.getElementsByClassName("hcharts-tab");
		        	$(tabs[0].children[1]).click();
		        });
		        setTimeout(function() {
			        page.render(code+'tab2.png');
	//		        page.render(code+'tab3.png');
	//		        page.render(code+'tab4.png');
	//		        page.render(code+'tab5.png');
			        ind++;
			        if(ind>=codes.length){
			        	phantom.exit();
			        }else{
			        	download(ind)
			        }
		        
		        }, 3000);
		});
	});
}
download(0)
