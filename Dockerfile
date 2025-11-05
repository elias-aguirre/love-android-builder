# We use an official OpenJDK image as a base
FROM openjdk:17-jdk-slim

# Environment variables
ENV ANDROID_HOME=/opt/android-sdk
ENV JAVA_HOME=/usr/local/openjdk-17
ENV GRADLE_HOME=/opt/gradle/gradle-8.1
ENV PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$JAVA_HOME/bin:$GRADLE_HOME/bin:$PATH

# We install dependencies and download the Command-line Tools 
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends wget unzip \
 && mkdir -p $ANDROID_HOME/cmdline-tools \
 && cd $ANDROID_HOME/cmdline-tools \
 && wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip \
 && unzip -q cmdline-tools.zip \
 && rm cmdline-tools.zip \
 && mv cmdline-tools latest

# Accept the Android SDK licenses
RUN yes | sdkmanager --sdk_root=$ANDROID_HOME --licenses 

# We install git / bash / python3 / gradle
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends git bash python3 

RUN wget -q https://services.gradle.org/distributions/gradle-8.1-bin.zip -O gradle-8.1-bin.zip

RUN unzip -d /opt/gradle gradle-8.1-bin.zip \
 && rm gradle-8.1-bin.zip \
 && ls /opt/gradle/gradle-8.1

RUN gradle -v

WORKDIR /app

RUN git clone --recurse-submodules --depth 1 --branch 11.5a https://github.com/love2d/love-android

# We give execution permission to the Gradle wrapper
RUN chmod +x ./love-android/gradlew

# Copy all the files
COPY resources/ ./love-android/app/src/embed/assets/

COPY icon/ ./love-android/app/src/main/res

COPY keystore/ ./love-android/app/

COPY libs/ ./love-android/app/libs

COPY config.properties config.properties

COPY scripts/update_android_info.py update_android_info.py

COPY scripts/generate_keystore.sh generate_keystore.sh

# Run the script to update the Android info
RUN python3 update_android_info.py

# Run the script to generate the keystore
RUN ./generate_keystore.sh

WORKDIR /app/love-android

# Build APK (No Record)
RUN gradle assembleEmbedNoRecordRelease -Dorg.gradle.jvmargs="-Xmx4096M"

# Build APK (Record)
RUN gradle assembleEmbedRecordRelease -Dorg.gradle.jvmargs="-Xmx4096M"

# Build AAB (No Record)
RUN gradle bundleEmbedNoRecordRelease -Dorg.gradle.jvmargs="-Xmx4096M"

# Build AAB (Record)
RUN gradle bundleEmbedRecordRelease -Dorg.gradle.jvmargs="-Xmx4096M"
