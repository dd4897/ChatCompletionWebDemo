import requests
import uuid
import base64

img_path = f"D:\PythonProgram\ChatCompletionWebDemo\generate_img\img_"
dall_url = "https://api.xiabb.chat/chatapi/drawing/task"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6NjAyOTcyNTQ4NzQ4MjEsIkFjY291bnQiOiJkZGw0ODk3QDE2My5jb20iLCJBY2NvdW50VHlwZSI6MSwiTmlja05hbWUiOiJkZOmaj-mjjiIsIkxvZ2luTW9kZSI6MiwiaWF0IjoxNzA5MjcyMTY2LCJuYmYiOjE3MDkyNzIxNjYsImV4cCI6MTcwOTk5MjE2NiwiaXNzIjoiQUlUb29scyIsImF1ZCI6IkFJVG9vbHMifQ.fL2cO_ExJU2ZSGCWf4PUoVNS0fSxt-hy0m8T0nApthE"
}


# sdwebuiapi text to img
def Text2Img(prompt, negative_prompt, steps, batch_size):
    sd_api_params = {
        "prompt": "",
        "negative_prompt": "",
        "batch_size": 1,
        "steps": 30,
    }
    sd_api_params['prompt'] = prompt
    sd_api_params['negative_prompt'] = negative_prompt
    sd_api_params['steps'] = steps
    sd_api_params['batch_size'] = batch_size
    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=sd_api_params)
    result_list = save_images(response.json()["images"])
    return result_list


# dall-3/dall-2 api
def Text2ImgDall(prompt):
    dall_api_params = {
        "model": "dall-e-3",
        "size": 100,
        "n": 1,
        "quality": "standard",
        "prompt": ""
    }
    dall_api_params['prompt'] = prompt
    print(dall_api_params)
    response = requests.post(dall_url, headers=headers, json=dall_api_params)
    result = response.json()
    print(result)
    image_list = result['result']['imageUrls']
    result_list = save_images(image_list)
    return result_list


def save_images(image_list):
    # base64 or https url
    result_list = []
    if image_list[0].startswith("https://"):
        return image_list
    for i in image_list:
        rsa = uuid.uuid4()
        with open(img_path + f"{str(rsa)}.png",
                  "wb") as image_file:
            image_file.write(base64.b64decode(i))
            result_list.append(
                img_path + f"{str(rsa)}.png")
    return result_list
