// libs
import Vue from 'vue';
import axios from 'axios';
import FormData from 'form-data';

// my stuff
import { uploadForm, imageThumb } from './templates.js'

var
	bolgId = null,
	images = [],
	uploader = {
		template: uploadForm,
		methods: {
			checkForm: function(e) {
				e.preventDefault()
				console.log(this.$refs)
				this.upload()

			},
			refreshImgs(imgs) {
				console.log('refreshing images..')
			},
			upload() {
				var myFormData = new FormData(this.$refs.uploadForm);
				axios({
						method: 'post',
						url: `/upload/${bolgId}`,
						data: myFormData,
						config: { headers: { 'Content-Type': 'multipart/form-data' } }
					})
					.then(response => (this.$parent.images = response.data.images))

					.catch(function(error) {
						console.log(error);
					});
			}
		},

		mounted() {
			console.log('component componentized.')
		}
	},
	thumber = {
		props: ['format', 'id', 'name', 'orig_name'],
		template: imageThumb,
		methods: {
			imgLoc() {
				return `/static/img/processed/${bolgId}/${this.name}100.${this.format}`
			}
		},

		mounted() {
			console.log('thumber thumbed')
		}

	};


new Vue({
	el: '#img-upload',
	data: {
		images: []

	},
	components: {
		'fileUpload': uploader,
		'imageThumb': thumber
	},

	mounted() {
		bolgId = this.$el.dataset.bolg
		console.log('vue instanced')
		console.log(this)
		axios
			.get(`/api/${bolgId}/images`, { crossdomain: false })
			.then(response => (this.images = response.data.images))
	}
});