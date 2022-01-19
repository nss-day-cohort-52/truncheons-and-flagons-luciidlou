import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from teams.request import get_teams


class HandleRequests(BaseHTTPRequestHandler):
    def parse_query_string_parameters(self, params):
        filters = {}
        pairs = params.split("&")
        for pair in pairs:
            [key, value] = pair.split("=")
            if key in filters:
                filters[key]['resources'].append(value)
            else:
                filters[key] = { 'resources': [value] }

        return filters

    def parse_url(self, path):
        id = None
        filters = None
        url_parts = path.split("/")
        url_parts.pop(0)

        resource = url_parts[1]
        if "?" in resource:
            [resource, params] =  resource.split("?")
            filters = self.parse_query_string_parameters(params)

        try:
            route_parameters = url_parts[2]
            if "?" in route_parameters:
                [id, params] = route_parameters.split("?")
                id = int(id)
                filters = self.parse_query_string_parameters(params)
            else:
                try:
                    id = int(route_parameters)
                except IndexError:
                    pass  # No route parameter exists: /animals
                except ValueError:
                    pass  # Request had trailing slash: /animals/
        except IndexError:
            pass  # No route parameter exists

        return (resource, id, filters)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}
        (resource, id, filters) = self.parse_url(self.path)
        response = f"{get_teams(filters)}"

        self.wfile.write(response.encode())


def main():
    host = ''
    port = 8089
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
