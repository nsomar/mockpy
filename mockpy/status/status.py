import re


class Status(object):

    def __init__(self, mapping_handler):
        self.mapping_handler = mapping_handler

    def html_response(self):
        string = "<html>"
        string += "<body>"

        string += "Server running correctly<br/><br/>"
        string += "Parsed interceptors:<br/>"
        string += "_" * 80
        string += "<br/>"
        for item in self.mapping_handler.mappings:
            string += " - " + item.file_name + "<br/>"

            request = str(item.request).replace("\n", "<br/>")
            string += "<br/>"
            string += "Request:<br/>" + request + "<br/>"
            string += "<br/>"

            response = item.response.title()
            string += "Response:<br/>" + response + "<br/>"
            string += "_" * 80
            string += "<br/>"


        string += "</body>"
        string += "</html>"
        return string

    @staticmethod
    def is_status(url):
        return re.match("^.*(127\.0\.0\.1|localhost)(:\d*)?/status$", url) is not None
