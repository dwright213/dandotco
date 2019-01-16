<script type="text/javascript">


	 
	var bolgListing = {
		props: ['title', 'perma', 'excerpt', 'id', 'tags', 'created', 'resultsLength', 'index'],
		computed: {
			lastOne() {

			}
		},
		methods: {

			tileId: function() {
				return 'bolg-' + this.id
			},

			bolgLink: function() {
				return '/bolg/' + this.perma
			},

			tagLink: function(tag) {
				return '/tagged/' + tag
			}

		}
	}
	
	export default bolgListing;

</script>

<template>

	<div 	:id=tileId() 
			class="bolg">
		<h3>
			<a v-bind:href=bolgLink()>
				{{ title }}
			</a>
			<span class='bolg-listing__time-stamp'> {{ created.toLowerCase() }}</span>
		</h3>
		<p v-html="excerpt"></p>
		<br>
		<span v-for="tag, index in tags">
			<a  v-bind:href=tagLink(tag.name) v-html="'#'+tag.html+' '"></a>
		</span>
		<hr v-if="(index+1) < resultsLength">
	</div>

</template>