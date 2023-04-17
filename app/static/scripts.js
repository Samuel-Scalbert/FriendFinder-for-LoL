function generateCircleChart(selector, value) {
  const chartConfig = {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [value, 100-value],
        backgroundColor: [
          value > 50 ? 'rgb(220, 106, 245)' : 'rgb(255, 0, 0)',
          'rgba(0,0,0,.05)'
        ],
        borderWidth:0,
        cutout:'85%',
      }]
    },
    options:{
      radius:80,
      rotation:180,
      responsive:false,
       animation:{animateScale:true},

      tooltips:{enabled:false},
       legend:{display:false}
    },

   plugins:[{
     beforeDraw:function(chart){
          const width = chart.width;
          const height = chart.height;
        	const ctx = chart.ctx;

        	ctx.restore();
        	ctx.font='bold 55px sans-serif';
      		ctx.textAlign= 'center';
      		chart.ctx.fillStyle="white";

        	 ctx.fillText(value.toString(),width/2,height/2+10);

  	 },
   }]

 };

const ctx = document.querySelector(selector);

new Chart(ctx.getContext('2d'),chartConfig);

}
