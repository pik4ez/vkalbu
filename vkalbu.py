#!/usr/bin/env python3

import os
import sys
import argparse
import configparser
import vk_api
import albums_parser
import album
import track
import subprocess


# Parse args.
usage = "vkalbu /path/to/albums_list.json"
description="Discography creator for vk.com."
args_parser = argparse.ArgumentParser(
        description=description,
        usage=usage
        )
args_parser.add_argument(
        'albums_file',
        help='path to file containing albums list in json format'
        )
args_parser.add_argument(
        '--timeout',
        help='vk api requests timeout in seconds',
        type=int,
        default=3
        )
args_parser.add_argument(
        '--sleep',
        help='sleep time in seconds between vk api requests',
        type=int,
        default=1
        )
args = args_parser.parse_args()


"""Returns albums list json from specified file."""
def get_albums_list():
    # Try to read list from file.
    if args.albums_file:
        with open(args.albums_file) as fp:
            albums = fp.read()
            return albums
    return None


"""Handles captcha request."""
def captcha_handler(captcha):
    print("Captcha %s" % captcha.get_url())
    key = input("Enter captcha code: ").strip()
    return captcha.try_again(key)


# Create vk.com albums, search for tracks and add it to albums.
if __name__ == '__main__':
    # Get albums data from stdin or albums file
    albparser = albums_parser.AlbumsParser()
    albums = get_albums_list()
    if not albums:
        print('Failed to read albums list. Albums file not provided.')

    if not albums:
        print('Empty albums list, exit.')
        sys.exit()

    albums = albparser.parse_json(albums)

    # Read config.
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/auth.ini')

    # Get vk api object.
    vk = vk_api.VkApi(
            login=config['user']['login'],
            password=config['user']['password'],
            app_id=config['app']['id'],
            scope='audio',
            captcha_handler=captcha_handler
            )

    # Authorize.
    try:
        vk.authorization()
    except vk_api.AuthorizationError as e:
        print(e)
        sys.exit()

    # Init APIs for albums and tracks.
    album_api = album.Album(vk)
    track_api = track.Track(vk)

    # Process provided albums.
    for album in albums:
        # Create album if doesn't exist.
        album['full_name'] = '%s — %s (%d)' % (
                album['artist'],
                album['title'],
                album['year']
                )
        album_id = album_api.get_id_by_title(album['full_name'])
        if not album_id:
            print('Creating album "%s".' % album['full_name'])
            m_args = {
                    'title': album['full_name']
                    }
            added_album = vk.method('audio.addAlbum', m_args)
            album_id = added_album['album_id']
        else:
            print('album "%s" exists, reusing' % album['full_name'])

        # Find tracks, collect their information.
        tracks_for_album = []
        for track in reversed(album['tracks']):
            track_query = track_api.Query(
                    artist=album['artist'],
                    album=album['title'],
                    title=track['title'],
                    year=album['year'],
                    length=track['duration']
                    )
            print('Searching for track:')
            print(track_query)
            found_track = track_api.search(track_query)

            if (found_track):
                print('Found track %d "%s"' % (
                    found_track['id'],
                    found_track['title']
                    ))
                m_args = {
                        'audio_id': found_track['id'],
                        'owner_id': found_track['owner_id']
                        }
                saved_track_id = vk.method('audio.add', m_args)
                if saved_track_id:
                    tracks_for_album.append(saved_track_id)

        # Add all the found tracks into album at once.
        if len(tracks_for_album):
            print('Adding %d tracks to album "%s".' % (
                len(tracks_for_album),
                album['full_name']
                ))
            audio_ids = ",".join(str(i) for i in tracks_for_album)
            print('Audio_ids %s.' % audio_ids)
            m_args = {
                    'album_id': album_id,
                    'audio_ids': audio_ids
                    }
            vk.method('audio.moveToAlbum', m_args)
            print('Done.')
