// libs
import Vue from 'vue';
import axios from 'axios';
import FormData from 'form-data';

// my stuff
import { uploadForm } from './templates.js'

var
	bolgId = null,

	uploader = {
		template: uploadForm,
		methods: {
			checkForm: function(e) {
				e.preventDefault()
				console.log(this.$refs)
				this.upload()

			},

			upload() {
				var myFormData = new FormData(this.$refs.uploadForm);
				axios({
						method: 'post',
						url: `/upload/${bolgId}`,
						data: myFormData,
						config: { headers: { 'Content-Type': 'multipart/form-data' } }
					})
					.then(function(response) {
						console.log(response);
					})
					.catch(function(error) {
						console.log(error);
					});
			}
		},

		mounted() {
			console.log('component componentized.')
		}
	};


new Vue({
	el: '#img-upload',

	components: {
		'fileUpload': uploader
	},

	mounted() {
		bolgId = this.$el.dataset.bolg
		console.log('vue instanced')
	}
});