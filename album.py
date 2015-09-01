class Album:
    """Requires vk api object. """
    def __init__(self, vk):
        self.vk = vk

    """Tries to find album by title.

    Returns vk album id if album were found.
    Returns None elsewhere.
    """
    def get_id_by_title(self, title):
        step = 100
        max_offset=1000
        offset = 0
        albums_count = 1
        while offset < albums_count and offset < max_offset:
            m_args = {
                    'count': step,
                    'offset': offset
                    }
            albums = self.vk.method('audio.getAlbums', m_args)
            if not albums['count']:
                raise Exception('failed to get albums count')
            albums_count = albums['count']
            if not albums['items']:
                raise Exception('failed to get albums list')
            for album in albums['items']:
                if album['title'] == title:
                    return album['id']
            offset += step
        return None
