vkalbu
======

Creates albums in vk.com. Helps to create discographies.

Creates vk audio albums and fills it with songs. Uses json files as input.
Built on top of vk.com API v5.35.


Usage
-----

Get vk.com auth token (described here: https://vk.com/dev/auth_sites).
Paste it to auth.py (temporary, should be fixed).

```
chmod 0400 auth.py
```

Create auth config and write your vk auth data there:

```
cp auth.ini.template auth.ini
# edit file
chmod 0400 auth.ini
```

Create albums list. Find sample in tests/fixtures/albums_list.json.
Run vkalbu:

```
./vkalbu.py /path/to/albums_list.json
```

Inline json can be passed to STDIN:

```
echo '{"albums": [ <albums list here> ]}' | ./vkalbu.py
```

Some kind of parser can be used to prepare albums list in proper format.
Luckily enough, dgrab lives in neighbour repo, check it out:
https://github.com/pik4ez/dgrab.

Running vkalbu with dgrab:

```
./dgrab.py http://www.allmusic.com/album/stone-temple-pilots-mw0001975741 | ./vkalbu.py
```


Tests
-----

```
cd path/to/vkalbu
./all_tests.sh
```
