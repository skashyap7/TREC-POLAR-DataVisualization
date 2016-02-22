d3.json("viz-all.json",function(data){
	for(var key in data){
		var bardata = [];
		for (var f in data[key])
		{
			bardata.push(data[key][f]);
		}
		show_chart(bardata,key);
	}
});
//for (var i =0;i<50;i++)
//	bardata.push(Math.round(Math.random()*30+10))
function show_chart(bardata,mimetype){
var tempColor;
var height = 400,
	width = 900,
	barwdith = 256,
	baroffset = 5;
var yScale = d3.scale.linear()
			.domain([0,d3.max(bardata)])
			.range([0,height])

var xScale = d3.scale.ordinal()
			.domain(d3.range(0,bardata.length))
			.rangeBands([0,width])
function colors_google(n) {
  var colors_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colors_g[n % colors_g.length];
}

var color = d3.scale.linear()
			.domain([0,bardata.length*0.10,bardata.length*0.20,bardata.length*0.30,bardata.length*0.40,bardata.length*0.50,bardata.length*0.60,bardata.length*0.70,bardata.length*0.80,bardata.length*0.90,bardata.length])
			.range(["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"])

var tooltip = d3.select('body').append('div')
				.style('position','absolute')
				.style('padding','0 10px')
				.style('background','white')
				.style('opacity',0)

var mychart = d3.select("#chart").append('div')
	.attr('class','well')
	.append('svg')
	.attr('width', width)
	.attr('height',height)
	.append('g')
	.selectAll('rect').data(bardata)
	.enter().append('rect')
		.style('fill',function(d,i){
			return color(i)	
		})
		.attr('width',xScale.rangeBand())
		.attr('x',function(d,i){
			return xScale(i);
		})
		.attr('height',0)
		.attr('width', 2)
		.attr('y',height)
		.on('mouseover',function(d){
			tooltip.transition()
				.style('opacity',0.9)
			tooltip.html(d)
				.style('left',d3.event.pageX +'px')
				.style('top',d3.event.pageY+'px')
			tempColor = this.style.fill;
			d3.select(this)
				.style('opacity',0.5)
				.style('fill','yellow')
		})
		.on('mouseout',function(d){
			d3.select(this)
				.style('opacity',1)
				.style('fill',tempColor)
		});
		
		
		
mychart.transition()
	.attr('height',function(d){
			return yScale(d);
		})
	.attr('y',function(d,i){
			return height - yScale(d);
	})
	.duration(1000)
	.ease('elastic')
	.delay(function(d,i){
		return i*10;
	})
}
