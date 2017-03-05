import pytest
import requests

from imgrabber import tasks
from pipeliner import Pipeline, task


def fetch_file(url):
    resp = requests.get(url)
    return resp.content


class TestSinglePipeline(object):
    """
    Test single pipeline for one url.
    """
    def test_image_save(self, tmpdir):
        folder = tmpdir
        img_url = 'https://www.w3schools.com/css/img_fjords.jpg'

        pipeline = Pipeline(
            tasks.fetch_url(),
            tasks.get_filename(),
            tasks.save_file(folder=folder.strpath, default_extension='.jpg'),
            url=img_url
        )
        pipeline.run(wait=True)

        filename = folder.join('img_fjords.jpg')

        assert filename.read() == fetch_file(img_url)


class TestMultiplePipelines(object):
    def test_multipipeline(self, tmpdir):

        @task(depends=['items'])
        def foreach(context, func):
            items = context.get('items')

            pipelines = []
            for item in items:
                pipeline = func(item)
                pipelines.append(pipeline)
                pipeline.run()

            context.current_pipeline.wait_for(pipelines)

        def spawn_pipeline(url):
            return Pipeline(
                tasks.fetch_url(),
                tasks.get_filename(),
                tasks.save_file(folder=tmpdir.strpath),
                url=url
            )

        Pipeline(
            foreach(spawn_pipeline),
            items=[
                'http://i.imgur.com/VGHoi.jpg',
                'http://i.imgur.com/UIcZyA4.png',
                'http://i.imgur.com/kCXV8yz.jpg',
            ]
        ).run(wait=True)

        f1 = tmpdir.join('VGHoi.jpg')
        f2 = tmpdir.join('UIcZyA4.png')
        f3 = tmpdir.join('kCXV8yz.jpg')

        assert f1.read() == fetch_file('http://i.imgur.com/VGHoi.jpg')
        assert f2.read() == fetch_file('http://i.imgur.com/UIcZyA4.png')
        assert f3.read() == fetch_file('http://i.imgur.com/kCXV8yz.jpg')
