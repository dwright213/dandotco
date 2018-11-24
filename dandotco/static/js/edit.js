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
					.then(response => (this.$parent.images = response.data.images))
					.catch(function(error) {
						console.log(error);
					});
			}
		},

		mounted() {

		}
	},
	thumber = {
		props: ['format', 'id', 'name', 'orig_name'],
		template: imageThumb,
		computed: {
			thumbBg: function() {
				return {backgroundImage: `url('${this.imgLoc()}')`}
			}

		},
		methods: {
			imgLoc() {
				return `/static/img/processed/${bolgId}/${this.name}100.${this.format}`
			},
			removeImg() {
				axios
					.post(`/remove/${bolgId}/${this.orig_name}`, { crossdomain: false })
					.then(response => (this.$parent.images = response.data.images))
					.catch(function(error){ console.log(error) })
				
			}
		},

		mounted() {
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
		axios
			.get(`/api/${bolgId}/images`, { crossdomain: false })
			.then(response => (this.images = response.data.images))
	}
});