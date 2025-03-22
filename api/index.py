from svgwrite import Drawing
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

    response = requests.get('https://quotable.vercel.app/random').json()

    author = response['author']
    content = textwrap.wrap(response['content'])

    font_style = random.choice(['normal', 'italic', 'oblique'])
    font_weight = random.choice(['normal', 'bold', 'bolder', 'lighter'])

    draw = Drawing(size=(width + 'px', height + 'px'))

    dy = -0.6 * len(content) - 1.2
    for text in content:
        draw.add(
            draw.text(text,
                      dx=['0em'],
                      dy=[str(dy) + 'em'],
                      fill='#' + color,
                      font_size=size + 'pt',
                      font_style=font_style,
                      font_weight=font_weight,
                      text_anchor='middle',
                      x=['50%'],
                      y=['50%']))
        dy += 1.2
    dy += 1.2
    draw.add(
        draw.text('- {}'.format(author),
                  dx=['0em'],
                  dy=[str(dy) + 'em'],
                  fill='#' + color,
                  font_size=size + 'pt',
                  font_style=font_style,
                  font_weight=font_weight,
                  text_anchor='middle',
                  x=['50%'],
                  y=['50%']))

    return send_file(io.BytesIO(bytes(draw.tostring(), 'utf-8')),
                     'image/svg+xml',
                     max_age=0)
