#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

_path = os.path.dirname(os.path.relpath(__file__))
_save_path = os.path.join(_path, '..', 'AUTHORS.md')


header = """\

**Lead by**: [seekheart](http://github.com/seekheart)

"""
url = "https://api.github.com/repos/seekheart/show_watchdog/contributors"

r = requests.get(url)
contributors = r.json()

lines = []
for i in contributors:
    url = i.get('html_url')
    username = i.get('login')
    lines.append('* [{}]({}) '.format(username, url))

text = header + '\n'.join(lines)

with open(_save_path, 'w') as f:
    f.write(text)
