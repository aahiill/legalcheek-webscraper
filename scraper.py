import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dataclasses import dataclass, asdict
from typing import Optional
import pandas as pd

url = 'https://www.legalcheek.com/the-firms-most-list/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}


@dataclass
class Programme:
    firm: str
    title: str
    applications_open: Optional[str]
    applications_close: Optional[str]
    link: Optional[str]


def extract_hrefs(page_url):
    """Fetch `page_url` and return a list of all (href, text) tuples."""
    try:
        resp = requests.get(page_url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Request failed:  ", e)
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    anchors = soup.find_all("a", href=True)
    results = []

    for a in anchors:
        href = urljoin(page_url, a["href"])
        text = a.get_text(strip=True)
        results.append((href, text))
    return results


def extract_programmes(page_url, firm):
    """Fetch the firm-specific `page_url`s and return the programmes"""
    try:
        resp = requests.get(page_url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Request failed:  ", e)
        return []

    
    soup = BeautifulSoup(resp.text, "html.parser")

    # find the deadlines heading
    deadlines_h2 = soup.find("h2", string=lambda s: s and s.strip().lower() == "deadlines")
    if not deadlines_h2:
        return []

    # find the deadline cards (contains information for programmes)
    deadlines_container = deadlines_h2.find_next("div", class_="c-grid")
    if not deadlines_container:
        return []
    
    cards = deadlines_container.select("div.c-card.c-card_centered, div.c-card.c-card__centered")

    if not cards:
        return []

    programmes = []

    for card in cards:
        title_tag = card.find("h3", class_="c-heading")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not title:
            continue

        open_date = None
        close_date = None

        for row in card.select("div.c-card_row, div.c-card__row"):
            label_tag = row.select_one("span.c-card__label, span.c-card_label")
            date_tag = row.select_one("span.c-card__date, span.c-card_date")

            if not label_tag or not date_tag:
                continue

            label = label_tag.get_text(strip=True).lower()
            date = date_tag.get_text(strip=True)

            if "open" in label:
                open_date = date
            elif "close" in label:
                close_date = date

        a = card.select_one("a.c-button[href]")
        link = urljoin(page_url, a["href"]) if a else None
        programmes.append(
            Programme(
                firm=firm,
                title=title,
                applications_open=open_date,
                applications_close=close_date,
                link=link,
            )
        )

    return programmes
        



if __name__ == "__main__":
    links = extract_hrefs(url)
    # filter for firm pages (e.g. '/firm/clifford-chance/')
    firm_segment = "/firm/"
    # remove the tuples where t is a number and not the firm's name
    firm_urls = {(h, t) for (h, t) in links if firm_segment in h and not t.strip().isdigit()}

    all_programmes = []

    for href, text in firm_urls:
        programmes = extract_programmes(href, text)
        all_programmes.extend(programmes)

    # Convert to DataFrame and export to CSV
    df = pd.DataFrame(asdict(p) for p in all_programmes)
    df.to_csv("legalcheek_deadlines.csv", index=False)

    print(f"Exported {len(df)} programmes to legalcheek_deadlines.csv")