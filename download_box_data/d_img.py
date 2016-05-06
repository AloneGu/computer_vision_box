import os
content = open('index.html').read()
content = eval(content)
print content
for d in content:
    if 'img' in d['name']:
        try:
            cmd = 'wget -P ./imgs {}'.format('http://52.25.251.198/files/bbox_imgs/20-00/'+d['name'])
            os.system(cmd)
        except:
            pass