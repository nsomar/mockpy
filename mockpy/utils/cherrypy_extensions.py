import cherrypy
from mockpy.models.mapping_request import *


"""
    Extensions
"""
def to_mapper_request():
    dic = {"method": cherrypy.request.method,
         "url": cherrypy.url(),
         "headers": cherrypy.request.headers}

    if cherrypy.request.process_request_body:
      dic["body"] = cherrypy.request.body.read()

    return MappingRequest(dic)

setattr(cherrypy, "to_mapper_request", to_mapper_request)
