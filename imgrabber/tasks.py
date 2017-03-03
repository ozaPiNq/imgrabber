import requests

from pipeliner import task


@task(depends=['url'], provides=['headers', 'data'])
def fetch_url(context):
    url = context.get('url')

    result = requests.get(url)

    context['headers'] = result.headers
    context['data'] = result.text

    return context


@task(depends=['data'])
def save_file(context):
    pass
