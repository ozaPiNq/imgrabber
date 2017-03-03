import re
import requests

from pipeliner import task


@task(depends=['url'], provides=['headers', 'data'])
def fetch_url(context):
    url = context.get('url')

    result = requests.get(url)

    context['headers'] = result.headers
    context['data'] = result.text


@task(depends=['url', 'headers'], provides=['filename'])
def get_filename(context):
    url = context.get('url')
    headers = context.get('headers', {})

    if 'Content-Disposition' in headers:
        cd = headers.get('Content-Disposition')
        if cd:
            match = re.search('filename="([^"]*)"', cd)
            if match:
                context['filename'] = match.group(1)

    if not context.get('filename'):
        context['filename'] = url.split('/')[-1]


@task(depends=['data'])
def save_file(context):
    pass
