import tornado.ioloop
import tornado.web
from tornado import gen
# import tornado_directmail
from tornado_directmail.client import AliMail

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        access_id = 'LTAIXj3iWYkXZTKV'
        access_secret = 'VnGuSvcm8dUdvVKsKcwzpcWacgMM3f'
        from_address = 'system@blockvita.com'
        from_alias = 'Test'
        resp = yield AliMail(access_id, access_secret, from_address, from_alias).send('haolee1990@qq.com', 'subject', 'content')
        print(resp)
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()