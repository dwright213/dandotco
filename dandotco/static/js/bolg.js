import './scripts/global.js'
import './scripts/bolgImageFigs.js'
import './scripts/tagSearcher.js'

// stop clumsy admin from accidentally deleting bolgs
document
	.getElementById('post-delete-form')
	.addEventListener('submit', function(event) {
		if(!confirm("Are you sure you wish to delete?")) {
			event.preventDefault()
		}
	}, false);
