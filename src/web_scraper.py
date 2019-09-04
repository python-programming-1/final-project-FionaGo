import requests
from bs4 import BeautifulSoup
import os
import warnings
warnings.filterwarnings("ignore")


# starting URL
url = 'https://mitsloan.mit.edu/mba/admissions/class-2020-profile'
res = requests.get(url)
res.raise_for_status()

# # let's only pull 10 URLs
# for i in range(10):
#
# 	res = requests.get(url)
#
# 	# check the status
# 	res.raise_for_status()
#
# 	# find the source URL of the image from the starting URL
# 	soup = BeautifulSoup(res.text)
# 	comic_div = soup.select('picture.item-comic-image')
# 	image_url = comic_div[0].contents[0].attrs['src']
# 	image_res = requests.get(image_url)
# 	image_res.raise_for_status()
#
# 	# save the image in chunk, then close it
# 	image_file = open(os.path.basename(image_url), 'wb')
# 	for chunk in image_res.iter_content(100000):
# 		image_file.write(chunk)
# 	image_file.close()
#
# 	# find the previous URL then rewrite the starting URL
# 	prev_div = soup.select('div .gc-calendar-nav__previous')
# 	prev_url= prev_div[0].contents[3].attrs['href']
# 	url = 'https://www.gocomics.com' + prev_url
#
# 	# print the latest URLs
# 	print(url)