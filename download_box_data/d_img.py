import os
content = open('index.html').read()
content = eval(content)
print content
for d in content:
    if 'img' in d['name']:
        try:
            cmd = 'wget -P ./org_imgs {}'.format('http://52.25.251.198/files/imgs/20-00/'+d['name'])
            tmp_s = d['name']
            tmp_s = tmp_s.replace('.jpg','')
            tmp_s = tmp_s.replace('img_','')
            print tmp_s
            if int(tmp_s)<=445:
                continue
            os.system(cmd)
        except:
            pass