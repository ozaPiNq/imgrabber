import os
import argparse

from imgrabber import tasks
from pipeliner import Pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="File of URL to fetch")
    parser.add_argument("--folder", help="Folder to save files to. "
                                         "Defaults to CWD")
    args = parser.parse_args()

    folder = args.folder or os.getcwd()
    start_pipeline(args.input_file, folder)


def start_pipeline(input_file, folder):
    def file_processing_pipeline(url):
        return Pipeline(
            tasks.fetch_url(),
            tasks.get_filename(),
            tasks.save_file(folder=folder),
            url=url
        )

    Pipeline(
        tasks.read_file(input_file=input_file),
        tasks.foreach(file_processing_pipeline)
    ).run(wait=True)


if __name__ == '__main__':
    main()
