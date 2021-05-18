
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json
import pickle

def application(environ,start_response):
        total_coin = 0
        try:
                f = open("coin.txt", "rb")
                total_coin = pickle.load(f)
        except:
                f = open("coin.txt", "wb")
                pickle.dump(total_coin, f)
                f.close()

        f = open("coin.txt", "rb")
        total_coin = pickle.load(f)
        f.close()

        d = parse_qs(environ['QUERY_STRING'])
        xcoin = escape(d.get('coin', [''])[0])
        mode = escape(d.get('mode', [''])[0])
        if(len(xcoin)>0):
                coin = int(xcoin)
        else:
                coin = 0

        if mode == "add":
                total_coin += coin
        elif mode == "minus":
                total_coin -= coin
                if(total_coin<0):
                        total_coin = 0
        elif mode == "init":
                total_coin = 0

        #         pass
        f = open("coin.txt", "wb")
        pickle.dump(total_coin, f)
        f.close()

        response_body = json.dumps({'coin': total_coin, "mode": mode})
        status = '200 OK'
        response_headers = [
                ('Content_Type', 'application/json'),
                ('Content_Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body]

httpd = make_server('172.20.10.6', 8051, application)
httpd.serve_forever()

