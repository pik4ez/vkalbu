#!/usr/bin/env python3

import argparse
import configparser
import auth
import album
import track
from time import sleep

# pip3 install vk
# https://github.com/dimka665/vk
import vk

# set args
args_parser = argparse.ArgumentParser()
args_parser.add_argument(
        'albums_list',
        help='path to file containing albums list in json format'
        )
args_parser.add_argument(
        '--sleep',
        help='sleep time in seconds between vk api requests',
        type=int
        )
args = args_parser.parse_args()

# set sleep interval between vk api requests
SLEEP_INTERVAL = 1
if args.sleep:
    SLEEP_INTERVAL = args.sleep

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
            album_id = vkapi.audio.addAlbum(title=album_full_name)['album_id']

        tracks_for_album = []
        for track in tracks:
            track_name = track[0]
            track_length = track[1]
            track_query = track_api.Query(
                    artist=artist,
                    album=album_name,
                    title=track_name,
                    year=year,
                    length=track_length
                    )
            track_id = track_api.search(track_query)

            if (track_id):
                tracks_for_album.append(track_id)

            sleep(SLEEP_INTERVAL)

        if len(tracks_for_album):
            print('adding %d tracks to album %s:' % (
                len(tracks_for_album),
                album_full_name
                ))
            vkapi.audio.moveToAlbum(
                    album_id=album_id,
                    album_ids=tracks_for_album
                    )
