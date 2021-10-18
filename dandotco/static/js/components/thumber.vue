<script type="text/javascript">
	var thumber = {

		props: ['format', 'id', 'name', 'orig_name'],

		computed: {
			imgDir: function() {
				return `${this.$parent.imgDir}${this.$parent.bolgId}`;
			}
			// /static/img/processed/<bolg id>/filename.jpg

		},

		methods: {
			imgLoc() {
				return `${this.$parent.imgDir}${this.$parent.bolgId}/${this.name}100.${this.format}`
			},
			removeImg() {
				this.$parent.delete(this.orig_name)
			}

		}

	}
	export default thumber;

</script>

<template>
	<div class="img-thumb__container">
		<img class="img-thumb" v-bind:src=imgLoc() />
		<div class="img-thumb__controls img-thumb__controls">
			<div class="img-thumb__control">{{ imgDir }}/{{ name }}100.{{ format }}</div>
			<div class="img-thumb__control">{{ imgDir }}/{{ name }}400.{{ format }}</div>
			<div class="img-thumb__control">{{ imgDir }}/{{ name }}800.{{ format }}</div>
			<div class="img-thumb__control">{{ imgDir }}/{{ name }}1200.{{ format }}</div>
			<div class="img-thumb__control img-thumb__delete-btn" v-on:click="removeImg()">delete?</div>
		</div>

	</div>
</template>