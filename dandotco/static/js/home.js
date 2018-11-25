// libs
import Vue from 'vue'
import axios from 'axios'
import debounce from 'lodash.debounce'



// my stuff
import { bolgTile } from './templates.js';

var
	bolgs = [],

	bolgListing = {
		props: ['title', 'perma', 'excerpt', 'id', 'body', 'tags'],
		template: bolgTile,
		methods: {
			// historyUpdate: function() {
			// 	console.log('updating history')
			// 	history.pushState({}, 'tag search', '/tagged/blarg');

			// },

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
		taggedUriString: '',
		taggedUri: false,
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
			if (taggart.searchTag.length == 0) {
				taggart.bolgs = []
				taggart.searching = false
				if (this.taggedUri == true) {
					
				}
			}
		},

		search: debounce((value) => {
			if (value.length > 0 && taggart.taggedUriString != taggart.searchTag){
				axios
					.get(`/api/tagged/${value}`, { crossdomain: false })
					.then(response => (taggart.bolgs = response.data.results))
					.catch(function(error){ console.log(error) })

				taggart.searching = true
				
			} else {
				taggart.statusCheck()
			}
		}, 500)
	},

	mounted() {
		if (typeof this.$refs.tagInput.dataset.tagged != 'undefined') {
			this.taggedUri = true
			this.searchTag = this.$refs.tagInput.dataset.tagged
			this.taggedUriString = this.$refs.tagInput.dataset.tagged
		} else {

		}
	}


})