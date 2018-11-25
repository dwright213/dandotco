// libs
import Vue from 'vue';
import axios from 'axios';
import debounce from 'lodash.debounce'



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


var taggart = new Vue({
	el: '#main-container',

	data: {
		bolgs: [],
		searchTag: '',
		searching: false

	},
	computed: {
		hideNoResults() {
			if (this.bolgs.length == 0 && this.searching) {
				return false
			} else {
				return true
			}	
		}
	},

	components: {
		'bolg-listing': bolgListing
	},

	methods: {
		statusCheck: function() {
			if(bolgs.length == 0) {
				taggart.searching = false
			}
		},

		search: debounce((value) => {
			if (value.length > 0){
				axios
					.get(`api/tagged/${value}`, { crossdomain: false })
					.then(response => (taggart.bolgs = response.data.results))
					.catch(function(error){ console.log(error) })

				taggart.searching = true
				
			} else {
				taggart.searching = false
			}
		}, 500)
	},

	mounted() {
	}


})