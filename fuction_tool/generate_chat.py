from dotenv import load_dotenv, find_dotenv
from fuction_tool.sdweb_generate import Text2ImgDall,Text2Img
import os
import time
from openai import OpenAI
import gradio as gr
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
                avatar_images=(None, (os.path.join(os.path.dirname(__file__), r"D:\PythonProgram\ChatCompletionWebDemo\static\avatar1.png"))),
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