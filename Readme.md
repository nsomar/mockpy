# Mockpy

[![Build Status](https://travis-ci.org/oarrabi/mockpy.svg?branch=master)](https://travis-ci.org/oarrabi/mockpy)

Mockpy is a python open source line utility to quickly create mock servers on Mac OS X.
Mockpy is inspired by wiremock and uses libmproxy for the proxy functionality.

Mockpy works by reading a list of configuration files in the YAML format, it uses these configurations to match the HTTP request received and return an http response based on the matched YAML file configuration.

# Why mockpy
- You want a very lightweight utility to quickly create a mock API
- No need to edit your app code as it uses proxy mocking
- Works on top of proven technology ([mitmproxy](https://mitmproxy.org/) and [cherrypi](http://www.cherrypy.org/))
- Update to the mock API are picked up from files without the need to start/restart the server again.

# Installation

Mockpy can be installed as a python wheel using `pip`, as a standalone binary using `homebrew`, or by downloading the [archived binary](https://github.com/oarrabi/mockpy/releases) from release.

## Installing using brew (recommended)
Install using brew tap

    brew tap oarrabi/tap
    brew install mockpy

## Installing with pip

Make sure you have [pip](https://pip.pypa.io/en/latest/installing.html) installed.

Run the following to install mockpy

    pip install mockpy

# Usage

Bellow is a description of the basic operations that `mockpy` provides, for a more complete understanding please refer to [the wikis](https://github.com/oarrabi/mockpy/wiki).

## Initialize a directory
Initialize a the current folder by running:

    mockpy init
This will create two folders:    

`inout`: this folder will contains a list of mapping YAML files, each YAML file represents an request and response operation.

`res`: resource folder contains the static HTML, JSON, Images and static files returned as part of the mocking process.

To understand the YAML file format, please refer to the documentation.

### Sample 

    request:
        method: GET
        url: .*sample/matching.*
    response:
        status: 200
        body: hello world

The above catches all the GET request that has `sample/matching` in its URL, and returns the status 200. 
Requesting `http://localhost:9090/sample/matching` returns a response with `"hello world"` in its body.

More information about the YAML request/response check out the [wikis](https://github.com/oarrabi/mockpy/wiki/YAML-request-response--file-format).

## Start the mock server
The mock server can be started as a standalone web server, or as a proxy server.

### Standalone web server
Use `mockpy start` to start the standalone web server, this will setup a server on the default port. Visit `127.0.0.1:9090` to check the mock server.

### Proxy web server
To start mockpy in proxy server mode use `mockpy start -x`. This command does the following:
- Starts a proxy server on '127.0.0.1:9090'
- Sets the macs HTTP/HTTPS settings to the created proxy server.

# Documentation
Mockpy contains a documentation that can be accessed following [this link](https://github.com/oarrabi/mockpy/wiki).

# Future milestones and improvements
Mockpy is still under development, the following is a list of tasks and improvement it still lacks:

- Create a better documentation
- Devise a proper mechanism to format the printed HTTP request and response.
- Provide more command line flags options
