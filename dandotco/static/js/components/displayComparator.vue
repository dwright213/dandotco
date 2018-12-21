<script type="text/javascript">
	var displayComparator = {
		props: ['name', 'aspect', 'diag', 'color', 'rectid'],
		methods: {
			highlightRect: function() {
				console.log(this.$parent.highlightRect())
			}

		}
	}

	export default displayComparator;

</script>

<template>	
	<div 
		v-html="name" 
		@click="$parent.highlightRect(rectid)">
		
	</div>
</template>