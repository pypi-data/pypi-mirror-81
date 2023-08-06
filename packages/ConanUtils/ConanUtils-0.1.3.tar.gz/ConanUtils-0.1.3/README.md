# Conan Utils
useful utils for dealing with conan.io package manager

### Installation
Install latest version via pip:
```
python -m pip install conanutils
```

## Features
### Uploader
conan.io only supports uploading a single recipe ( or multiple recipes by a wildcard expression).
conan does not upload also all the needed dependencies to a remote server.
This is very annoying and often leads to a situation where dependent packages are missing on a 
remote server because someone failed to manually determine and upload dependent packages.

This tool is designed to support this feature. After a successful "conan install --build=missing ..." command
of the desired package, you can upload all needed packages in the dependency tree to a remote server.

Example
```
#following conan call will build qt5 and all missing dependencies with your build parameters
conan install qt5/5.13.2@bincrafters/stable --build=missing -pr MyAwesomeProfile

#this tool will upload your whole dependency tree to your conan server
python -m conanutils.upload -r YourServer qt5/5.13.2@bincrafters/stable 

```

### Configurator
When you work productively in a team with conan.io, you will realize that its essential that all
developers in a teams need to share exactly same conan settings. Als for new team members it is
exhausting to configure conan in the desired version with needed remotes, build profiles and so on.  

This tool simplifies this process by creating a json configuration that defines all needed remotes,
the correct conan version and all need build profiles. With a single command, conan can be
configured exactly as intended. 

Example
```
#create a new configuration
python -m conanutils.config --new /path/to/new/JsonFile.json

#adept the file to your needs and share it with your team members ( e.g. version it directly 
with your project ) 

#all other developers execute the following command after every change of the config:
#this will apply all defined settings in the config.
python -m conanutils.config /path/to/the/JsonFile.json


```


