import os
import configparser
import base64

def update_android_information(app_name, bundle_id, icon_specifier, version_string, version_code, keystore_filename, keystore_alias, keystore_key_password, keystore_store_password, custom_scheme, include_libs):
    build_gradle_path = "love-android/app/build.gradle"
    manifest_path = "love-android/app/src/main/AndroidManifest.xml"
    gradle_properties_path = "love-android/gradle.properties"

    # Update build.gradle
    with open(build_gradle_path, "r+", encoding="utf-8") as file:
        data = file.read()
        insert_pos = data.find("\n", data.find("proguardFiles")) + 1
        data = data[:insert_pos] + "            signingConfig signingConfigs.release\n" + data[insert_pos:]
        insert_pos = data.find("buildTypes") - 4
        data = data[:insert_pos] + "    signingConfigs {\n" \
                                 "        release {\n" \
                                 f"            storeFile file('./{keystore_filename}')\n" \
                                 f"            keyAlias '{keystore_alias}'\n" \
                                 f"            keyPassword '{keystore_key_password}'\n" \
                                 f"            storePassword '{keystore_store_password}'\n" \
                                 "        }\n" \
                                 "    }\n" + data[insert_pos:]
        if include_libs:
            insert_pos = data.find("buildTypes") - 4
            data = data[:insert_pos] + "    sourceSets {\n" \
                                     "        main {\n" \
                                     "            jniLibs.srcDir(['libs'])\n" \
                                     "        }\n" \
                                     "    }\n" + data[insert_pos:]
        file.seek(0)
        file.truncate()
        file.write(data)

    # Update AndroidManifest.xml
    with open(manifest_path, "r+", encoding="utf-8") as file:
        data = file.read()
        data = data\
            .replace("OpenGL ES 2.0", "OpenGL ES 3.0")\
            .replace("0x00020000", "0x00030000")\
            .replace("@drawable/love", icon_specifier)
        try:
            scheme, host = custom_scheme.split("://")
            if scheme and host:
                data = data[:data.rfind("</intent-filter>") + 16] + f'''
                    <intent-filter>
                      <action android:name="android.intent.action.VIEW" />
                      <category android:name="android.intent.category.DEFAULT" />
                      <category android:name="android.intent.category.BROWSABLE" />
                      <data android:scheme="{scheme}" android:host="{host}" />
                    </intent-filter>''' + data[data.rfind("</intent-filter>") + 16:]
        except ValueError:
            pass
        file.seek(0)
        file.truncate()
        file.write(data)

    # Update gradle.properties
    with open(gradle_properties_path, "w", encoding="utf-8") as file:
        data = (
            f"app.name_byte_array={','.join(map(str, app_name .encode()))}\n"
            f"app.application_id={bundle_id}\n"
            "app.orientation=landscape\n"
            f"app.version_code={version_code}\n"
            f"app.version_name={version_string}\n"
            "android.enableJetifier=false\n"
            "android.useAndroidX=true\n"
            "android.defaults.buildfeatures.buildconfig=true\n"
            "android.nonTransitiveRClass=true\n"
            "android.nonFinalResIds=true\n"
            "org.gradle.caching=true\n"
        )
        file.write(data)

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        "app_name": config.get("DEFAULT", "app_name"),
        "bundle_id": config.get("DEFAULT", "bundle_id"),
        "icon_specifier": config.get("DEFAULT", "icon_specifier"),
        "version_string": config.get("DEFAULT", "version_string"),
        "version_code": config.get("DEFAULT", "version_code"),
        "keystore_filename": config.get("DEFAULT", "keystore_filename"),
        "keystore_alias": config.get("DEFAULT", "keystore_alias"),
        "keystore_key_password": config.get("DEFAULT", "keystore_key_password"),
        "keystore_store_password": config.get("DEFAULT", "keystore_store_password"),
        "custom_scheme": config.get("DEFAULT", "custom_scheme"),
        "include_libs": config.get("DEFAULT", "include_libs")
    }

if __name__ == "__main__":
    config_path = "config.properties"
    config = load_config(config_path)

    update_android_information(
        app_name=config["app_name"],
        bundle_id=config["bundle_id"],
        icon_specifier=config["icon_specifier"],
        version_string=config["version_string"],
        version_code=config["version_code"],
        keystore_filename=config["keystore_filename"],
        keystore_alias=config["keystore_alias"],
        keystore_key_password=config["keystore_key_password"],
        keystore_store_password=config["keystore_store_password"],
        custom_scheme=config["custom_scheme"],
        include_libs=config["include_libs"] == "true"
    )