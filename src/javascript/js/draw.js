
function draw_k_line_2(con_id,data,title,kline){

	var dom = document.getElementById(con_id);
	var myChart = echarts.init(dom);
	var option = null;
	var upColor = '#ec0000';
	var upBorderColor = '#8A0000';
	var downColor = '#00da3c';
	var downBorderColor = '#008F28';
	
	document.title = title;

	var category_data = Array.from(kline,a => a[0])
	var kline_data = Array.from(kline ,a => [a[1],a[2],a[4],a[3]]);
	
	
	var pred={};
// 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
	
	
	option = {
	    title: {
	        text: title,
	        left: 0
	    },
	    tooltip: {
	        trigger: 'axis',
	        axisPointer: {
	            type: 'cross'
	        }
	    },
	    legend: {
	        data: ['日K']
	    },
	    grid: {
	        left: '10%',
	        right: '10%',
	        bottom: '15%'
	    },
	    xAxis: {
	        type: 'category',
	        data: category_data,
	        scale: true,
	        boundaryGap: false,
	        axisLine: {onZero: false},
	        splitLine: {show: false},
	        splitNumber: 20,
	        min: 'dataMin',
	        max: 'dataMax'
	    },
	    yAxis: {
	        scale: true,
	        splitArea: {
	            show: true
	        }
	    },
	    dataZoom: [
	        {
	            type: 'inside',
	            start: 50,
	            end: 100
	        },
	        {
	            show: true,
	            type: 'slider',
	            top: '90%',
	            start: 50,
	            end: 100
	        }
	    ],
	    series: [
	        {
	            name: '日K',
	            type: 'candlestick',
	            data: kline_data,
	            itemStyle: {
	                color: upColor,
	                color0: downColor,
	                borderColor: upBorderColor,
	                borderColor0: downBorderColor
	            },
	            markPoint: {
	                label: {
	                    normal: {
	                        formatter: function (param) {
	                            return param != null ? param.value.toFixed(2) : '';
	                        }
	                    }
	                },
	                data: [
	                   
	                    {
	                        name: 'highest value',
	                        type: 'max',
	                        valueDim: 'highest'
	                    },
	                    {
	                        name: 'lowest value',
	                        type: 'min',
	                        valueDim: 'lowest'
	                    },
	                    {
	                        name: 'average value on close',
	                        type: 'average',
	                        valueDim: 'close'
	                    }
	                ],
	                tooltip: {
	                    formatter: function (param) {
	                    	console.log(param.data.coord);
	                        return param.name + '<br>' + (param.data.coord.toFixed(2) || '');
	                    }
	                }
	            },
	            markLine: {
	                symbol: ['none', 'none'],
	                data: [
	                    [
	                        {
	                            name: 'from lowest to highest',
	                            type: 'min',
	                            valueDim: 'lowest',
	                            symbol: 'circle',
	                            symbolSize: 10,
	                            label: {
	                                show: false
	                            },
	                            emphasis: {
	                                label: {
	                                    show: false
	                                }
	                            }
	                        },
	                        {
	                            type: 'max',
	                            valueDim: 'highest',
	                            symbol: 'circle',
	                            symbolSize: 10,
	                            label: {
	                                show: false
	                            },
	                            emphasis: {
	                                label: {
	                                    show: false
	                                }
	                            }
	                        }
	                    ],
	                    {yAxis:6700},
	                    {
	                        name: 'min line on close',
	                        type: 'min',
	                        valueDim: 'close'
	                    },
	                    {
	                        name: 'max line on close',
	                        type: 'max',
	                        valueDim: 'close'
	                    }
	                ]
	            }
	        }

	    ]
	};
	
	for(let key in data){
		option.legend.data.push(key);
		option.series.push({
	            name: key,
	            type: 'line',
	            data: data[key],
	            smooth: true,
	            lineStyle: {
	                opacity: 1
	            }
	        });
		
	}
	
	
	
	
	
	if (option && typeof option === "object") {
	    myChart.setOption(option, true);
	}
	
}


