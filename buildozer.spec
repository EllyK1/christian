[app]

# (str) Title of your application
title = ChristianApp

# (str) Package name
package.name = christianapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.christian

# (str) Source code where the main.py (christianmobileapp.py) lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,numpy,sounddevice,pyrebase,pillow,fpdf

# (str) Presplash of the application
presplash.filename = presplash.png
android.presplash_color = #FFFFFF

# (str) Icon of the application
icon.filename = christian.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature
android.allow_backup = True

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

# (str) The format used to package the app for release mode
android.release_artifact = aab


[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
