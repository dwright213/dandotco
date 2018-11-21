export var
	bolgTile = `
		<div :id=tileId() class="bolg">
			<h3>
				<a v-bind:href=bolgLink()>
					{{ title }}
				</a>
			</h3>
			<p>{{ excerpt }}</p>
			<br>

			<span v-for="tag, index in tags">
				<a v-bind:href=tagLink(tag)>{{ tag }}</a>
				<span v-if="index <= (tags.length - 1)"> // </span>				
			</span>

		</div>

	`,

	uploadForm = `
		<form 	ref=uploadForm
				method=POST 
				enctype=multipart/form-data 
				action="/upload/" 
				@submit=checkForm>

			<input type=file name=photo>
			<input type="submit">
		</form>
	`,

	imageThumb = `
		<img v-bind:src=imgLoc() />
	`;
