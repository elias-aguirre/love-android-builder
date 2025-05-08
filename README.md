# LÖVE Android Builder

This Docker image automatically prepares the environment needed to build games made with LÖVE using the [love2d/love-android](https://github.com/love2d/love-android) repository (tag `11.5a`). It allows you to generate `.apk` or `.aab` files, ready to be installed on Android devices or published on Google Play.

## 📋 Instructions
Before creating the Docker image, you can package the APK with your own LÖVE game. Save the files to the `resources` folder. You can also update the `config.properties` file to customize the game packaging.
### config.properties
| Name                      | Default                | Description                                                   |
| :-------------------------| -----------------------| ------------------------------------------------------------- |
| `app_name`                | `Test Game`            | App display name. Used in `app/src/main/AndroidManifest.xml`  |
| `bundle_id`               | `org.example.testgame` | App bundle id. Used in `app/build.gradle`                     |
| `icon_specifier`          | `@drawable/love`       | App icon specifier. Used in `app/src/main/AndroidManifest.xml`|
| `version_string`          | `1.0.0`                | App version string. Used in `app/build.gradle`                |
| `version_code`            | `1`                    | Numeric app version code. Used in `app/build.gradle`          |
| `keystore_filename`       | `android.keystore`     | Signing keystore's filename.                                  |
| `keystore_alias`          | `test-alias`           | Signing keystore's alias.                                     |
| `keystore_key_password`   | `testpassword`         | Signing keystore's key password.                              |
| `keystore_store_password` | `testpassword`         | Signing keystore's store password.                            |
| `custom_scheme`           | `testscheme://testhost`| URL scheme. Used in `app/src/main/AndroidManifest.xml`        |
| `include_libs`            |  `false`               | Whether to include JNI libraries.                             |

To change the icon, replace the `love.png` file or provide your own files (remember to update `icon_specifier` if needed) with PNG's of the same size:
* icon/drawable-hdpi/love.png (72x72)
* icon/drawable-mdpi/love.png (48x48)
* icon/drawable-xhdpi/love.png (96x96)
* icon/drawable-xxhdpi/love.png (144x144)
* icon/drawable-xxxhdpi/love.png (192x192)

To add your own signing keystore file, save it into the `keystore` folder (remember to update `keystore_filename` if needed).

## 🛠 How to build the Docker image
```bash
docker build -t love-android-builder .
```

## 📦 Extract apk/aab from the container
First, create the container:
```bash
docker create --name love love-android-builder
```
Then, copy the APK or AAB file:
```bash
docker cp love:/app/love-android/app/build/outputs/apk/embedNoRecord/release/app-embed-noRecord-release.apk love.apk
docker cp love:/app/love-android/app/build/outputs/bundle/embedNoRecordRelease/app-embed-noRecord-release.aab love.aab
```
If your game uses microphone:
```bash
docker cp love:/app/love-android/app/build/outputs/apk/embedRecord/release/app-embed-record-release.apk love.apk
docker cp love:/app/love-android/app/build/outputs/bundle/embedRecordRelease/app-embed-record-release.aab love.aab
```