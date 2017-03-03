from imgrabber import tasks


class TestFetchUrl(object):
    def test_fetches_url(self, context):
        context['url'] = 'https://www.w3schools.com/css/trolltunga.jpg'

        task = tasks.fetch_url()

        new_context = task(context)

        assert new_context['data']
        assert new_context['headers']
