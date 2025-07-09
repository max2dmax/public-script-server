#!/bin/bash
# Create a CLI menu for the user

while true; do
  echo "Choose an option:"
  echo "1. Say Hello"
  echo "2. Show date"
  echo "3. Exit"

  read choice

  case $choice in
    1)
      echo "Hello!"
      ;;
    2)
      date
      ;;
    3)
      echo "Goodbye!"
      break
      ;;
    *)
      echo "Invalid option."
      ;;
  esac
done