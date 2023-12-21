# coding=utf-8
import os
import sys
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
from audio import Audio
import hashlib
 

API_KEY = 'mQOupbMlGRGaiA6Bg3erwo0b'
SECRET_KEY = 'btLPtZ3LK9kCxGeAwg56feiikGPkWrIY'

TEXT = "欢迎使用百度语音合成。"

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
PER = 110
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 6

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """
class TTSBaidu:
    def __init__(self):
        self.token = fetch_token()
        self.audio = Audio()

    def string_to_md5(self, string):
        md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
        return md5_val
    
    def say(self, message):
        print(message)
        md5_str = self.string_to_md5(message)
        os.makedirs("./wav", exist_ok=True)
        wav_filename = os.path.join('./wav', md5_str + ".wav")
        err_filename = os.path.join('./wav', md5_str + ".err")
        if (os.path.isfile(wav_filename)):
            self.audio.play(wav_filename)
            return True

        tex = quote_plus(message)  # 此处TEXT需要两次urlencode
        print(tex)
        params = {'tok': self.token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
                'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)
        print('test on Web Browser' + TTS_URL + '?' + data)

        req = Request(TTS_URL, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()

            headers = dict((name.lower(), value) for name, value in f.headers.items())

            has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
        except  URLError as err:
            print('asr http response http code : ' + str(err.code))
            result_str = err.read()
            has_error = True
        if has_error:
            with open(err_filename, 'wb') as of:
                of.write(result_str)
            return False
        else:
            of = open(wav_filename, 'wb')
            of.write(result_str)
            of.close()
            self.audio.play(wav_filename)
            return True
            # with open(wav_filename, 'wb') as of:
            #     of.write(result_str)
            #     return True

if __name__ == '__main__':
    pass