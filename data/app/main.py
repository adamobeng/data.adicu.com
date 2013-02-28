import tornado.web

import app.basic

class MainHandler(app.basic.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = self.get_secure_cookie("name")
        token = self.get_secure_cookie("_id")
        self.render('index.html', message="Hello, %s! Your API Token is %s" %
                (name, token))
