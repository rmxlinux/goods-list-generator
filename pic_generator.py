import json
import pic_process
from PIL import Image

def generate(path, w_limit=1926081700, text_color=(255, 0, 0), banned_img='banned_1.png', fonts='times.ttf', reduction=1.5):
    path = str(path)
    if path.lower().find('.png') == -1:
        path += '.png'
    with open('default.flf', 'rb') as f:
        raw_data = f.read()
        json_str = raw_data.decode('utf-8')
        data = json.loads(json_str)
    pic_list = []
    if text_color != (255, 0, 0):
        banned_icon = pic_process.change_color(Image.open(banned_img), text_color)
    else:
        banned_icon = Image.open(banned_img)
    for i in data["data"]:
        if i['count'] <= 0:
            pic_list.append(pic_process.merge_images(pic_process.base642image(i['base64']), banned_icon))
        else:
            pic_list.append(pic_process.note_image(pic_process.base642image(i['base64']), str(i['count']), color=text_color, fonts=fonts, reduction=reduction))
    if path.find('~return') != -1:
        return pic_process.process_images(pic_list, w_limit)
    else:
        pic_process.process_images(pic_list, w_limit).save(path)