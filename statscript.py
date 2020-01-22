import urllib3
import glob
import time
import shutil
import urllib

files = glob.glob("/home/advait/image_moderation/nsfw-docker/data_subset_rand/*")
urls = []
for file in files:
	path = file.split('/')
	url = path[-2]+'/'+path[-1]
	urls.append(url)

print(urls)

http = urllib3.PoolManager()
totaltime = 0

for i, url in enumerate(urls):
	start = time.time()

	r = http.request('GET', 'http://127.0.0.1:5000/url/'+urllib.parse.quote_plus(url))
	roundtrip = time.time() - start
	totaltime+=roundtrip
	try:
		if float(r.data) < 0.2:
			shutil.copyfile(files[i], '/home/advait/image_moderation/nsfw-docker/supposedly_safe/'+files[i].split('/')[-1]) 
			print("Safe")
		print(float(r.data), '-->', roundtrip, 'seconds')
	except Exception as e:
		continue
	

print('Average response time: ',totaltime/len(urls))