import urllib3
import glob
import time
import shutil
import urllib
import requests
from google.cloud import vision
import io

def get_average_respone_time_from_urls():
	files = glob.glob("/home/advait/image_moderation/image-moderation-docker/data_subset_rand/*")
	urls = []
	for file in files:
		path = file.split('/')
		url = path[-2]+'/'+path[-1]
		urls.append(url)

	# print(urls)

	http = urllib3.PoolManager()
	totaltime = 0

	for i, url in enumerate(urls[:100]):
		start = time.time()

		r = http.request('GET', 'http://127.0.0.1:5000/url/'+urllib.parse.quote_plus(url))
		roundtrip = time.time() - start
		totaltime+=roundtrip
		try:
			if float(r.data) < 0.2:
				# shutil.copyfile(files[i], '/home/advait/image_moderation/image-moderation-docker/supposedly_safe/'+files[i].split('/')[-1]) 
				# print("Safe")
				continue
		    # print(float(r.data), '-->', roundtrip, 'seconds')
		except Exception as e:
			continue
		

	print('Average response time: ',totaltime/len(urls[:100]))

def get_average_respone_time_from_images():
	files = glob.glob("/home/advait/image_moderation/image-moderation-docker/data_subset_rand/*")

	totaltime=0

	endpoint = 'http://127.0.0.1:5000/image'
	for file in files[:100]:
		img = {'file': open(file, 'rb')}
		start = time.time()
		r = requests.post(endpoint, files=img)
		roundtrip = time.time() - start
		totaltime+=roundtrip
		print(r.text, '-->', roundtrip)

	print('Average response time: ',totaltime/len(files[:100]))

def response_time_from_google_safe_search():
    """Detects unsafe features in the file."""
    client = vision.ImageAnnotatorClient()
    files = glob.glob("/home/advait/image_moderation/image-moderation-docker/data_subset_rand/*")

    with io.open(files[0], 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    start = time.time()
    response = client.safe_search_detection(image=image)
    roundtrip = time.time() - start
	# totaltime+=roundtrip
    print(r.text, '-->', roundtrip)
    safe = response.safe_search_annotation

# get_average_respone_time_from_images()
# get_average_respone_time_from_urls()
response_time_from_google_safe_search()