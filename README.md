vkmus
=====

Creates discographies in vk.com.

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

Create albums list. Get sample in tests/fixtures/albums_list.json.
Run vkmus:

```
vkmus.py path/to/albums_list.json
```


Tests
-----

```
cd path/to/vkmus
./all_tests.sh
```
