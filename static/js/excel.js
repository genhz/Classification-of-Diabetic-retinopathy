var chart = Highcharts.chart('container', {
    data: {
        table: 'datatable'
    },
    // chart: {
    //     type: 'column'
    // },
    // title: {
    //     text: '各类别相似度'
    //     // 该功能依赖 data.js 模块，详见https://www.hcharts.cn/docs/data-modules
    // },
    // yAxis: {
    //     allowDecimals: false,
    //     min: 0,
    //     max: 1,
    //     title: {
    //         text: '',
    //         rotation: 0
    //     }
    // },
    // tooltip: {
    //     formatter: function () {
    //         return '<b>' + this.series.name + '</b><br/>' +
    //             this.point.y + ' 个' + this.point.name.toLowerCase();
    //     }
    // },
    // 	plotOptions: {
	// 	line: {
	// 		dataLabels: {
	// 			enabled: true // 开启数据标签
	// 		}
	// 	}
	// }
chart: {
        type: 'column'
    },
    title: {
        text: '各类别相似率'
    },
    subtitle: {
        text: '点击右边可下载数据'
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        min:0,
        max:1,
        title: {
            text: '概率'
        }
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}%'
            }
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    }
});