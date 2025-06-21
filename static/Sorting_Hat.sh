#!/bin/bash

TARGET_DIR="${1:-}"

if [ -z "$TARGET_DIR" ]; then
    read -rp "Enter the full path to the folder you wanna organize: " TARGET_DIR
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "🚫 Directory not found: $TARGET_DIR"
    exit 1
fi

cd "$TARGET_DIR" || exit

for FILE in *; do
    if [ -f "$FILE" ]; then
        EXT="${FILE##*.}"

        if [ "$FILE" = "$EXT" ]; then
            EXT="no_extension"
        fi

        mkdir -p "$EXT"

        mv "$FILE" "$EXT/"
        echo "📁 Moved '$FILE' → $EXT/"
    fi
done

echo "✅ All done! Your files have been sorted! 💅"