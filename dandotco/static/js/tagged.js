// libs
import Vue from 'vue';
import axios from 'axios';

// my stuff
import { bolgTile } from './templates.js';


var 
	bolgs = [],

	bolgListing = {
		props: ['title', 'slug', 'excerpt', 'id', 'body', 'tags'],
		template: bolgTile,
		methods: {
			tileId: function() {
				return 'bolg-' + this.id
			},
			bolgLink: function() {
				return '/bolg/' + this.slug
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
	methods: {
		getTag: function() {
			return this.$el.dataset.tag
		}
	},
	mounted() {
		
		// this.myAttribute = this.$el.getAttribute('data-tag');
		console.log(this.getTag());

		axios
			.get(`/api/tagged/${this.getTag()}`, { crossdomain: false })
			.then(response => (this.bolgs = response.data))
	}
});

