#!/bin/bash


osascript -e 'tell app "System Events" to tell appearance preferences to set dark mode to true'
osascript -e 'tell application "Finder" to set desktop picture to POSIX file "/Users/maxstevenson/Dev/public-script-server/static/images/batman_wallpaper.jpg"'

say -v Daniel "Batman Mode enabled! Welcome to the bat cave, Bruce Wayne."
osascript -e 'tell application "Terminal" to do script "echo 🦇 Welcome to Batman Mode 🦇; echo \"I am vengeance. I am the night. I am Batman.\"; echo \"\"; figlet Batman"'

afplay "/Users/maxstevenson/Dev/public-script-server/static/audio/batman_theme.mp3"