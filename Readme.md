# Mockpy
[![Build Status](https://travis-ci.org/oarrabi/mockpy.svg?branch=master)](https://travis-ci.org/oarrabi/mockpy)

Mockpy is a python open source line utility to quickly create mock servers on Mac OS X.
Mockpy is inspired from wiremock and uses libmproxy for the proxy functionality.

mockpy works by reading a list of configuration files in the YAML format, it uses these configurations to match the http request received and return an http response based on the matched YAML file configuration.


# Installation

Mockpy can be installed as a python wheel using `pip` or as a standalone binary using `homebrew`

## Installing with pip

Make sure you have [pip](https://pip.pypa.io/en/latest/installing.html) installed.

Run the following to install mockpy

    pip install mockpy

## Installing using brew
Install using brew tap

    brew tap oarrabi/tap
    brew install mockpy

# Usage
