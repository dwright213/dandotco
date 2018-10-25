var
	// plugins
	gulp = require('gulp'),
	webpack = require('webpack-stream'),

	// watch this glob
	jsGlob = './js/**/*.js',
	sassGlob = './css/**/*.sass'

	// input paths
	jsInput = './js/main.js',
	sassInput = './css/main.sass',

	// output paths
	jsOutput = './dist/',
	cssOutput = './dist/';


gulp.task('develop', function() {
	gulp.watch(jsInput, gulp.parallel('scripts'))

})

gulp.task('scripts', function() {
	return gulp.src(jsGlob)
		.pipe(webpack({
			mode: 'development',
			output: {
				filename: 'main.js'
			},
			resolve: {
				alias: {
					vue: 'vue/dist/vue.js'
				}
			}
		}))


		.pipe(gulp.dest('./dist/'));
})