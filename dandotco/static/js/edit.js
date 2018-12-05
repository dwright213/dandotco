// libs
import Vue from 'vue';
import axios from 'axios';
import FormData from 'form-data';

// my stuff
import uploader from './components/imgUploader';
import thumber from './components/thumber';

var
	bolgId = null,
	images = [],


	editing = new Vue({
		el: '#img-upload',
		data: {
			bolgId: '',
			images: [],
			imgDir:''

		},

		components: {
			'fileUpload': uploader,
			'imageThumb': thumber
		},

		methods: {

			upload(uploadForm) {
				var myFormData = new FormData(uploadForm);
				axios({
						method: 'post',
						url: `/upload/${this.bolgId}`,
						data: myFormData,
						config: { headers: { 'Content-Type': 'multipart/form-data' } }
					})
					.then(response => (this.images = response.data.images))
					.catch(function(error) {
						console.log(error);
					});
			},

			delete(orig_name) {
				axios
					.post(`/remove/${this.bolgId}/${orig_name}`, { crossdomain: false })
					.then(response => (this.images = response.data.images))
					.catch(function(error) { console.log(error) })

			}

		},




		mounted() {
			this.bolgId = this.$el.dataset.bolg
			this.imgDir = this.$el.dataset.imgLoc
			axios
				.get(`/api/${this.bolgId}/images`, { crossdomain: false })
				.then(response => (this.images = response.data.images))
		}
	});