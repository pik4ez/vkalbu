class Track:
    """Requires vk api object. """
    def __init__(self, vkapi):
        self.vkapi = vkapi

    """Searches for audio track.

    Returns vk track id if track were found.
    Returns None elsewhere.
    """
    def search(self, artist, album, title, year=None, length=None):
        tracks = self.vkapi.audio.search(q=title)
        print(tracks)
        raise Exception('NOT IMPLEMENTED')
        return None
