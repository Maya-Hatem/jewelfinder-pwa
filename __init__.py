# app/services/ebay.py
import os
import base64
import time
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv

load_dotenv()


_token_cache = {"token": None, "expires_at": 0}


def _token_url() -> str:
    env = (os.getenv("EBAY_ENV") or "sandbox").strip().lower()
    return (
        "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
        if env == "sandbox"
        else "https://api.ebay.com/identity/v1/oauth2/token"
    )


def _search_url() -> str:
    env = (os.getenv("EBAY_ENV") or "sandbox").strip().lower()
    return (
        "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
        if env == "sandbox"
        else "https://api.ebay.com/buy/browse/v1/item_summary/search"
    )


async def get_app_token() -> str:
    now = int(time.time())
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    client_id = (os.getenv("EBAY_CLIENT_ID") or "").strip()
    client_secret = (os.getenv("EBAY_CLIENT_SECRET") or "").strip()

    if not client_id or not client_secret:
        raise RuntimeError("Missing EBAY_CLIENT_ID or EBAY_CLIENT_SECRET in .env")

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(_token_url(), headers=headers, data=data)

    if r.status_code != 200:
        raise RuntimeError(f"Token error {r.status_code}: {r.text}")

    payload = r.json()
    _token_cache["token"] = payload["access_token"]
    _token_cache["expires_at"] = now + int(payload.get("expires_in", 7200))
    return _token_cache["token"]




async def search_items(query: str, limit: int = 12) -> List[Dict[str, Any]]:
    return [
        {
            "title": "Gold Solitaire Engagement Ring",
            "price": 180.00,
            "currency": "GBP",
            "retailer": "eBay",
            "link": "https://www.ebay.co.uk",
            "image_url": "/static/ring1.png",
        },
        {
            "title": "Rose Gold Engagement Ring with Diamond",
            "price": 210.00,
            "currency": "GBP",
            "retailer": "eBay",
            "link": "https://www.ebay.co.uk",
            "image_url": "/static/ring2.png",
        },
        {
            "title": "Classic Diamond Engagement Ring",
            "price": 250.00,
            "currency": "GBP",
            "retailer": "eBay",
            "link": "https://www.ebay.co.uk",
            "image_url": "/static/ring3.png",
        },
        {
            "title": "Vintage Style Diamond Engagement Ring",
            "price": 275.00,
            "currency": "GBP",
            "retailer": "eBay",
            "link": "https://www.ebay.co.uk",
            "image_url": "/static/ring4.png",
        },
        {
            "title": "White Gold Diamond Engagement Ring",
            "price": 300.00,
            "currency": "GBP",
            "retailer": "eBay",
            "link": "https://www.ebay.co.uk",
            "image_url": "/static/ring5.png",
        },
    ][:limit]





    token = await get_app_token()
    marketplace = (os.getenv("EBAY_MARKETPLACE") or "EBAY_GB").strip()

    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": marketplace,
    }

    safe_query = f"{query} jewelry OR jewellery -toy -game -craft -bead -pattern"

    params = {
        "q": safe_query,
        "limit": str(limit),
        "category_ids": "281",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(_search_url(), headers=headers, params=params)

    if r.status_code != 200:
        raise RuntimeError(f"Search error {r.status_code}: {r.text}")

    data = r.json()
    items = data.get("itemSummaries", [])

    results = []
    for item in items:
        price_obj = item.get("price") or {}
        price_val = price_obj.get("value")
        if price_val is None:
            continue

        results.append(
            {
                "title": item.get("title", "Untitled"),
                "price": float(price_val),
                "currency": price_obj.get("currency", "GBP"),
                "retailer": "eBay",
                "link": item.get("itemWebUrl", ""),
                "image_url": (item.get("image") or {}).get("imageUrl", ""),
            }
        )

    results.sort(key=lambda x: x["price"])
    return results