function draw_k_line(con_id,sid){
	
	var m5 = mm[sid];

	var dom = document.getElementById(con_id);
	var myChart = echarts.init(dom);
	var option = null;
	var upColor = '#ec0000';
	var upBorderColor = '#8A0000';
	var downColor = '#00da3c';
	var downBorderColor = '#008F28';
	var data0;
	let sname = price[sid]["data"][sid]["qt"][sid][1];
	
	current_price = m5[m5.length-1][2];
	
	document.title = sname+'-'+sid+":"+current_price;

	var category_data = Array.from(m5,a => a[0])
	var kline_data = Array.from(m5 ,a => [a[1],a[2],a[4],a[3]]);
	
	var pred={};
	
	pred[5] = data[sid+'_5'];
	pred[10] = data[sid+'_10'];
// 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
	
	

	

	option = {
	    title: {
	        text: sname+':'+current_price,
	        left: 0
	    },
	    tooltip: {
	        trigger: 'axis',
	        axisPointer: {
	            type: 'cross'
	        }
	    },
	    legend: {
	        data: ['日K', 'MA5_upper', 'MA5_lower', 'MA10_upper', 'MA10_lower']
	    },
	    grid: {
	        left: '10%',
	        right: '10%',
	        bottom: '15%'
	    },
	    xAxis: {
	        type: 'category',
	        data: category_data,
	        scale: true,
	        boundaryGap: false,
	        axisLine: {onZero: false},
	        splitLine: {show: false},
	        splitNumber: 20,
	        min: 'dataMin',
	        max: 'dataMax'
	    },
	    yAxis: {
	        scale: true,
	        splitArea: {
	            show: true
	        }
	    },
	    dataZoom: [
	        {
	            type: 'inside',
	            start: 50,
	            end: 100
	        },
	        {
	            show: true,
	            type: 'slider',
	            top: '90%',
	            start: 50,
	            end: 100
	        }
	    ],
	    series: [
	        {
	            name: '日K',
	            type: 'candlestick',
	            data: kline_data,
	            itemStyle: {
	                color: upColor,
	                color0: downColor,
	                borderColor: upBorderColor,
	                borderColor0: downBorderColor
	            },
	            markPoint: {
	                label: {
	                    normal: {
	                        formatter: function (param) {
	                            return param != null ? param.value.toFixed(2) : '';
	                        }
	                    }
	                },
	                data: [
	                   
	                    {
	                        name: 'highest value',
	                        type: 'max',
	                        valueDim: 'highest'
	                    },
	                    {
	                        name: 'lowest value',
	                        type: 'min',
	                        valueDim: 'lowest'
	                    },
	                    {
	                        name: 'average value on close',
	                        type: 'average',
	                        valueDim: 'close'
	                    }
	                ],
	                tooltip: {
	                    formatter: function (param) {
	                    	console.log(param.data.coord);
	                        return param.name + '<br>' + (param.data.coord.toFixed(2) || '');
	                    }
	                }
	            },
	            markLine: {
	                symbol: ['none', 'none'],
	                data: [
	                    [
	                        {
	                            name: 'from lowest to highest',
	                            type: 'min',
	                            valueDim: 'lowest',
	                            symbol: 'circle',
	                            symbolSize: 10,
	                            label: {
	                                show: false
	                            },
	                            emphasis: {
	                                label: {
	                                    show: false
	                                }
	                            }
	                        },
	                        {
	                            type: 'max',
	                            valueDim: 'highest',
	                            symbol: 'circle',
	                            symbolSize: 10,
	                            label: {
	                                show: false
	                            },
	                            emphasis: {
	                                label: {
	                                    show: false
	                                }
	                            }
	                        }
	                    ],
	                    {yAxis:6700},
	                    {
	                        name: 'min line on close',
	                        type: 'min',
	                        valueDim: 'close'
	                    },
	                    {
	                        name: 'max line on close',
	                        type: 'max',
	                        valueDim: 'close'
	                    }
	                ]
	            }
	        },
	        {
	            name: 'MA5_upper',
	            type: 'line',
	            data: pred[5]['upper'],
	            smooth: true,
	            lineStyle: {
	                opacity: 1
	            }
	        },
	        {
	            name: 'MA5_lower',
	            type: 'line',
	            data: pred[5]["lower"],
	            smooth: true,
	            lineStyle: {
	                opacity: 1
	            }
	        },
	        {
	            name: 'MA10_upper',
	            type: 'line',
	            data: pred[10]["upper"],
	            smooth: true,
	            lineStyle: {
	                opacity: 1
	            }
	        },
	        {
	            name: 'MA10_lower',
	            type: 'line',
	            data: pred[10]["lower"],
	            smooth: true,
	            lineStyle: {
	                opacity: 1
	            }
	        }

	    ]
	};
	
	
	
	
	
	if (option && typeof option === "object") {
	    myChart.setOption(option, true);
	}
	
}


function draw_2y_line(cid,dates,values,title){
	
		
	var dom = document.getElementById(cid);
	var myChart = echarts.init(dom);
	var app = {};

	var option;

	
	const dateList = dates
	//const valueList = values;
	const s = Array.from(values,v =>{ return {
		  type: 'line',
		  showSymbol: false,
	data: v};
		})
	option = {
	  // Make gradient line here
	
	  title: [
		{
		  left: 'center',
		  text: title
		}
	  ],
	  tooltip: {
		trigger: 'axis'
	  },
	  xAxis: [
		{
		  data: dateList
		}
		
	  ],
	  yAxis: [
		{}		
	  ],
	  grid: [
		{
		  bottom: '60%'
		}
	  ],
	  series: s
	  
	};
	
	

	if (option && typeof option === 'object') {
		myChart.setOption(option);
	}

	
}

function draw_gradient_line(cid,dates,values,title){
	
		
	var dom = document.getElementById(cid);
	var myChart = echarts.init(dom);
	var app = {};

	var option;



	// prettier-ignore
	
	const dateList = dates
	//const valueList = values;
	const s = Array.from(values,v =>{ return {
		  type: 'line',
		  showSymbol: false,
	data: v};
		})
	option = {
	  // Make gradient line here
	
	  title: [
		{
		  left: 'center',
		  text: title
		}
	  ],
	  tooltip: {
		trigger: 'axis'
	  },
	  xAxis: [
		{
		  data: dateList
		}
		
	  ],
	  yAxis: [
		{}		
	  ],
	  grid: [
		{
		  bottom: '60%'
		}
	  ],
	  series: s
	  
	};
	
	

	if (option && typeof option === 'object') {
		myChart.setOption(option);
	}

	
}