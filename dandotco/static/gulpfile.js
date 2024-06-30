var
	// plugins
	gulp = require('gulp'),
	webpack = require('webpack-stream'),
	// sass = require('gulp-sass'),
	sass = require('gulp-sass')(require('sass')),
	vueLoader = require('vue-loader/lib/plugin'),

	// watch this glob
	vueGlob = './js/components/*.vue',
	jsGlob = './js/**/*.js',
	scssGlob = './scss/**/*.scss',
	imgGlob = './img/ui/*',
	faviconGlob = './img/ui/favicons/*',

	// input paths
	jsInput = './js/main.js',
	scssInput = './scss/main.scss',
	imgInput = './img/ui/*',

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
			tagged: './js/tagged.js',
			labs: './js/labs.js'
		},
		resolve: {
			extensions: ['*', '.js', '.vue', '.json'] 
		},
		output: {
			filename: '[name].chunk.js'
		},
		module: {
			rules: [{
					test: /\.vue$/,
					loader: 'vue-loader'
				},
				{
					test: /\.css$/,
					use: [
						'vue-style-loader',
						'css-loader'
					]
				}
			]
		},
		plugins: [
			// make sure to include the plugin for the magic
			new vueLoader()
		]
	},

	devAlias = { vue: 'vue/dist/vue.js' },
	prodAlias = { vue: 'vue/dist/vue.min.js' };



gulp.task('default', function(done) {
	dist = '/var/media/'
	webpackConf.resolve['alias'] = prodAlias
	gulp.series('images', 'styles', 'scripts', 'favicons')();
	done();
})

gulp.task('develop', function() {
	webpackConf.resolve['alias'] = devAlias
	webpackConf.mode = 'development'
	gulp.watch([jsGlob, vueGlob], gulp.parallel('scripts'))
	gulp.watch(scssGlob, gulp.parallel('styles'))
	gulp.watch(imgGlob, gulp.parallel('images'))

});

gulp.task('images', function() {
	return gulp.src(imgInput)
		.pipe(gulp.dest(`${dist}img/ui`));
});

gulp.task('favicons', function() {
	return gulp.src(faviconGlob)
		.pipe(gulp.dest(`${dist}img/ui/favicons`));
});

gulp.task('styles', function() {
	return gulp.src(scssInput)
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(`${dist}css/`));
});

gulp.task('scripts', function() {
	return gulp.src(jsGlob)
		.pipe(webpack(webpackConf))
		.pipe(gulp.dest(`${dist}js/`));
});


