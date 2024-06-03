  var chart = new ApexCharts(document.querySelector("#myChart"), options);
   chart.render();

   var data2 = {{ data2|tojson }};
   var options = {
     series: data2.data,
     chart: {
     width: 500,
     type: 'donut',
     dropShadow: {
       enabled: true,
       color: '#111',
       top: -1,
       left: 3,
       blur: 3,
       opacity: 0.2
     }
   },
   stroke: {
     width: 0,
   },
   plotOptions: {
     pie: {
       donut: {
         labels: {
           show: true,
           total: {
             showAlways: true,
             show: true
           }
         }
       }
     }
   },
   labels:data2.labels,
   dataLabels: {
     dropShadow: {
       blur: 3,
       opacity: 0.8
     }
   },
   fill: {
   type: 'pattern',
     opacity: 1,
     pattern: {
       enabled: true,
       style: ['verticalLines', 'squares', 'horizontalLines', 'circles','slantedLines'],
     },
   },
   states: {
     hover: {
       filter: 'none'
     }
   },
   theme: {
     palette: 'palette2'
   },
   title: {
     text: " Productos con mayor Stock"
   },
   responsive: [{
     breakpoint: 480,
     options: {
       chart: {
         width: 200
       },
       legend: {
         position: 'bottom'
       }
     }
   }]
   };

   var chart = new ApexCharts(document.querySelector("#mychart2"), options);
   chart.render();


   var data3 = {{ data3|tojson }};

   var options = {
     series: [{
     data: data3.data}],
     chart: {
     type: 'bar',
     height: 380
   },
   plotOptions: {
     bar: {
       barHeight: '100%',
       distributed: true,
       horizontal: true,
       dataLabels: {
         position: 'bottom'
       },
     }
   },
   colors: ['#33b2df', '#546E7A', '#d4526e', '#13d8aa', '#A5978B', '#2b908f', '#f9a3a4', '#90ee7e'
   ],
   dataLabels: {
     enabled: true,
     textAnchor: 'start',
     style: {
       colors: ['#fff']
     },
     formatter: function (val, opt) {
       return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
     },
     offsetX: 0,
     dropShadow: {
       enabled: true
     }
   },
   stroke: {
     width: 1,
     colors: ['#fff']
   },
   xaxis: {
     categories: data3.labels,
   },
   yaxis: {
     labels: {
       show: false
     }
   },
   title: {
       text: 'Proveedores',
       align: 'center',
       floating: true
   },
   subtitle: {
       text: 'Proveedores destacados de la tienda',
       align: 'center',
   },
   tooltip: {
     theme: 'dark',
     x: {
       show: false
     },
     y: {
       title: {
         formatter: function () {
           return ''
         }
       }
     }
   }
   };

   var chart = new ApexCharts(document.querySelector("#myChart"), options);
   chart.render();
 
 /*
     // Obtener los datos pasados desde Flask
    var data =  data|tojson ;
         
    // Configurar opciones de la gráfica
    var options = {
     series: [{
     name: 'Nombre',
     data: data.data
   }],
     annotations: {
     points: [{
       x: 'Bananas',
       seriesIndex: 0,
       label: {
         borderColor: '#775DD0',
         offsetY: 0,
         style: {
           color: '#fff',
           background: '#775DD0',
         },
         text: '',
       }
     }]
   },
   chart: {
     height: 350,
     type: 'bar',
   },
   plotOptions: {
     bar: {
       borderRadius: 10,
       columnWidth: '50%',
     }
   },
   dataLabels: {
     enabled: false
   },
   stroke: {
     width: 2
   },
   
   grid: {
     row: {
       colors: ['#fff', '#f2f2f2']
     }
   },
   xaxis: {
     labels: {
       rotate: -45
     },
     categories: data.labels,
     tickPlacement: 'on'
   },
   yaxis: {
     title: {
       text: 'Productos mas vendidos',
     },
   },
   fill: {
     type: 'gradient',
     gradient: {
       shade: 'light',
       type: "horizontal",
       shadeIntensity: 0.25,
       gradientToColors: undefined,
       inverseColors: true,
       opacityFrom: 0.85,
       opacityTo: 0.85,
       stops: [50, 0, 100]
     },
   }
   }; */
