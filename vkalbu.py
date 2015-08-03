#!/usr/bin/env python3

import sys
import select
import argparse
import configparser
import vkapi
import auth
import albums_parser
import album
import track


# Parse args.
usage = "vkalbu.py --file /path/to/albums_list.json\n" + \
        "cat /path/to/albums_list.json | vkalbu.py"
description="Discography creator for vk.com."
args_parser = argparse.ArgumentParser(
        description=description,
        usage=usage
        )
args_parser.add_argument(
        '--albums-file',
        help='path to file containing albums list in json format'
        )
args_parser.add_argument(
        '--timeout',
        help='vk api requests timeout in seconds',
        type=int
        )
args_parser.add_argument(
        '--sleep',
        help='sleep time in seconds between vk api requests',
        type=int
        )
args = args_parser.parse_args()

# Read config.
config = configparser.ConfigParser()
config.read('auth.ini')

# Get vk api object.
token = auth.auth(config['user']['login'], config['user']['password'])
vk = vkapi.VkApi(
        token=token,
        sleep_interval=args.sleep,
        request_timeout=args.timeout
        )


# Parse and create albums, search for tracks and add it to albums.
if __name__ == '__main__':
    # Get albums data from stdin or albums file
    albparser = albums_parser.AlbumsParser()
    albums = None
    if select.select([sys.stdin,],[],[],0.0)[0]:
        raw_albums = sys.stdin.readlines()
        albums = albparser.parse_json(raw_albums)
    elif args.albums_file:
        albums = albparser.parse_file(args.albums_file)

    if not albums:
        print('empty albums list, exit')
        sys.exit()

    album_api = album.Album(vk)
    track_api = track.Track(vk)

    for album in albums:
        album['full_name'] = '%s — %s (%d)' % (
                album['artist'],
                album['title'],
                album['year']
                )
        album_id = album_api.get_id_by_title(album['full_name'])
        if not album_id:
            print('creating album "%s"' % album['full_name'])
            added_album = vk.audio.addAlbum(
                    title=album['full_name']
                    )
            album_id = added_album['album_id']
        else:
            print('album "%s" exists, reusing' % album['full_name'])

        tracks_for_album = []
        for track in reversed(album['tracks']):
            track_query = track_api.Query(
                    artist=album['artist'],
                    album=album['title'],
                    title=track['title'],
                    year=album['year'],
                    length=track['duration']
                    )
            print('searching for track:')
            print(track_query)
            found_track = track_api.search(track_query)

            if (found_track):
                print('found track %d "%s"' % (
                    found_track['id'],
                    found_track['title']
                    ))
                saved_track_id = vk.audio.add(
                        audio_id=found_track['id'],
                        owner_id=found_track['owner_id']
                        )
                if saved_track_id:
                    tracks_for_album.append(saved_track_id)

        if len(tracks_for_album):
            print('adding %d tracks to album "%s"' % (
                len(tracks_for_album),
                album['full_name']
                ))
            audio_ids = ",".join(str(i) for i in tracks_for_album)
            print('audio_ids %s' % audio_ids)
            vk.audio.moveToAlbum(
                    album_id=album_id,
                    audio_ids=audio_ids
                    )
