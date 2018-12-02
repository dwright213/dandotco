<script type="text/javascript">

	var uploader = {
		methods: {
			checkForm: function(e) {
				e.preventDefault()
				this.$parent.upload(this.$refs.uploadForm)

			}
		}
			
	}

	export default uploader;
</script>

<template>	
	<form 	ref=uploadForm
			method=POST 
			enctype=multipart/form-data 
			@submit=checkForm>

		<input class="compose-form__input" type=file name=photo>
		<input class="compose-form__button" type="submit">
	</form>
</template>
