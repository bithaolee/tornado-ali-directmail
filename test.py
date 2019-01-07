import tornado.ioloop
import tornado.web
import client
from tornado import gen

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        access_id = 'xxxxxxxxxxx'
        access_secret = 'sssssss'
        from_address = 'system@xxxx.com'
        from_alias = 'Test'
        resp = yield client.AliMail(access_id, access_secret, from_address, from_alias).send('xxxxxxxx@qq.com', 'subject', 'content')
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