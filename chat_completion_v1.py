import gradio as gr
import os
import time
from openai import OpenAI
import matplotlib
from fuction_tool.sdweb_generate import Text2ImgDall,Text2Img
matplotlib.use('TkAgg')
from dotenv import load_dotenv, find_dotenv
import json
import urllib.error
import urllib.parse
import urllib.request
# 加载环境变量和初始化API
_ = load_dotenv(find_dotenv())
openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def generate_images_with_prompts(prompt, navigator_prompt,slider,model_select):
    if model_select != "stable-diffusion":
        image_list = Text2ImgDall(prompt)
        return image_list
    else:
        image_list = Text2Img(prompt,navigator_prompt,steps=20,batch_size=slider)
        return image_list




def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    return history


def bot(history):
    messages = [{"role": "user", "content": history[-1][0]}]
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        temperature=0
    )
    history[-1][1] = ""
    for chunk in completion:
        for choice in chunk.choices:
            content = choice.delta.content
            if content:
                history[-1][1] += content
                time.sleep(0.05)
                yield history
# 你的bot函数...
def show_navigator_prompt(model_choice):
    if model_choice == "stable-diffusion":
        # 如果选择了stable-diffusion，返回一个反向提示词的框
        return gr.update(visible=True),gr.update(visible=True)
    else:
        # 否则返回一个隐藏的文本框
        return gr.update(visible=False),gr.update(visible=False)

def chat_image_component():
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                bubble_full_width=False,
                avatar_images=(None, (os.path.join(os.path.dirname(__file__), r"D:\yuanlis_project\Aicontent\ChatCompletion\ChatCompletionWebDemo\static\avatar.jpg"))),
            )
            txt = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="Enter text and press enter",
                container=False,
                label="chat now",
            )
            commit_btn = gr.Button("chat", scale=2)
            commit_btn.click(fn=add_text, inputs=[chatbot, txt], outputs=[chatbot, txt]).then(
                bot, chatbot, chatbot, api_name="bot_response"
            ).then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
            txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=True).then(
                bot, chatbot, chatbot, api_name="bot_response"
            )
            txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
        with gr.Column(scale=2, min_width=600):
            model_select = gr.Dropdown(choices=["Dall-3", "stable-diffusion"], label="Choose a Model")
            prompt_input = gr.Textbox(placeholder="Enter prompt for image generation", label="Image Prompt")
            navigator_prompt_input = gr.Textbox(visible=False, placeholder="Enter navigator prompt", label="Navigator Prompt")
            slider = gr.Slider(
                visible=False,
                minimum=1,
                maximum=8,
                step=1,
                label="Slider",
                interactive=True
            )
            model_select.change(
                fn=show_navigator_prompt,
                inputs=model_select,
                outputs=[navigator_prompt_input, slider]
            )
            gallery = gr.Gallery(show_label=False)
            btn = gr.Button("Generate images")
            btn.click(
                generate_images_with_prompts,
                [prompt_input, navigator_prompt_input,slider,model_select],
                gallery
            )

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
# 创建其他Tab页面的内容（示例）
def chat_completion_translate():
    gr.Markdown("### Translate your text from one language to another")
    source_language = gr.Radio(['zh', "en"], label="Source Language")
    target_language = gr.Radio(["th", "en"], label="Target Language")
    sentence_input = gr.Textbox(label="Enter Sentence")
    output_text = gr.Textbox(label="Translated Sentence", interactive=False)
    submit_button = gr.Button("Translate")
    def translate(sentence, src_lan, tgt_lan):
        url = 'http://api.niutrans.com/NiuTransServer/translation?'
        data = {"from": src_lan, "to": tgt_lan, "apikey": os.getenv("Translate_key"), "src_text": sentence}
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

    submit_button.click(
        fn=translate,
        inputs=[sentence_input, source_language, target_language],
        outputs=output_text
    )


def other_tab_content_2():
    with gr.Column():
        gr.Markdown("### Another tab page for different functionalities.")
        # 添加更多的控件和功能

with gr.Blocks() as app:
    with gr.Tabs():
        with gr.TabItem("Chat & Image Generation"):
            chat_image_component()
        with gr.TabItem("Translate"):
            chat_completion_translate()
        with gr.TabItem("Other Tab 2"):
            other_tab_content_2()

if __name__ == "__main__":
    app.launch(server_port=7861)