import re
import base64
import requests
from bs4 import BeautifulSoup

url = 'http://jandan.net/ooxx/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
image_pat = re.compile(r'(\/\w+\/)')

while url:
    r = requests.get(url, headers=headers)
    url = ''
    soup = BeautifulSoup(r.text, 'lxml')
    images = soup.select("span.img-hash")
    for image in images:
        image_url = str(base64.b64decode(image.text), 'utf-8')
        large_image_url = image_pat.sub('/large/', image_url)
        ir = requests.get("http:" + large_image_url)
        if ir.status_code == 200:
            open(image.split("/")[-1], 'wb').write(ir.content)

    next_page_button = soup.find('a', {'class': 'previous-comment-page'})

    if next_page_button:
        url = 'http:' + next_page_button.get('href')
