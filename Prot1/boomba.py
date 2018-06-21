import time
import urllib.request, json
import requests
import urllib

# while (True):
req = urllib.request.Request("https://pantip.com/home/ajax_loadmore_home?p=" + str(time.time()))
print("https://pantip.com/home/ajax_loadmore_home?p=" + str(time.time()))
r = urllib.request.urlopen(req).read().decode('utf-8')
cont = json.loads(r)
print (cont)
text_file = open("Output.txt", "w")
text_file.write(r)
text_file.close()
    # time.sleep(10)
