import requests,pprint,random,html
from flask import Flask
from flask import Flask, render_template, request
from decouple import config

app = Flask(__name__)
# 텔레그램 API
url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')

# google API
google_url = 'https://translation.googleapis.com/language/translate/v2'
google_key = config('GOOGLE_TOKEN')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route(f'/{token}', methods=['POST'])
def telegram():
    # 1. 텔레그램이 보내주는 데이터 구조 확인
    pprint.pprint(request.get_json())
    # 2. 사용자 아이디.메시지 추출
    chat_id = request.get_json().get('message').get('chat').get('id')
    message = request.get_json().get('message').get('text')

    # 사용자가 로또라고 입력하면 로또 번호 6개 돌려주기
    if message == '로또':
        # li = []
        # for i in range(1,46):
        #     li.append(i)
        # result = random.sample(li,6)
        result = random.sample(range(1,46),6)

    # 사용자가 /번역 이라고 말하면 한-영 번역 제공
    elif message[:4] == '/번역 ':
        data = {
            'q': message[4:],
            'source': 'ko',
            'target': 'en'
        }
    # 1. 구글 API 번역 요청
        response = requests.post(f'{google_url}?key={google_key}',data).json()
    
    # 2. 번역 결과 추출 => 답장 변수에 저장
        result = html.unescape(response['data']['translations'][0]['translatedText'])

    # 그 외의 경우엔 메아리
    else:
        result = '로또 혹은 /번역 안녕하세요 라고 입력해보세요!'
    
    # 3. 텔레그램 API에 요청해서 답장 보내주기
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={result}')
    return '', 200

@app.route('/write')
def Hello_world():
    return render_template('write.html')

@app.route('/send')
def send():
    # 1. 사용자가 입력한 데이터 받아오기(request > 플라스크 기능)
    message = request.args.get('message')
    # 2. 텔레그램 API 메시지 전송 요청 보내기(requests > 파이썬 기능)
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')

    # 리턴 안해줘도 메시지 전송되지만 제대로 기능하는지 확인하기 위한 절차
    return '메시지 전송 완료! :)'


# 반드시 파일 최하단에 위치시킬 것!
if __name__ == '__main__':
    app.run(debug=True)
