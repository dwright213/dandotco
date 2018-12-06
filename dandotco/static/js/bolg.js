var imgs = Array.from(document.getElementsByTagName('img'));

for (let img of imgs) {
	let wrapper = document.createElement('figure');
	
	if (img.classList.length > 0) {
		let classez = Array.from(img.classList)
		
		classez.map(klass => {
			wrapper.classList.add(klass) 
			img.classList.remove(klass)
		})


	}

	img.parentNode.insertBefore(wrapper, img)
	wrapper.appendChild(img)


	
	if (img.title.length > 0) {
		let figCap = document.createElement('figcaption');
		
		figCap.innerHTML = img.title
		wrapper.appendChild(figCap)
	}

}
