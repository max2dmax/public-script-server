#!/bin/bash
# Ask user for a password and check it

read -sp "Enter the secret code: " input
echo

if [ "$input" == "unicorn42" ]; then
  echo "Access granted."
else
  echo "Access denied."
fi