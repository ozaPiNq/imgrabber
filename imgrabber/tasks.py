import os
import re
import uuid
import requests

from urlparse import urlparse
from pipeliner import task


@task(depends=['url'], provides=['headers', 'data'])
def fetch_url(context):
    """
    Fetch URL using HTTP GET request

    :param url: URL to be fetched

    :return: Returns HTTP headers and HTTP payload (data)
    """
    url = context.get('url')

    result = requests.get(url)

    context['headers'] = result.headers
    context['data'] = result.content


@task(depends=['url', 'headers'], provides=['filename'])
def get_filename(context):
    """
    Get filename from Content-Disposition header or URL

    :param url: fetched file url
    :param headers: fetched URL headers

    :return: file name. If none found it will be blank
    """
    url = context.get('url')
    headers = context.get('headers', {})

    cd = headers.get('Content-Disposition')
    if cd:
        match = re.search('filename="([^"]*)"', cd)
        if match:
            context['filename'] = match.group(1)

    if not context.get('filename'):
        parsed_url = urlparse(url)
        context['filename'] = parsed_url.path.split('/')[-1]


@task(depends=['data', 'filename'])
def save_file(context, folder, default_extension=''):
    """
    Save file to disk

    :param folder: folder for file
    :param default_extension: default extension for files with empty filenames
    :param filename: file name
    :param data: data to be saved to file
    """
    def random_name():
        """ For now it uses uuid.uuid4() """
        return str(uuid.uuid4())

    data = context['data']
    filename = context['filename']

    if not filename:
        filename = random_name() + default_extension

    abs_filename = os.path.join(folder, filename)

    with open(abs_filename, 'wb') as f:
        f.write(data)


@task(depends=['items'])
def foreach(context, func):
    """
    For each element in items starts new Pipeline, returned from func,
    then waits for pipelines to finish

    :param items: iterable of items
    :param func: function returning Pipeline object
    """
    items = context.get('items')

    pipelines = []
    for item in items:
        pipeline = func(item)
        pipelines.append(pipeline)
        pipeline.run()

    context.current_pipeline.wait_for(pipelines)


@task(depends=['filename'], provides=['items'])
def read_file(context):
    """
    Read lines from file with filename and stores them in items
    :param filename: file name to read
    :return: file lines
    """
    filename = context.get('filename')

    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.rstrip('\n'))

    context['items'] = lines
