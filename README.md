vkalbu
======

Creates albums in vk.com. Helps to create discographies.

Creates vk audio albums and fills it with songs. Uses json files as input.
Built on top of vk.com API v5.35.


Usage
-----

Create auth config and write your vk auth data there:

```
cp auth.ini.template auth.ini
# Paste your auth data
chmod 0400 auth.ini
```

You can get your page ID from your vk.com home page URI.
To get app id, create application and go to application settings page.

The simplest way to run vkalbu is to create albums list and run
the script similar to https://gist.github.com/pik4ez/bd628d53f2818574b683.

It uses https://github.com/pik4ez/dgrab.

Albums list is a file with one link to album per line.
Link to album is a link to page containing album data no the site
supported by dgrab (see dgrab docs). For example:

```
http://www.discogs.com/Judas-Priest-Screaming-For-Vengeance/master/26341
http://www.discogs.com/Judas-Priest-Defenders-Of-The-Faith/master/26183
http://www.allmusic.com/album/godsmack-mw0000042111
http://www.allmusic.com/album/faceless-mw0000023020
```

After albums list created, just run the starter script:

```
chmod +x /path/to/vkalbu_starter
/path/to/vkalbu_starter
```

You can write your own albums parser. In this case, get sample albums
list in vkalbu native format from file tests/fixtures/albums_list.json
and teach your parser to make similar output. Then feed vkalbu with it.

Something like this:

```
my_shiny_parser http://site.com/band/album.html > /some/tmp/file.json
/path/to/vkalbu.py /some/tmp/file.json
```


Tests
-----

```
cd path/to/vkalbu
./all_tests.sh
```
