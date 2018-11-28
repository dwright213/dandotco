"""
create needed tables
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
    	'ALTER TABLE bolg ADD COLUMN pictures text;'
    	'ALTER TABLE tag ADD COLUMN kitchens text;'
    )
]
