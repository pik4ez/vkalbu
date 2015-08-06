import os
import unittest
import albums_parser

class AlbumsParserTest(unittest.TestCase):
    def test_parse_json(self):
        parser = albums_parser.AlbumsParser()
        file_path = os.path.dirname(__file__) + \
                '/fixtures/albums_list.json'
        with open(file_path, 'r') as f:
            data = f.read()
        f.close()
        result = parser.parse_json(data)
        expected = [
            {
                "artist": "SomeArtist",
                "title": "SomeAlbum",
                "year": 1970,
                "tracks": [
                    {"title": "SomeTrackOne", "duration": 100},
                    {"title": "SomeTrackTwo", "duration": 200}
                ]
            },
            {
                "artist": "AnotherArtist",
                "title": "AnotherAlbum",
                "year": 1970,
                "tracks": [
                    {"title": "AnotherTrackOne", "duration": 100},
                    {"title": "AnotherTrackTwo", "duration": 200}
                ]
            }
        ]
        self.assertEqual(result, expected)


        # TODO implement
        def test_is_valid(self):
            pass

if __name__ == '__main__':
    unittest.main()
