var bolgs = [];

	bolgListing = {
		props: ['title', 'id', 'body'],
		template: '<div :id=tileId() ><h3>{{ title }}</h3> <p>{{ body }}</p><br></div>',
		methods: {
			tileId: function() {
				return 'bolg-' + this.id
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
	mounted() {
		axios
			.get('http://localhost:5000/api', {crossdomain: false})
			.then(response => (this.bolgs = response.data))
	}
})