// libs
import Vue from 'vue';
import axios from 'axios';

// my stuff
import { bolgTile } from './templates.js';


var 
	bolgs = [],

	bolgListing = {
		props: ['title', 'perma', 'excerpt', 'id', 'body', 'tags'],
		template: bolgTile,
		methods: {
			tileId: function() {
				return 'bolg-' + this.id
			},
			bolgLink: function() {
				return '/bolg/' + this.perma
			},
			tagLink: function(tag) {
				return '/tagged/' + tag
			}
		}
	};


new Vue({
	el: '#vuecont',
	data: function() {
		return {
			bolgs: null
		}
	},
	components: {
		'bolg-listing': bolgListing
	},
	mounted() {
		axios
			.get('/api', { crossdomain: false })
			.then(response => (this.bolgs = response.data))
	}
});

