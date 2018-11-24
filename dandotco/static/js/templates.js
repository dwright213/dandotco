export var
	bolgTile = `
		<div :id=tileId() class="bolg">
			<h3>
				<a v-bind:href=bolgLink()>
					{{ title }}
				</a>
			</h3>
			<p v-html="excerpt"></p>
			<br>

			<span v-for="tag, index in tags">
				<a v-bind:href=tagLink(tag)>{{ tag }}</a>
				<span v-if="index < (tags.length - 1)"> // </span>				
			</span>

		</div>

	`,

	uploadForm = `
		<form 	ref=uploadForm
				method=POST 
				enctype=multipart/form-data 
				@submit=checkForm>

			<input class="compose-form__input" type=file name=photo>
			<input class="compose-form__button" type="submit">
		</form>
	`,

	imageThumb = `
		<div class="img-thumb" v-bind:style="thumbBg">
			<div class="img-thumb__delete-btn" v-on:click="removeImg()">delete?</div>
			<div class="img-thumb__info-text">{{ name }}100.{{ format }}</div>
			<div class="img-thumb__info-text">{{ name }}400.{{ format }}</div>
			<div class="img-thumb__info-text">{{ name }}800.{{ format }}</div>
			<div class="img-thumb__info-text">{{ name }}1200.{{ format }}</div>
			<!-- <img v-bind:src=imgLoc() /> -->
			
		</div>
	`;
