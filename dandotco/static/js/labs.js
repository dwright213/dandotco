// import './home'

import Vue from 'vue';
import SVG from 'svg.js';
var LinearScale = require('linear-scale');

import displayComparator from './components/displayComparator'

var 
	benchWidth = 800,
	center = benchWidth/4,
	scale = LinearScale([0,2500], [0,1000]),
	draw = SVG('bolg-holder');



var displays = [
		{
			name: 'Dell Dimension D420',
			aspect: [16, 9],
			diag: 13.3,
			color: 'green',
			id: 1,
			rectid: ''
		},
		{
			name: 'HP Pro Slate 12',
			aspect: [4, 3],
			diag: 12.3,
			color: 'red',
			id: 2,
			rectid: ''
		},
		{
			name: 'iBook Clamshell',
			aspect: [4, 3],
			diag: 12.1,
			color: 'blue',
			id: 3,
			rectid: ''
		}
	];




function inchToMm(inches) {
	return inches * 25.4 * 1.5
}  



var displayComp = new Vue({
	el: '#comparator',
	data: {
		displays: displays,
		rects: []
	},
	
	components: {
		'display-comparator': displayComparator
	},

	methods: {
		shiftDisplays: function(position) {
			console.log(position)
		},

		highlightRect: function(id) {
			SVG.select('rect').attr({stroke: 'none'})
			let screen = SVG.get(id);
			screen
				.attr({stroke: '#000'})
				.front();
		},

		drawDisplays: function() {
			let rects = [];
			this.displays.map((display, index) => {
				let 
					diagSq = Math.pow(display.diag, 2),
					widthSq = Math.pow(display.aspect[0], 2),
					heightSq = Math.pow(display.aspect[1], 2),
					relDiag = Math.sqrt((widthSq + heightSq)),
					width = display.aspect[0]/relDiag * display.diag,
					height = display.aspect[1]/relDiag * display.diag,

					rectangle = draw.rect(inchToMm(width), inchToMm(height))
					.attr({ 
						fill: display.color,
						'fill-opacity': 0.5	
					})
					.move((benchWidth-inchToMm(width))/2, 25);
					display['rectid'] = rectangle.node.id
					rects.push(rectangle)

			})

		}
	},

	mounted() {
		this.drawDisplays()
	}

})



