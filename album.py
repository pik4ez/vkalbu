class Album:
    """Requires vk api object. """
    def __init__(self, vkapi):
        self.vkapi = vkapi
        self.max_offset = 1000

    """Tries to find album by title.

    Returns vk album id if album were found.
    Returns None elsewhere.
    """
    def get_id_by_title(self, title):
        step = 100
        offset = 0
        albums_count = 1
        while offset < albums_count and offset < self.max_offset:
            albums = self.vkapi.audio.getAlbums(count=step, offset=offset)
            if not albums['count']:
                raise Exception('failed to get albums count')
            albums_count = albums['count']
            if not albums['items']:
                raise Exception('failed to get albums items')
            for album in albums['items']:
                if album['title'] == title:
                    return album['id']
            offset += step
        return None
