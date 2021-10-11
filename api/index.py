from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from flask import Flask, request, send_file

import io
import os
import random
import requests
import textwrap

app = Flask(__name__)


@app.route('/api')
def view_func():
    color = request.args.get('color', os.getenv('DEFAULT_COLOR'))
    height = request.args.get('height', os.getenv('DEFAULT_HEIGHT'))
    size = request.args.get('size', os.getenv('DEFAULT_SIZE'))
    width = request.args.get('width', os.getenv('DEFAULT_WIDTH'))

    response = requests.get('https://api.quotable.io/random').json()

    quote = '{}\n\n- {}'.format('\n'.join(textwrap.wrap(response['content'])),
                                response['author'])

    image = Image.new('RGBA', (int(width), int(height)))

    font = ImageFont.truetype(random.choice(font_manager.findSystemFonts()),
                              int(size))

    draw = ImageDraw.Draw(image)
    multiline_textsize = draw.multiline_textsize(quote, font)
    draw.multiline_text((image.size[0] / 2 - multiline_textsize[0] / 2,
                         image.size[1] / 2 - multiline_textsize[1] / 2),
                        quote,
                        '#' + color,
                        font,
                        align='center')

    bytes = io.BytesIO()
    image.save(bytes, 'png')
    bytes.seek(0)
    return send_file(bytes, 'image/png')
