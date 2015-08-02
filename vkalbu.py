#!/usr/bin/env python3

import sys
import argparse
import configparser
import auth
import albums_parser
import album
import track
from time import sleep

# pip3 install vk
# https://github.com/dimka665/vk
import vk

# set args
args_parser = argparse.ArgumentParser()
args_parser.add_argument(
        'albums_file',
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

if __name__ == '__main__':
    albums = albums_parser.AlbumsParser().parse_file(args.albums_file)
    if not albums:
        print('empty albums list, exit')
        sys.exit()

    # authorize
    token = auth.auth(config['user']['login'], config['user']['password'])
    vkapi = vk.API(access_token=token, api_version='5.35')

    album_api = album.Album(vkapi)

    track_api = track.Track(vkapi)
    for album in albums:
        album['full_name'] = '%s — %s (%d)' % (
                album['artist'],
                album['title'],
                album['year']
                )
        album_id = album_api.get_id_by_title(album['full_name'])
        if not album_id:
            print('creating album "%s"' % album['full_name'])
            added_album = vkapi.audio.addAlbum(
                    title=album['full_name']
                    )
            album_id = added_album['album_id']
        else:
            print('album "%s" exists, reusing' % album['full_name'])

        tracks_for_album = []
        for track in album['tracks']:
            track_query = track_api.Query(
                    artist=album['artist'],
                    album=album['title'],
                    title=track['title'],
                    year=album['year'],
                    length=track['duration']
                    )
            found_track = track_api.search(track_query)

            if (found_track):
                print('found track %d "%s"' % (
                    found_track['id'],
                    found_track['title']
                    ))
                saved_track = vkapi.audio.add(
                        audio_id=found_track['id'],
                        owner_id=config['user']['id']
                        )
                print(saved_track)
                raise Exception('NOT IMPLEMENTED')
                if saved_track_id:
                    tracks_for_album.append(saved_track_id)

            sleep(SLEEP_INTERVAL)

        if len(tracks_for_album):
            print('adding %d tracks to album "%s"' % (
                len(tracks_for_album),
                album['full_name']
                ))
            audio_ids = ",".join(str(i) for i in tracks_for_album)
            print('audio_ids %s' % audio_ids)
            vkapi.audio.moveToAlbum(
                    album_id=album_id,
                    audio_ids=audio_ids
                    )
