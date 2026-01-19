import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.legalcheek.com/the-firms-most-list/'

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

def extract_hrefs(page_url):
	try:
		resp = requests.get(page_url, headers=headers, timeout=15)
		resp.raise_for_status()
	except requests.exceptions.RequestException as e:
		print('Request failed:', e)
		return []

	soup = BeautifulSoup(resp.text, 'html.parser')
	anchors = soup.find_all('a', href=True)
	results = []
	for a in anchors:
		href = urljoin(page_url, a['href'])
		text = a.get_text(strip=True)
		results.append((href, text))
	return results


if __name__ == '__main__':
	links = extract_hrefs(url)
	# filter for firm pages (e.g. '/firm/clifford-chance/')
	firm_segment = '/firm/'
	firm_urls = {(h, t) for (h, t) in links if firm_segment in h and not t.strip().isdigit()}
	for href in firm_urls:
		print(href)
