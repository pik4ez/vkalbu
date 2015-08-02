import json

class AlbumsParser():
    def parse_file(self, file_path):
        with open(file_path) as fp:
            res = json.load(fp)
            if res['albums']:
                return res['albums']

        raise Exception('failed to parse albums')
