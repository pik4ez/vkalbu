#!/usr/bin/env python3

import configparser
import auth
import vk
import album
import track

# read config
config = configparser.ConfigParser()
config.read('auth.ini')

# get token
token = auth.auth(config['user']['login'], config['user']['password'])

if __name__ == '__main__':
    # authorize
    vkapi = vk.API(
            access_token=token
            )

    album_api = album.Album(vkapi)

    # TODO read albums list
    # albums = album_api.parse_albums_file(albums_file)
    albums = [
            ('Stone Temple Pilots', 'Core', 2010, [
                    ('Dead & Bloated', 5 * 60 + 10),
                    ('Sex Type Thing', 3 * 60 + 38),
                ]),
            ]

    track_api = track.Track(vkapi)
    for album in albums:
        artist = album[0]
        album_name = album[1]
        year = album[2]
        tracks = album[3]
        album_full_name = '%s — %s (%d)' % (artist, album_name, year)
        album_id = album_api.get_id_by_title(album_full_name)
        if not album_id:
            print('creating album %s' % (album_full_name))
            album_id = vkapi.audio.addAlbum(title=album_full_name)['album_id']

        for track in tracks:
            track_name = track[0]
            track_length = track[1]
            track_id = track_api.search(
                    artist=artist,
                    album=album_name,
                    title=track_name,
                    year=year,
                    length=track_length
                    )
            print('track_id %r' % (track_name))

            # TODO find track
            # track = vkmus.find(album_name, track_name)

            # TODO add to my music
            # vkmus.add_to_my_music(track)

            # TODO add to album
            # vkmus.add_to_album(track, album)
