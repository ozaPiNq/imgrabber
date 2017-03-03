from imgrabber import tasks


class TestFetchUrl(object):
    def test_fetches_url(self, context, requests_get):
        expected_response = {
            'text': 'sample_data',
            'headers': {
                'Server': 'mocked_server',
                'Content-Type': 'image/jpeg'
            }
        }
        requests_get(expected_response)

        context['url'] = 'https://www.w3schools.com/css/trolltunga.jpg'

        new_context = tasks.fetch_url()(context)

        assert new_context['data'] == expected_response['text']
        assert new_context['headers'] == expected_response['headers']
