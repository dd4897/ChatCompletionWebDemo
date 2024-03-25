import gradio as gr
from fuction_tool.generate_chat import chat_image_component
from fuction_tool.translate import chat_completion_translate
from fuction_tool.generate_dramascript import dramagenerate
import matplotlib
# matplotlib.use('TkAgg')

with gr.Blocks() as app:
    with gr.Tabs():
        with gr.TabItem("DramaGenerate"):
            dramagenerate()
        with gr.TabItem("Chat & Image Generation"):
            chat_image_component()
        with gr.TabItem("Translate"):
            chat_completion_translate()


if __name__ == "__main__":
    app.launch(server_port=7861)