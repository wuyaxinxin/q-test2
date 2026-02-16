document.addEventListener('DOMContentLoaded', function() {
    const chartDom = document.getElementById('main-chart');
    const myChart = echarts.init(chartDom);
    
    myChart.showLoading({
        text: '数据加载中...',
        color: '#667eea',
        textColor: '#000',
        maskColor: 'rgba(255, 255, 255, 0.8)',
        zlevel: 0
    });
    
    fetch('/api/trade-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应失败');
            }
            return response.json();
        })
        .then(result => {
            myChart.hideLoading();
            
            if (result.status !== 'success') {
                throw new Error('数据格式错误');
            }
            
            const data = result.data;
            const years = data.years;
            const countries = data.countries;
            
            const colorMap = {
                '中国': '#d62728',
                '美国': '#1f77b4',
                '德国': '#ff7f0e',
                '日本': '#2ca02c',
                '英国': '#9467bd'
            };
            
            const series = [];
            
            Object.keys(countries).forEach(countryName => {
                const countryData = countries[countryName];
                const baseColor = colorMap[countryName] || '#333';
                
                series.push({
                    name: `${countryName}-进口`,
                    type: 'line',
                    data: countryData.import,
                    smooth: true,
                    lineStyle: {
                        width: 2,
                        type: 'solid',
                        color: baseColor
                    },
                    itemStyle: {
                        color: baseColor
                    },
                    emphasis: {
                        focus: 'series'
                    }
                });
                
                series.push({
                    name: `${countryName}-出口`,
                    type: 'line',
                    data: countryData.export,
                    smooth: true,
                    lineStyle: {
                        width: 2,
                        type: 'dashed',
                        color: baseColor
                    },
                    itemStyle: {
                        color: baseColor
                    },
                    emphasis: {
                        focus: 'series'
                    }
                });
            });
            
            const option = {
                title: {
                    text: '全球主要国家进出口总额趋势',
                    left: 'center',
                    textStyle: {
                        fontSize: 18,
                        fontWeight: 'bold',
                        color: '#2c3e50'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    },
                    formatter: function(params) {
                        let result = `<strong>${params[0].axisValue}年</strong><br/>`;
                        params.forEach(param => {
                            result += `${param.marker} ${param.seriesName}: ${param.value.toFixed(2)} 亿美元<br/>`;
                        });
                        return result;
                    }
                },
                legend: {
                    data: series.map(s => s.name),
                    top: 40,
                    type: 'scroll',
                    padding: [5, 5]
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    top: '20%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: years,
                    name: '年份',
                    nameLocation: 'middle',
                    nameGap: 30,
                    axisLine: {
                        lineStyle: {
                            color: '#666'
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '金额 (亿美元)',
                    nameLocation: 'middle',
                    nameGap: 50,
                    axisLine: {
                        lineStyle: {
                            color: '#666'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    }
                },
                dataZoom: [
                    {
                        type: 'slider',
                        start: 0,
                        end: 100,
                        bottom: '5%'
                    },
                    {
                        type: 'inside',
                        start: 0,
                        end: 100
                    }
                ],
                series: series
            };
            
            myChart.setOption(option);
            
            window.addEventListener('resize', function() {
                myChart.resize();
            });
        })
        .catch(error => {
            myChart.hideLoading();
            console.error('数据加载失败:', error);
            
            myChart.setOption({
                title: {
                    text: '数据加载失败',
                    subtext: '请刷新页面重试',
                    left: 'center',
                    top: 'center',
                    textStyle: {
                        color: '#999',
                        fontSize: 20
                    }
                }
            });
        });
});
