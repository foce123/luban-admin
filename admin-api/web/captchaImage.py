# -*- coding: utf-8 -*- 
"""
@Author: 孟颖
@email: 652044581@qq.com
@date: 2023/4/13 13:36
@desc: 生成验证码
"""
import pathlib
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
from pathlib import Path


class CaptchaImage:

    def __init__(self, width=130, height=35, string_count=4, font_size=30, noise_line=3, noise_point=30):
        """
        :param width: 图片宽度
        :param height: 图片高度
        :param string_count: 验证码的数量
        :param font_size: 字体的大小
        :param noise_line: 噪声线的数量
        :param noise_point: 噪声点的数量
        """
        self.width = width
        self.height = height
        self.string_count = string_count
        self.font_size = font_size
        self.noise_line = noise_line
        self.noise_point = noise_point

    # 生成验证码
    def generate(self, width=120, height=35):
        image = self.background()
        captcha_string, image = self.draw_string(image)
        image: Image = self.noise(image)
        image = image.resize((width, height), resample=Image.BICUBIC)
        output_buffer = BytesIO()
        image.save(output_buffer, format='png')
        binary_data = output_buffer.getvalue()
        image_base64 = self.io2base64(binary_data)
        return captcha_string, image_base64

    # io转base64
    def io2base64(self, content: bytes):
        encode_data = base64.b64encode(content)
        return str(encode_data, encoding='utf-8')

    # 生成背景
    def background(self):
        background_color = (255, 255, 255)
        image = Image.new('RGB', (self.width, self.height), background_color)
        return image

    # 随机颜色
    def random_color(self):
        c1 = random.randint(0, 200)
        c2 = random.randint(0, 200)
        c3 = random.randint(0, 200)
        return c1, c2, c3

    # 生成随机字符串
    def random_string(self):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        return random.choice([random_num, random_low_alpha])

    # 合成文字
    def draw_string(self, image: Image):
        draw = ImageDraw.Draw(image)
        font_file = pathlib.Path.joinpath(Path(__file__).parent, "static/fontBold.ttf").as_posix()
        font = ImageFont.truetype(font=font_file, size=self.font_size)
        string_container = []
        for i in range(self.string_count):
            random_char = self.random_string()
            draw.text((10 + i * 30, -2), random_char, self.random_color(), font=font)
            string_container.append(random_char)
        captcha_string = "".join(string_container)
        return captcha_string, image

    # 生成噪声
    def noise(self, image: Image):

        draw = ImageDraw.Draw(image)
        # 噪声线
        for i in range(self.noise_line):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.random_color())

        # 噪声点
        for i in range(self.noise_point):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self.random_color())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.random_color())

        return image


if __name__ == '__main__':
    captcha = CaptchaImage()

    # 生成验证码图片和字符串
    captcha_string, image_base64 = captcha.generate(width=108, height=36)
