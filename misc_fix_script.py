"""
Script that I ran to fix a bunch of the summaries, titles, and tags

It ended up being faster to fix the rest of them manually, so this is mostly
of archeological significance
"""


import steve.util
cfg = steve.util.get_project_config()
data = steve.util.load_json_files(cfg)
from datetime import datetime
import re
# We'll try to extract the MP number from the titles a couple of different ways
title_re1 = re.compile('^(.+) #(MP..).*$')
title_re2 = re.compile('^Montreal Python (\d+) (\w+ \w+) (.+)$')
for filename, contents in data:
    contents['copyright_text'] = "CC BY 3.0"
    match1 = title_re1.match(contents['title'])
    match2 = title_re2.match(contents['title'])
    if 'Oct. 22' in contents['summary']:
        prefix = "Montreal, Oct. 22, 2012 - "
        if contents['summary'].startswith(prefix):
            contents['summary'] = contents['summary'][len(prefix):]
        contents['recorded'] = datetime(2012, 10, 22).isoformat()
        contents['tags'] = ['MP32']
    elif match1:
        author_regex = re.compile('.+ - ((\S+ )*\S+) pr.se')
        match = author_regex.match(contents['summary'])
        if match:
            speaker, x = match.groups()
            contents['speakers'].append(speaker)
        title, tag = match1.groups()
        contents['tags'] = [tag]
        contents['title'] = title
    elif match2:
        number, speaker, subject = match2.groups()
        tag = "MP%02d" % int(number)
        contents['title'] = subject
        contents['speakers'].append(speaker)
        contents['tags'] = [tag]
    elif 'Introduction' in contents['title']:
        contents['tags'] = ['Tutorials']
    print contents['title'], 'by', contents['speakers'], 'tags', contents['tags']
    #print "Summary:", contents['summary']

steve.util.save_json_files(cfg, data)