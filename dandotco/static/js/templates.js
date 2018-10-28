export var
	bolgTile = `
		<div :id=tileId() class="bolg">
			<h3>
				<a v-bind:href=bolgLink()>
					{{ title }}
				</a>
			</h3>
			<p>{{ body }}</p>
			<br>
		</div>

	`;

