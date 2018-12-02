<script type="text/javascript">
	var thumber = {

		props: ['format', 'id', 'name', 'orig_name'],

		computed: {
			thumbBg: function() {
				return { backgroundImage: `url('${this.imgLoc()}')` }
			}

		},

		methods: {
			imgLoc() {
				return `/static/img/processed/${this.$parent.bolgId}/${this.name}100.${this.format}`
			},
			removeImg() {
				this.$parent.delete(this.orig_name)
			}

		}

	}
	export default thumber;

</script>

<template>
	<div class="img-thumb" v-bind:style="thumbBg">
		<div class="img-thumb__delete-btn" v-on:click="removeImg()">delete?</div>
		<div class="img-thumb__info-text">{{ name }}100.{{ format }}</div>
		<div class="img-thumb__info-text">{{ name }}400.{{ format }}</div>
		<div class="img-thumb__info-text">{{ name }}800.{{ format }}</div>
		<div class="img-thumb__info-text">{{ name }}1200.{{ format }}</div>
		<!-- <img v-bind:src=imgLoc() /> -->

	</div>
</template>