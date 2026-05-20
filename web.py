import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any


CATEGORY_URLS = {
    "ring": [
        "https://www.danjewellers.co.uk/gold-rings/cid10006/gold-rings.asp",
        "https://www.danjewellers.co.uk/silver-rings/cid10014/silver-rings.asp",
        "https://www.danjewellers.co.uk/diamond-rings/cid10021/diamond-rings.asp",
    ],
    "necklace": [
        "https://www.danjewellers.co.uk/gold-chains/cid10003/gold-chains.asp",
        "https://www.danjewellers.co.uk/silver-chains/cid10012/silver-chains.asp",
    ],
    "bracelet": [
        "https://www.danjewellers.co.uk/gold-bracelets/cid10002/gold-bracelets.asp",
        "https://www.danjewellers.co.uk/silver-bracelets/cid10011/silver-bracelets.asp",
    ],
    "earrings": [
        "https://www.danjewellers.co.uk/gold-earrings/cid10004/gold-earrings.asp",
        "https://www.danjewellers.co.uk/silver-earrings/cid10013/silver-earrings.asp",
        "https://www.danjewellers.co.uk/diamond-earrings/cid10019/diamond-earrings.asp",
    ],
}


async def _fetch_page(url: str) -> str:
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        response = await client.get(url)
        if response.status_code != 200:
            return ""
        return response.text


def _extract_products(html: str, retailer: str, limit: int) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[Dict[str, Any]] = []

    links = soup.select("h3 a")

    for link_tag in links:
        title = link_tag.get_text(strip=True)
        link = link_tag.get("href", "").strip()

        if not title or not link:
            continue

        if not link.startswith("http"):
            link = "https://www.danjewellers.co.uk/" + link.lstrip("/")

        image_url = ""
        container = link_tag

        for _ in range(4):
            container = container.parent
            if not container:
                break
            img = container.find("img")
            if img:
                image_url = (
                    img.get("src")
                    or img.get("data-src")
                    or img.get("data-original")
                    or ""
                ).strip()
                if image_url:
                    break

        if image_url and not image_url.startswith("http"):
            image_url = "https://www.danjewellers.co.uk/" + image_url.lstrip("/")

        results.append(
            {
                "title": title,
                "price": None,
                "currency": "GBP",
                "retailer": retailer,
                "link": link,
                "image_url": image_url,
            }
        )

        if len(results) >= limit:
            break

    return results


async def search_dan(query: str, kind: str = "", limit: int = 4) -> List[Dict[str, Any]]:
    kind = (kind or "").strip().lower()
    urls = CATEGORY_URLS.get(kind, CATEGORY_URLS["ring"])

    all_results: List[Dict[str, Any]] = []

    for url in urls:
        html = await _fetch_page(url)
        if not html:
            continue

        page_results = _extract_products(html, "Dan Jewellers", limit)
        all_results.extend(page_results)

        if len(all_results) >= limit:
            break

    query_words = [word.lower() for word in query.split() if len(word) > 2]

    if query_words:
        filtered = []
        for item in all_results:
            title_lower = item["title"].lower()
            if any(word in title_lower for word in query_words):
                filtered.append(item)
    else:
        filtered = all_results

    unique_results = []
    seen_links = set()

    for item in filtered:
        link = item.get("link", "")
        if link in seen_links:
            continue
        seen_links.add(link)
        unique_results.append(item)

    blocked_words = ["junior", "boxing glove"]

    cleaned_results = []
    for item in unique_results:
        title_lower = item["title"].lower()
        if any(word in title_lower for word in blocked_words):
            continue
        cleaned_results.append(item)

    return cleaned_results[:limit]