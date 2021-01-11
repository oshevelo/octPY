from celery import Celery

from django.core.files.base import ContentFile

from PIL import Image
from io import BytesIO

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def resize(img_size, image_path):
    img = Image.open(image_path)
    img.thumbnail(img_size, Image.ANTIALIAS)

    outputIO = BytesIO()
    img.save(outputIO, format=img.format, quality=100)

    return {
        'name': '_thumb',
        'content': ContentFile(outputIO.getvalue()),
        'save': False,
    }