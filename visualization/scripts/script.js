function colors_google(n) {
  var colors_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colors_g[n % colors_g.length];
}

var height = 400,
	width = 400,
	radius = 200,
	inradius = 100;

var tempColor;

var mimetype = {
    "application/atom+xml": "2984",
    "application/dita+xml; format=concept": "345",
    "application/epub+zip": "36",
    "application/fits": "24",
    "application/gzip": "2060",
    "application/java-vm": "1",
    "application/msword": "244",
    "application/octet-stream": "211687",
    "application/ogg": "26",
    "application/pdf": "44658",
    "application/postscript": "219",
    "application/rdf+xml": "1042",
    "application/rss+xml": "8894",
    "application/rtf": "53",
    "application/vnd.google-earth.kml+xml": "298",
    "application/vnd.ms-excel": "227",
    "application/vnd.ms-excel.sheet.4": "1",
    "application/vnd.ms-htmlhelp": "1",
    "application/vnd.oasis.opendocument.presentation": "1",
    "application/vnd.oasis.opendocument.text": "10",
    "application/vnd.rn-realmedia": "105",
    "application/vnd.sun.xml.writer": "1",
    "application/x-7z-compressed": "2",
    "application/x-bibtex-text-file": "13",
    "application/x-bittorrent": "3",
    "application/x-bzip": "6",
    "application/x-bzip2": "63",
    "application/x-compress": "44",
    "application/x-debian-package": "4",
    "application/x-elc": "324",
    "application/x-executable": "35",
    "application/x-font-ttf": "9",
    "application/x-gtar": "46",
    "application/x-hdf": "41",
    "application/x-java-jnilib": "5",
    "application/x-lha": "2",
    "application/x-matroska": "66",
    "application/x-msdownload": "72",
    "application/x-msdownload; format=pe": "1",
    "application/x-msdownload; format=pe32": "16",
    "application/x-msmetafile": "6",
    "application/x-rar-compressed": "1",
    "application/x-rpm": "3",
    "application/x-sh": "5680",
    "application/x-shockwave-flash": "141",
    "application/x-sqlite3": "1",
    "application/x-stuffit": "1",
    "application/x-tar": "37",
    "application/x-tex": "17",
    "application/x-tika-msoffice": "2809",
    "application/x-tika-ooxml": "1775",
    "application/x-xz": "11",
    "application/xhtml+xml": "385751",
    "application/xml": "21000",
    "application/xslt+xml": "7",
    "application/zip": "3762",
    "audio/basic": "54",
    "audio/mp4": "18",
    "audio/mpeg": "646",
    "audio/vorbis": "5",
    "audio/x-aiff": "10",
    "audio/x-flac": "2",
    "audio/x-mpegurl": "1",
    "audio/x-ms-wma": "55",
    "audio/x-wav": "59",
    "image/gif": "40049",
    "image/jpeg": "85879",
    "image/png": "37997",
    "image/svg+xml": "342",
    "image/tiff": "477",
    "image/vnd.adobe.photoshop": "4",
    "image/vnd.dwg": "3",
    "image/vnd.microsoft.icon": "1570",
    "image/x-bpg": "7",
    "image/x-ms-bmp": "59",
    "image/x-xcf": "1",
    "message/rfc822": "182",
    "message/x-emlx": "1",
    "text/html": "739588",
    "text/plain": "137335",
    "text/troff": "2",
    "text/x-diff": "1",
    "text/x-jsp": "3",
    "text/x-perl": "14",
    "text/x-php": "25",
    "text/x-python": "5",
    "text/x-vcard": "19",
    "video/mp4": "675",
    "video/mpeg": "255",
    "video/quicktime": "954",
    "video/x-flv": "13",
    "video/x-m4v": "203",
    "video/x-ms-asf": "26",
    "video/x-ms-wmv": "139",
    "video/x-msvideo": "96",
    "xscapplication/zip": "85"
}
var piedata = [];
JSON.parse(JSON.stringify(mimetype),function(k,v){
	var mimedata = {
		"name": k,
		"value": v
	}
	piedata.push(mimedata);	
})
display_data(piedata);

function display_data(piedata)
{
  
    var pie = d3.layout.pie()
    			.value(function(d){
    				return d.value;
    			})

    var arc = d3.svg.arc()
    			.outerRadius(radius)

    var color = d3.scale.category10();

    var info = d3.select('#analysis').append('div')
                    .style('position','absolute')
                    .style('padding','0 10px')
                    .style('background','white')
                    .style('color','black')
                    .style('opacity',0)

    var tooltip = d3.select('#chart').append('div')
    				.style('position','absolute')
    				.style('padding','0 10px')
    				.style('background','white')
    				.style('color','black')
    				.style('opacity',0)

    var mychart = d3.select("#chart").append('svg')
    	.attr('width', width)
    	.attr('height',height)
    	.append('g')
    	.attr('transform','translate('+ (width-radius )+','+ (height -radius) +')')
    	.selectAll('path').data(pie(piedata))
    	.enter()
    		.append('path')
    		.attr('fill',function(d,i){
    			return colors_google(i);	
    		})
    		.attr('d',arc)
    		.on('mouseover',function(d){
    			tooltip.transition()
    				.style('opacity',0.9)
    			tooltip.html(d.data.name+','+d.data.value)
    				.style('left',d3.event.pageX +'px')
    				.style('top',d3.event.pageY+'px')
                info.transition()
                    .style('opacity',0.9)
                info.html("Total no of "+d.data.name+" files = "+d.data.value)
    			tempColor = this.style.fill;
    			d3.select(this)
    				.style('opacity',0.8)
    		})
    		.on('mouseout',function(d){
    			d3.select(this)
    				.style('opacity',1)
    				.style('fill',tempColor)
    		});
}