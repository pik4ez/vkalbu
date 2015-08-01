from difflib import SequenceMatcher
from collections import namedtuple

class Track:
    SORT_DATE_ADD = 0
    SORT_DURATION = 1
    SORT_POPULARITY = 2

    RELEVANCY_INSTANT_TRESHOLD = 0.8

    RELEVANCY_TITLE = 0.4
    RELEVANCY_ARTIST = 0.2
    RELEVANCY_YEAR = 0.1
    RELEVANCY_LENGTH = 0.3

    Query = namedtuple('Query', ['artist', 'album', 'title', 'year', 'length'])
    VkTrack = namedtuple('Track', ['title', 'artist', 'length'])

    """Requires vk api object. """
    def __init__(self, vkapi):
        self.vkapi = vkapi


    """Searches for audio track.

    Returns vk track id if track were found.
    Returns None elsewhere.
    """
    def search(self, query):
        offset = 0
        count = 100
        best_match = (0, None, None)
        tracks = self.vkapi.audio.search(
                q=query.title,
                auto_complete=0,
                lyrics=0,
                performer_only=0,
                sort=self.SORT_POPULARITY,
                search_own=0,
                offset=offset,
                count=count
                )

        if not tracks['count']:
            raise Exception('failed to get tracks count')

        if not tracks['items']:
            raise Exception('failed to get tracks list')

        for track in tracks['items']:
            vk_track = self.VkTrack(
                    track['title'],
                    track['artist'],
                    track['duration']
                    )
            relevancy = self.get_relevancy(query, vk_track)
            if relevancy > self.RELEVANCY_INSTANT_TRESHOLD:
                return track['id']
            if relevancy > best_match[0]:
                best_match = (relevancy, track['id'], track)

        return best_match[1]


    def get_relevancy(self, query, track):
        relevancy = self.similar(query.title, track.title) * \
            self.RELEVANCY_TITLE

        if track.artist:
            relevancy = relevancy + (
                    self.similar(query.artist, track.artist) *
                    self.RELEVANCY_ARTIST
                    )

        if query.year and track.title.find(str(query.year)) != -1:
            relevancy = relevancy + self.RELEVANCY_YEAR

        if query.length and track.length:
            length_diff = abs(query.length - track.length)
            diff_penalty_per_second = self.RELEVANCY_LENGTH / 10
            diff_penalty = length_diff * diff_penalty_per_second
            if (diff_penalty < self.RELEVANCY_LENGTH):
                bonus = (self.RELEVANCY_LENGTH - diff_penalty)
                relevancy = relevancy + bonus

        return relevancy


    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
