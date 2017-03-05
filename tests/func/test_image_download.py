import pytest
import requests

from imgrabber import tasks
from pipeliner import Pipeline


class TestSinglePipeline(object):
    """
    Test single pipeline for one url.
    """
    def fetch_file(self, url):
        resp = requests.get(url)
        return resp.content

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

        assert filename.read() == self.fetch_file(img_url)
