var
	// plugins
	gulp = require('gulp'),
	webpack = require('webpack-stream'),
	sass = require('gulp-sass'),

	// watch this glob
	jsGlob = './js/**/*.js',
	scssGlob = './scss/**/*.scss',
	svgGlob = './img/*.svg',

	// input paths
	jsInput = './js/main.js',
	scssInput = './scss/main.scss',
	svgInput = './img/*.svg',

	// output paths
	dist = './dist/';


gulp.task('develop', function() {
	gulp.watch(jsGlob, gulp.parallel('scripts'))
	gulp.watch(scssGlob, gulp.parallel('styles'))
	gulp.watch(svgGlob, gulp.parallel('sprites'))

});

gulp.task('sprites', function () {
    return gulp.src(svgInput)
        .pipe(gulp.dest(dist));
});

gulp.task('styles', function () {
  return gulp.src(scssInput)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(dist));
});

gulp.task('scripts', function() {
	return gulp.src(jsGlob)
		.pipe(webpack({
			mode: 'development',
			entry: {
				home: './js/home.js',
				bolg: './js/bolg.js',
				compose: './js/compose.js'
			},
			output: {
				filename: '[name].chunk.js'
			},
			resolve: {
				alias: {
					vue: 'vue/dist/vue.js'
				}
			}
		}))
		.pipe(gulp.dest(dist));
});
