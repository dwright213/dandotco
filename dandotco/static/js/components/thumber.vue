<script type="text/javascript">
	var thumber = {

		props: ['format', 'id', 'name', 'orig_name', 'processed_sizes'],

		computed: {
			imgDir: function() {
				return `${this.$parent.imgDir}${this.$parent.bolgId}`;
			},
			enabledSizes: function() {
				let sizes = [];
				if (this.processed_sizes) {
					sizes = this.processed_sizes;
				} else {
					sizes = [100,400,800,1200];
				}
				return sizes;
			}


		},

		methods: {
			// return a description per image size.
			sizeDesc(size) {
				let desc = '';
				
				if (size === 100) {
					desc = 'thumbnail';
				}
				
				if (size === 400) {
					desc = 'half width';
				}
				
				if (size === 800) {
					desc = 'full width';
				}

				if (size > 800) {
					desc = 'huge, undithered';
				}
				return desc;
			},
			imgLoc(width) {
				return `${this.$parent.imgDir}${this.$parent.bolgId}/${this.name}${width}.${this.format}`
			},
			removeImg() {
				this.$parent.delete(this.orig_name)
			},
			copyImgLoc(width) {
				let url = this.imgLoc(width);
				navigator.clipboard.writeText(url)
			},
			markdownImgTag(width) {
				let url = this.imgLoc(width),
					mdTag = `![ALT TEXT](${url} "CAPTION TEXT"){: .float-right }`;
				navigator.clipboard.writeText(mdTag)
			},
			markdownLinkTag(width) {
				let url = this.imgLoc(width),
					mdTag = `![ALT TEXT](${url} "CAPTION TEXT"){: .float-right }`;
					mdTag = `[LINK TEXT](${url} "ALT TEXT")`;
					debugger;

				navigator.clipboard.writeText(mdTag)
			}
		}
	}
	export default thumber;
</script>
<template>
	

	<div class="img-thumb__container">
		<img class="img-thumb" v-bind:src=imgLoc(100) />
		<div class="img-thumb__controls img-thumb__controls">
		
			<div class="img-thumb__control">
				<div class="img-thumb__control__desc"><strong>{{ this.orig_name }}</strong></div>
				<button class="img-thumb__delete-btn" v-on:click="removeImg()">delete</button>
			</div>

			<div class="img-thumb__control" v-for="size in enabledSizes">
				<div class="img-thumb__control__desc">{{sizeDesc(size)}} / {{size}}</div>
				<button class="img-thumb__control__copy" v-on:click="copyImgLoc(size)">url</button> 
				<button class="img-thumb__control__copy" v-on:click="markdownImgTag(size)">img</button>
				<button class="img-thumb__control__copy" v-on:click="markdownLinkTag(size)">link</button>
			</div>
		</div>

	</div>
</template>