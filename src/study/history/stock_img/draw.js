
function splitData(rawData) {
    var categoryData = [];
    var values = []
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i])
    }
    return {
        categoryData: categoryData,
        values: values
    };
}



function draw(con_id,sid){

	var dom = document.getElementById(con_id);
	var myChart = echarts.init(dom);
	var option = null;
	var upColor = '#ec0000';
	var upBorderColor = '#8A0000';
	var downColor = '#00da3c';
	var downBorderColor = '#008F28';
	var data0;
	console.log(sdata);
	let sname = sdata["data"][sid]["qt"][sid][1];
	var m5 = sdata["data"][sid]['m5'];
	current_price = m5[m5.length-1][2];
	
	document.title = sname+'-'+sid+":"+current_price;

	var mdata = Array.from(m5 ,a => [a[0],a[1],a[2],a[4],a[3]]);
	data0 = splitData(mdata);
	
	
	
	pred[5] = calculateValue(m5,5);
	pred[10] = calculateValue(m5,10);
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
	        data: data0.categoryData,
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
	            data: data0.values,
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
	                    {yAxis:stock['value']},
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
	notifyMe();
}