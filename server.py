import falcon
from waitress import serve

app = falcon.API()

users = {
    'admin': hash('admin'),
}


class Auth(object):
    def on_get(self, req, resp):
        user = req.params['user']
        password = req.params['password']
        if user in users.keys():
            password = hash(password)
            if users[user] == password:
                resp.status = falcon.HTTP_200
                resp.body = "Fuck yeah!"
                return
            else:
                resp.status = falcon.HTTP_403
                return
        else:
            resp.status = falcon.HTTP_403
            return


app.add_route('/', Auth())
serve(app, listen='*:5678')
