#!/bin/bash

# Change what it says here. You can also choose a voice. Check under system settings > Accessibility > Spoken Content for different voices. 
osascript -e 'say "This is a test!" using "Samantha"'

# Wait for dramatic effect. Change the number to change how long it waits. 
sleep 3

# Launch website. Change url to choose a new website. Currently set to open Rick Astley's eternal reign. 
osascript -e 'open location "https://www.youtube.com/watch?v=dQw4w9WgXcQ"'