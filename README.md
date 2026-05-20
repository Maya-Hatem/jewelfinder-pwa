# JewelFinder

JewelFinder is a web-based jewellery comparison platform developed for a dissertation project.  
It allows users to search, filter, and compare jewellery products within a single interface.

---

## Features

- Keyword-based search  
- Category filtering  
- Price sorting  
- Structured product display  
- Prototype image-based search  

---

## How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Run the app:

python -m uvicorn main:app --reload --port 8001

3. Open in browser:

http://127.0.0.1:8001

---

## Variables

To enable live API functionality, create a `.env` file:

EBAY_CLIENT_ID=your_client_id  
EBAY_CLIENT_SECRET=your_client_secret  
EBAY_MARKETPLACE=EBAY_GB  

The `.env` file is not included in this submission for security reasons.

---

## Note

Fallback data may be used if the external API is unavailable.