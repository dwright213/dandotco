<script type="text/javascript">
	var thumber = {

		props: ['format', 'id', 'name', 'orig_name'],

		computed: {
			imgDir: function() {
				return `${this.$parent.imgDir}${this.$parent.bolgId}`;
			}


		},

		methods: {
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
				<div class="img-thumb__control__desc">thumbnail / 100px</div>
				<button class="img-thumb__control__copy" v-on:click="copyImgLoc(100)">url</button> 
				<button class="img-thumb__control__copy" v-on:click="markdownImgTag(100)">img</button>
				<button class="img-thumb__control__copy" v-on:click="markdownLinkTag(100)">link</button>
			</div>
			
			<div class="img-thumb__control">
				<div class="img-thumb__control__desc">half paragraph / 400px</div>
				<button class="img-thumb__control__copy" v-on:click="copyImgLoc(400)">url</button> 
				<button class="img-thumb__control__copy" v-on:click="markdownImgTag(400)">img</button>
				<button class="img-thumb__control__copy" v-on:click="markdownLinkTag(400)">link</button>
			</div>
			
			<div class="img-thumb__control">
				<div class="img-thumb__control__desc">full paragraph / 800px</div>
				<button class="img-thumb__control__copy" v-on:click="copyImgLoc(800)">url</button> 
				<button class="img-thumb__control__copy" v-on:click="markdownImgTag(800)">img</button>
				<button class="img-thumb__control__copy" v-on:click="markdownLinkTag(800)">link</button>
			</div>
			
			<div class="img-thumb__control">
				<div class="img-thumb__control__desc">huge / 1200px</div>
				<button class="img-thumb__control__copy" v-on:click="copyImgLoc(1200)">url</button> 
				<button class="img-thumb__control__copy" v-on:click="markdownImgTag(1200)">img</button>
				<button class="img-thumb__control__copy" v-on:click="markdownLinkTag(1200)">link</button>
			</div>

			<div class="img-thumb__control">
				<button class="img-thumb__delete-btn" v-on:click="removeImg()">delete</button>
			</div>
		</div>

	</div>
</template>