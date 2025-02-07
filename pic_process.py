import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def image2base64(image_path, quality=70):
    with Image.open(image_path) as img:
        buffer = BytesIO()
        img.save(buffer, format=img.format, quality=quality)
        img_bytes = buffer.getvalue()
        base64_encoded = base64.b64encode(img_bytes).decode('utf-8')
        return base64_encoded

def base642image(base64_string):
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_bytes))
    return img

def process_images(pic_list, w_limit = 1926081700):
    max_width = 0
    max_height = 0
    for pic in pic_list:
        width, height = pic.size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height
    resized_pics = []
    for pic in pic_list:
        resized_pics.append(pic.resize((max_width, max_height), Image.Resampling.LANCZOS))
    num_images = len(resized_pics)
    if num_images < 10:
        total_width = max_width * num_images
        total_height = max_height
    else:
        num_rows = (num_images + 9) // 10
        total_width = max_width * 10
        total_height = max_height * num_rows
    if total_width > w_limit:
        scale_factor = w_limit / total_width
        max_width = int(max_width * scale_factor)
        max_height = int(max_height * scale_factor)
        resized_pics = [pic.resize((max_width, max_height), Image.Resampling.LANCZOS) for pic in resized_pics]
        if num_images < 10:
            total_width = max_width * num_images
            total_height = max_height
        else:
            num_rows = (num_images + 9) // 10
            total_width = max_width * 10
            total_height = max_height * num_rows
    combined_image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
    if num_images < 10:
        for i, pic in enumerate(resized_pics):
            x = i * max_width
            y = 0
            pic = pic.convert('RGBA')
            combined_image.paste(pic, (x, y))
    else:
        for i, pic in enumerate(resized_pics):
            row = i // 10
            col = i % 10
            x = col * max_width
            y = row * max_height
            pic = pic.convert('RGBA')
            combined_image.paste(pic, (x, y))

    return combined_image

def merge_images(background_image, cover_image):
    background_image = background_image.convert('RGBA')
    cover_image = cover_image.convert('RGBA')
    bg_width, bg_height = background_image.size
    resized_cover = cover_image.resize((bg_width, bg_height), Image.Resampling.LANCZOS)
    result_image = Image.new('RGBA', (bg_width, bg_height))
    result_image.paste(background_image, (0, 0))
    result_image.paste(resized_cover, (0, 0), mask=resized_cover.split()[3])
    return result_image

def note_image(image, text, color=(255, 0, 0), fonts='times.ttf', reduction=1.5):
    try:
        width, height = image.size
        draw = ImageDraw.Draw(image)
        font_size = int(min(width, height) / reduction)
        font = ImageFont.truetype(fonts, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), text, font=font, fill=color)
        return image
    except Exception as e:
        return None

def change_color(image, color):
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if a != 0:
                pixels[x, y] = (*color, a)
    return image