import http.server
import socket
import threading

from web import serverFile as sf
import LapseController as ci

class WebInterface():
    def __init__(self, l_config, c_config):
        self.port = 80
        self.host_name = socket.gethostbyname(socket.gethostname())
        self.camera = ci.LapseController(c_config)

        self.files = {
            '/': sf.LapsePage('web/site/index.html', l_config, self._stop_server),
            '/config': sf.ConfigPage('web/site/config.html', c_config),
            '/error': sf.ErrorPage('web/site/error.html'),
            '/styles.css': sf.CSSFile('web/site/styles.css'),
            '/preview.jpg': sf.PreviewFile('web/site/preview.jpg', c_config),
            '/favicon.ico': sf.ICOFile('web/site/favicon.ico')
        }

        handler = self._create_handler_class(self.files)
        self.http_server = http.server.HTTPServer((self.host_name, self.port), handler)

    def _stop_server(self):
        threading.Thread(target=self.http_server.shutdown, daemon=True).start()

    def _create_handler_class(self, file_dict):
        class InterfaceHandler(http.server.BaseHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.files = file_dict
                super(InterfaceHandler, self).__init__(*args, **kwargs)

            def do_HEAD(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            def _redirect(self, path):
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', path)
                self.end_headers()

            def do_GET(self):
                self.send_response(200)
                data = self.files[self.path]

                self.send_header('Content-type', data.content_type)
                self.end_headers()
                self.wfile.write(data.get_file())

            def do_POST(self):
                post_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(post_length).decode("utf-8")

                redirect = self.path
                did_succeed = self.files[self.path].handle_post(post_data)
                if not did_succeed:
                    redirect = '/error'
                    self.files[redirect].set_error(self.files[self.path].error, self.path)

                self._redirect(redirect)


        return InterfaceHandler

    def run_server(self):
        print(f"Starting server on {self.host_name}:{self.port}")
        self.http_server.serve_forever()