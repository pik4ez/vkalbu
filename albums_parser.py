import json

class AlbumsParser():
    """Parses albums list json string."""
    def parse_json(self, data):
        res = json.loads(data)
        if not self.is_valid(res):
            raise Exception('invalid albums list')
        return res['albums']


    """Validates albums list."""
    # TODO test
    def is_valid(self, res):
        if not isinstance(res, dict):
            return False
        if not res['albums']:
            return False

        for album in res['albums']:
            if not album['artist']:
                return False
            if not album['title']:
                return False
            if not album['tracks']:
                return False

            for track in album['tracks']:
                if not track['title']:
                    return False
                if not track['duration']:
                    return False

        return True
