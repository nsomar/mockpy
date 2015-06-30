## Mockpy
[![Build Status](https://travis-ci.org/oarrabi/mockpy.svg?branch=master)](https://travis-ci.org/oarrabi/mockpy)

[Mockpy](%5Bhttps://github.com/oarrabi/mockpy%5D) is a work in progress (Wip) python open source tool to quickly create mock servers on Mac OS X. Mockpy is inspired from wiremock and uses libmproxy for the proxy functionality.

`Mockpy` was originally created as an example of writing a python application under TDD methodology. As for the current code base, mockpy has 88% line coverage and 58% file coverage.

`mockpy` works by reading a list of configuration files in the YAML format, it uses these configurations to match the http request received and return an http response based on the matched YAML file.

The bellow example shows a YAML configuration file to match any http request based on this criteria:

- The url matches `.*test3.*` regular expression
- The http request contains a header with `Authorisation` key and value that matches `Bearer.*123` regular expression.
If the request matches, mockpy returns the following http response:
- Status code 200
- The body content is loaded form the `test1.json` json file
- The header value of `Content-type: application/json`

    request:
        method: GET
        url: .*test3.*

        headers:
          Authorisation: Bearer.*123

    response:
        status: 200
        body_file: test1.json

        headers:
          Content-type: application/json

At a high level, mockpy consists of the following classes:

![](https://dl.dropboxusercontent.com/s/4r94z9ctgueiwzv/flow.png?dl=0)

- `MappingItemsManager` is initialised with a directory of YAML configuration files. It uses these YAML files to create a list of `MappingItem`.
- `MappingItem` is the class representation of a one YAML configuration file. After parsing a config file, it creates a `MappingRequest` and a `MappingResponse` instances.
- `MappingRequest` represents an http request. It has method to match the url, header and body of the received request.
- `MappingResponse` represents an http response. It has methods to construct an http response with a status, headers and a body.

### Mockpy modes of operations
Mockpy has two modes of operation, standalone, and mitm proxy.

When mockpy is run in the standalone mode, it creates a local server using [cherrypy](http://www.cherrypy.org/) web framework. Under this mode of operation, the client application needs to point to this locally hosted mock server ([http://127.0.0.1:9090](http://127.0.0.1:9090/status) by default). The http requests received by this mock server are matched in the same manner described in the previous section.

![](https://dl.dropboxusercontent.com/s/x0zkzxaemz86ggs/mode-server.png?dl=0)

`mockpy` proxy mode of operation creates a proxy server at a port `9090` (configurable). It then alter the Mac OSX proxy settings to forward the HTTP/HTTPS requests to this proxy server. `mockpy` proxy server will intercept all of the http requests; If the request matches one of the configuration files (read the previous section), it will be handled by the proxy server to return a mock response based on the config file. If it does not match, then the http request will be forwarded by the proxy to the original destination.

![](https://dl.dropboxusercontent.com/s/vv9pr1cl2uqbqqc/mode-proxy.png?dl=0)

### Future milestones and improvements
Mockpy is still under development, the following is a list of tasks and improvement it still lacks:

- Create a better documentation
- Integration with a Travis CI
- Devise a proper mechanism to format the printed HTTP request and response.
- Provide more command line flags options
