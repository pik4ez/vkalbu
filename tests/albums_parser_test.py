import os
import unittest
import albums_parser

class AlbumsParserTest(unittest.TestCase):
    def test_parse_file(self):
        parser = albums_parser.AlbumsParser()
        file_path = os.path.dirname(__file__) + \
                '/fixtures/albums_list.json'
        result = parser.parse_file(file_path)
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

if __name__ == '__main__':
    unittest.main()
