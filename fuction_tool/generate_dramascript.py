import os
import gradio as gr
from dotenv import load_dotenv,find_dotenv
import time
from openai import OpenAI
_ = load_dotenv(find_dotenv())
openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
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

def dramagenerate():
    with gr.Blocks():
        chatbot = gr.Chatbot(
            [],
			height=1000,
            bubble_full_width=False,
            avatar_images=(None, (
                os.path.join(os.path.dirname(__file__), r"D:\PythonProgram\ChatCompletionWebDemo\static\avatar1.png"))),
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

