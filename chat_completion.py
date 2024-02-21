import random
import gradio as gr
import os
import time
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import requests
import matplotlib
matplotlib.use('TkAgg')
_ = load_dotenv(find_dotenv())
openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
url = "https://api.xiabb.chat/chatapi/drawing/task"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6NjAyOTcyNTQ4NzQ4MjEsIkFjY291bnQiOiJkZGw0ODk3QDE2My5jb20iLCJBY2NvdW50VHlwZSI6MSwiTmlja05hbWUiOiJkZOmaj-mjjiIsIkxvZ2luTW9kZSI6MiwiaWF0IjoxNzA4MzA2NTM3LCJuYmYiOjE3MDgzMDY1MzcsImV4cCI6MTcwOTAyNjUzNywiaXNzIjoiQUlUb29scyIsImF1ZCI6IkFJVG9vbHMifQ.uJ_bo82Sl7CC3cygvZ1A6U0dBo0x3EJNXAzQHMND7SU"
}


def fake_gan(prompt):
    data = {
        "model": "dall-e-3",
        "size": 100,
        "n": 1,
        "quality": "standard",
        "prompt": "黄昏的街道"
    }
    data['prompt'] = prompt
    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    images = [
        (random.choice(res['result']['imageUrls']), f"U 0")
    ]
    return images


def generate_images_with_prompts(prompt, navigator_prompt, model_choice):
    return fake_gan(prompt)


def select_model(model_choice):
    return fake_gan()


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


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                bubble_full_width=False,
                avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.jpg"))),
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
            prompt_input = gr.Textbox(placeholder="Enter prompt for image generation", label="Image Prompt")
            navigator_prompt_input = gr.Textbox(placeholder="Enter navigator prompt", label="Navigator Prompt")

            gallery = gr.Gallery(label="Generated images", show_label=False, elem_id="gallery", object_fit="contain",
                                 height="auto")

            model_select = gr.Dropdown(choices=["Model 1", "Model 2", "Model 3"], label="Choose a Model")
            btn = gr.Button("Generate images")
            btn.click(
                generate_images_with_prompts,
                [prompt_input, navigator_prompt_input, model_select],
                gallery
            )
demo.queue()
if __name__ == "__main__":
    demo.launch()
