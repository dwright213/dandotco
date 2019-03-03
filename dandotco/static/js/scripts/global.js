
// little last minute UI tweaks that we want on all pages.
document.addEventListener("DOMContentLoaded", function() {

	// make header image function as a link to home.
	document
		.getElementById('header-titled')
		.addEventListener('click', function() {
			location.href = '/'
		}, false);

	// override my nav-item-list height, for mobile nav
	let navLinks = document.getElementsByClassName('nav-link'),
		linkHeight = navLinks[1].clientHeight;
	document.querySelector('style').textContent +=
		`@media screen and (max-width: 480px) {
			#nav-toggle:checked ~ #nav-item-list {
				height: ${navLinks.length * linkHeight}px!important;
			}
		}`

});
