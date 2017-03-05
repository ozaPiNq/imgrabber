import pytest

from imgrabber import tasks
from pipeliner import Pipeline, task
from mock import MagicMock


class TestFetchUrl(object):
    def test_fetches_url(self, context, requests_get):
        expected_response = {
            'content': 'sample_data',
            'headers': {
                'Server': 'mocked_server',
                'Content-Type': 'image/jpeg'
            }
        }
        requests_get(expected_response)

        context['url'] = 'https://www.w3schools.com/css/trolltunga.jpg'

        new_context = tasks.fetch_url()(context)

        assert new_context['data'] == expected_response['content']
        assert new_context['headers'] == expected_response['headers']


class TestGetFilename(object):
    @pytest.mark.parametrize("url,expected_filename", [
        ('http://example.com/somefile.jpg',             'somefile.jpg'),
        ('http://example.com/setup.exe',                'setup.exe'),
        ('http://example.com/s/a/w/e/r/t/file.txt',     'file.txt'),
        ('http://example.com/index.php',                'index.php'),
        ('http://example.com/',                         ''),
        ('http://example.com',                          ''),
    ])
    def test_get_filename_from_url(self, context, url, expected_filename):
        context['url'] = url

        new_context = tasks.get_filename()(context)

        assert new_context['filename'] == expected_filename

    @pytest.mark.parametrize("cd, expected_filename ", [
        ('inline',                                          'picturename.jpg'),
        ('attachment',                                      'picturename.jpg'),
        ('attachment; filename="pic.jpg"',                  'pic.jpg'),
        ('form-data; name="fieldName"',                     'picturename.jpg'),
        ('form-data; name="fieldName"; filename="pic.jpg"', 'pic.jpg'),
    ])
    def test_get_filename_from_content_disposition_header(self, context, cd,
                                                          expected_filename):
        context['headers'] = {'Content-Disposition': cd}
        context['url'] = 'http://localhost/picturename.jpg'

        new_context = tasks.get_filename()(context)

        new_context['filename'] == expected_filename


class TestSaveFile(object):
    def test_file_with_filename(self, context, tmpdir):
        context['data'] = b'test_data'
        context['filename'] = 'simple_file.txt'

        target_dir = tmpdir.mkdir('images')
        task = tasks.save_file(folder=target_dir.strpath)

        task(context)

        assert target_dir.join(context['filename']).read() == context['data']

    def test_file_without_filename(self, context, tmpdir):
        context['data'] = b'test_data'
        context['filename'] = ''

        target_dir = tmpdir.mkdir('images')
        task = tasks.save_file(folder=target_dir.strpath,
                               default_extension='.jpg')

        task(context)

        created_file = target_dir.listdir()[0]
        assert created_file.read() == context['data']

    def test_folder_not_found(self, context, tmpdir):
        context['data'] = b'test_data'
        context['filename'] = 'test_pic.jpg'

        target_dir = tmpdir.join('images')
        task = tasks.save_file(folder=target_dir.strpath,
                               default_extension='.jpg')

        with pytest.raises(IOError) as exc_info:
            task(context)

        assert exc_info.value.errno == 2

    @pytest.mark.xfail
    def test_folder_access_denied(self, context):
        assert 0, 'write the test'


class TestForeach(object):
    def test_foreach(self):
        mock_func1 = MagicMock()
        mock_func2 = MagicMock()

        @task()
        def test_func(context):
            cb = context.get('cb')
            cb()

        def create_pipeline(item):
            return Pipeline(test_func(), cb=item)

        Pipeline(
            tasks.foreach(create_pipeline),
            items=[mock_func1, mock_func2]
        ).run(wait=True)

        assert mock_func1.called
        assert mock_func2.called
