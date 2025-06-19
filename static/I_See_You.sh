#!/bin/bash
osascript -e 'say "Smile, you are on camera!" using "Whisper"'
osascript -e 'tell application "Photo Booth" to activate'
sleep 4
osascript -e 'say "Look into the lens..." using "Whisper"'