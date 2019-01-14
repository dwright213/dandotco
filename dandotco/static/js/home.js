import Vue from 'vue'
import axios from 'axios'
import debounce from 'lodash.debounce'

import bolgListing from './components/bolgListing'


var bolgs = [];
var taggart = new Vue({
	el: '#main-container',

	data: {
		bolgs: [],
		searchTag: '',
		taggedUriString: '',
		taggedUri: false,
		searching: false,
		explanation: ''

	},
	computed: {
		hideNoResults() {
			if (this.bolgs.length == 0 && this.searching) {
				return false
			} else {
				return true
			}
		},
		resultsLength() {
			return this.bolgs.length
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
			var 
				specialCharFilter = /\W|_/g,
				tag = value.replace(specialCharFilter, '');

			if (tag.length > 0 && taggart.taggedUriString != taggart.searchTag) {
				axios
					.get(`/api/tagged/${tag}`, { crossdomain: false })
					.then(response => {

						if (response.data.results.length == 0) {
							taggart.explanation = response.data.explanation
						}
						taggart.bolgs = response.data.results
					})
					.catch(function(error) { console.log(error) })

				taggart.searching = true

			} else {
				taggart.statusCheck()
			}
		}, 200)
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


