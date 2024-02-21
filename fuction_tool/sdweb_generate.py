import requests
import random
import uuid
import base64
sd_api_params = {
  "prompt": "",
  "negative_prompt": "",
  "batch_size": 1,
  "steps": 30,
}

def Text2Img(prompt,negative_prompt,steps,batch_size):
    sd_api_params['prompt'] = prompt
    sd_api_params['negative_prompt'] = negative_prompt
    sd_api_params['steps'] = steps
    sd_api_params['batch_size'] = batch_size
    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img",json=sd_api_params)
    image_list = []
    for i in response.json()["images"]:
      rsa = uuid.uuid4()
      with open(f'D:\yuanlis_project\Aicontent\ChatCompletion\ChatCompletionWebDemo\generate_img\img_{str(rsa)}.png',
                "wb") as image_file:
        image_file.write(base64.b64decode(i))
        image_list.append(f"D:\yuanlis_project\Aicontent\ChatCompletion\ChatCompletionWebDemo\generate_img\img_{str(rsa)}.png")
    print(image_list)
    return image_list





if __name__ == '__main__':
    res = Text2Img("a cat","",20,1)
    print(res)