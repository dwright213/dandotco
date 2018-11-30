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
	svgInput = './img/ui/*',
	
	// output paths
	dist = 'dist/',

	// webpack conf
	webpackConf = {
		mode: 'production',
		entry: {
			home: './js/home.js',
			bolg: './js/bolg.js',
			compose: './js/compose.js',
			edit: './js/edit.js',
			tagged: './js/tagged.js'
		},
		resolve: {},
		output: {
			filename: '[name].chunk.js'
		}
	},

	vueAlias = {alias: {vue: 'vue/dist/vue.js'}};



gulp.task('default', function (done) {
	dist = '/var/media/'
	webpackConf.mode = 'development'
	webpackConf.resolve = vueAlias
	gulp.series('sprites', 'styles', 'scripts')();
	done();
})

gulp.task('develop', function() {
	webpackConf.resolve = vueAlias
	webpackConf.mode = 'development'
	gulp.watch(jsGlob, gulp.parallel('scripts'))
	gulp.watch(scssGlob, gulp.parallel('styles'))
	gulp.watch(svgGlob, gulp.parallel('sprites'))

});

gulp.task('sprites', function () {
    return gulp.src(svgInput)
        .pipe(gulp.dest(`${dist}img/ui`));
});

gulp.task('styles', function () {
  return gulp.src(scssInput)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(`${dist}css/`));
});

gulp.task('scripts', function() {
	return gulp.src(jsGlob)
		.pipe(webpack(webpackConf
		// {
		// 	mode: 'development',
		// 	entry: {
		// 		home: './js/home.js',
		// 		bolg: './js/bolg.js',
		// 		compose: './js/compose.js',
		// 		edit: './js/edit.js',
		// 		tagged: './js/tagged.js'
		// 	},
		// 	output: {
		// 		filename: '[name].chunk.js'
		// 	},
		// 	resolve: {
		// 		alias: {
		// 			vue: 'vue/dist/vue.js'
		// 		}
		// 	}
		// }
		))
		.pipe(gulp.dest(`${dist}js/`));
});
