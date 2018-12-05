// element that will be wrapped
var imgs = Array.from(document.getElementsByTagName('img'));

// let myFirstPromise = new Promise((resolve, reject) => {
// 	// We call resolve(...) when what we were doing asynchronously was successful, and reject(...) when it failed.
// 	// In this example, we use setTimeout(...) to simulate async code. 
// 	// In reality, you will probably be using something like XHR or an HTML5 API.

// 	document.getElementsByTagName('img')

// 	setTimeout(function() {
// 		resolve("Success!"); // Yay! Everything went well!
// 	}, 250);

// });

for (let img of imgs) {
	let 
		wrapper = document.createElement('figure'),
		figCap = document.createElement('figcaption');

	img.parentNode.insertBefore(wrapper, img)
	wrapper.appendChild(img)
	wrapper.appendChild(figCap)
	figCap.innerHTML = img.title

}
