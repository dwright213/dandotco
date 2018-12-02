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

		highlighter: function(tags) {
			let highlighted_tags = []
			tags.map(tag => {
				highlighted_tags.push({
					'name': tag,
					'html': tag.replace(taggart.searchTag, `<strong>${taggart.searchTag}</strong>`)
				})
			})

			return highlighted_tags
		},

		search: debounce((value) => {
			if (value.length > 0 && taggart.taggedUriString != taggart.searchTag) {
				axios
					.get(`/api/tagged/${value}`, { crossdomain: false })
					.then(response => {
						taggart.bolgs = response.data.results

						// taggart.bolgs.map(bolg => {
						// 	let tags = taggart.highlighter(bolg.tags)
						// 	bolg.tags = tags
						// })

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


