import urllib.error
import urllib.parse
import urllib.request
import gradio as gr
import json
from dotenv import load_dotenv, find_dotenv
import os
# 加载环境变量和初始化API
_ = load_dotenv(find_dotenv())
def translate(sentence, src_lan, tgt_lan):
    url = 'http://api.niutrans.com/NiuTransServer/translation?'
    api_key = os.getenv('Translate_key')
    data = {"from": src_lan, "to": tgt_lan, "apikey": api_key, "src_text": sentence}
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
# 创建其他Tab页面的内容（示例）
def chat_completion_translate():
    gr.Markdown("### Translate your text from one language to another")
    source_language = gr.Radio(['zh', "en"], label="Source Language")
    target_language = gr.Radio(["th", "en"], label="Target Language")
    sentence_input = gr.Textbox(label="Enter Sentence")
    output_text = gr.Textbox(label="Translated Sentence", interactive=False)
    submit_button = gr.Button("Translate")
    submit_button.click(
        fn=translate,
        inputs=[sentence_input, source_language, target_language],
        outputs=output_text
    )
