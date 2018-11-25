// libs
import Vue from 'vue';
import axios from 'axios';
import debounce from 'lodash.debounce'



// my stuff
import { searchBox, resultBox } from './templates.js';

var
	bolgs = [],

	resulter = {
		props: ['id', 'title'],
		template: resultBox,
		mounted() {}
	}

var taggart = new Vue({
	el: '#tagbox',

	data: {
		bolgs: [],
		searchTag: 'no sir'

	},

	components: {
		'result-box': resulter
	},

	methods: {
		search: debounce((value) => {
			console.log(value)
			if (value.length > 2){
				axios
					.get(`api/tagged/${value}`, { crossdomain: false })
					.then(response => (taggart.bolgs = response.data))
					.catch(function(error){ console.log(error) })
				
			}
		}, 250)
	},

	mounted() {
		axios
			.get(`api/tagged/frogs`, { crossdomain: false })
			.then(response => (taggart.bolgs = response.data))
			.catch(function(error) { console.log(error) })

	}


})