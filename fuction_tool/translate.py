import json
import urllib.error
import urllib.parse
import urllib.request
def translate(sentence, src_lan, tgt_lan, apikey):
    url = 'http://api.niutrans.com/NiuTransServer/translation?'
    data = {"from": src_lan, "to": tgt_lan, "apikey": apikey, "src_text": sentence}
    data_en = urllib.parse.urlencode(data)
    req = url + "&" + data_en
    res = urllib.request.urlopen(req)
    res = res.read()
    res_dict = json.loads(res)
    if "tgt_text" in res_dict:
        result = res_dict['tgt_text']
    else:
        result = res
    return result
if __name__ == "__main__":
    trans = translate("你好", 'zh', 'th', 'abb4cde6ab17ac9f5377c2d4a527fd31')
    print(trans)
