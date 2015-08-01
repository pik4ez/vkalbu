#!/usr/bin/env python3

import unittest
import track

class TrackTestCase(unittest.TestCase):
    def test_get_relevancy(self):
        track_api = track.Track(None)
        query = track_api.Query(
                'artist',
                'album',
                'title',
                1980,
                100
                )
        worst_track = track_api.VkTrack(
                'habahaba',
                'bubma',
                200
                )
        normal_track = track_api.VkTrack(
                'Title (1980)',
                None,
                103
                )
        perfect_track = track_api.VkTrack(
                'title (1980)',
                'artist',
                100
                )

        worst_relevancy = track_api.get_relevancy(query, worst_track)
        normal_relevancy = track_api.get_relevancy(query, normal_track)
        perfect_relevancy = track_api.get_relevancy(query, perfect_track)
        self.assertLess(worst_relevancy, 0.2)
        self.assertLess(normal_relevancy, 0.8)
        self.assertLess(worst_relevancy, normal_relevancy)
        self.assertGreater(perfect_relevancy, 0.8)

if __name__ == '__main__':
    unittest.main()
