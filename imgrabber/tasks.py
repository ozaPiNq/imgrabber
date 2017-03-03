import re
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
    context['data'] = result.text


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
def save_file(context, folder):
    """
    Save file to disk
    :param folder: folder for file
    :param filename: file name
    :param data: data to be saved to file
    :return:
    """
    pass
