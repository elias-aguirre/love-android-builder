#!/bin/bash

# Exit if an error occurs
set -e

# Check if the keystore file already exists
if [ -f "./love-android/app/android.keystore" ]; then
  echo "Keystore already exists. Exiting."
  exit 0
fi

KEYSTORE="./love-android/app/android.keystore"
ALIAS="testalias"
STOREPASS="testpassword"

keytool -genkey -v \
 -keystore "$KEYSTORE" \
 -keyalg RSA -keysize 2048 -validity 10000 \
 -alias "$ALIAS" \
 -storepass "$STOREPASS" \
 -keypass "$STOREPASS" \
 -dname "CN=myname, OU=My Unit, O=My Company, L=San Francisco, ST=California, C=US"
