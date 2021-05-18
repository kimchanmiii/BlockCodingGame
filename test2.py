from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json
import pickle

def application(environ,start_response):
        total_coin = 0      # total_coin을 0으로 초기화하고 시작.

        # < try/except를 쓴 이유 >
        # 1) coin.txt 파일은 처음에 실행했을 땐 존재하지 않음.
        # 2) 존재하지 않는 파일을 읽으려고 할 경우, Error 발생.
        #  -> Error 발생시, except문을 들어가게 됨. (wb모드는 파일이 존재하지 않더래도, 새로 파일을 생성해 줌.)
        try:
            # 파이썬 서버에 있는 coin.txt 파일을 바이너리(이진)파일로 읽음(=rb모드)
            # Why? 피클은 파일을 읽을때 '이진(=바이너리) 모드' 로 지원하기 때문.
            f = open("coin.txt", "rb")
            total_coin = pickle.load(f)     # pickle.load(파일) : 파일에 있는 내용을 total_coin에 넣음. ex)만약 total_coin=20이면 그대로 불러오겠죠?
        except:
            # 만약 Error 발생했다면, 파일에 total_coin을 쓰고 close.
            # pickle.dump(객체, 파일) : 해당 파일에 객체 내용을 넣음.
            # load는 파일 -> 객체(파이썬코드)
            # dump는 객체(파이썬코드) -> 파일
            f = open("coin.txt", "wb")
            pickle.dump(total_coin, f)
            f.close()
        else:
            f.close()

        f = open("coin.txt", "rb")      # 이제는 파일이 '무조건' 존재할 것임. 따라서, rb모드로 파일 open
        total_coin = pickle.load(f)     # 파일에 쓰여진 내용을 total_coin에 넣음.
        f.close()                       # 파일은 close 해줘야함.

        d = parse_qs(environ['QUERY_STRING'])
        xcoin = escape(d.get('coin', [''])[0])
        mode = escape(d.get('mode', [''])[0])

        # len(xcoin)으로 준 이유는 coin= 뒤에 아무것도 오지않는 경우가 생김.  ex) 12.34.56.78?mode=get 이럴땐 coin이 안붙음
        # 그런 경우에는 int('') 이렇게 되는데, 안에 숫자값이 아니라서 Error 발생.
        # 따라서 xcoin의 길이가 1이상일 경우에만 실행하게 해놓음.
        if(len(xcoin)>0):
                coin = int(xcoin)
        else:
                coin = 0

        # mode 는 총 4가지 종류가 존재함.
        # 1) add : total_coin에 값을 더함(+=)
        # 2) minus : total_coin에 값을 빼줌(-=)
        #    -> But coin의 값이 음수값을 갖는것은 말이 안됨. 따라서 0미만의 값은 강제적으로 total_coin=0 설정.
        # 3) init : total_coin을 0으로 초기화 시켜줌.
        #    -> Why? 0으로 설정하려면, 파일을 직접 건드려야함. 단순히 님들 편하라고 만들어 놓은 것.
        # 4) 그외에 것들(get) : coin값을 주지 않을경우, 그저 total_coin값을 앱인벤터에 리턴함. -> if문에 따로 지정해주진 않았음
        if mode == "add":
                total_coin += coin
        elif mode == "minus":
                total_coin -= coin
                if(total_coin<0):
                        total_coin = 0
        elif mode == "init":
                total_coin = 0

        #         pass

        # total_coin에 값을 더하거나 뺐으면, 다시 그정보를 파일에 저장함.
        # 앞서 말했듯이, pickle은 이진모드로 write 해야함.
        # pickle.dump는 파이썬객체(total_coin)를 -> 파일(coin.txt)에 저장
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

httpd = make_server('192.168.0.5', 8051, application)
httpd.serve_forever()