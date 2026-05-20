# JewelFinder

Luxury-themed jewellery comparison Progressive Web App (PWA) built using FastAPI and eBay Browse API integration.

## Features

- Live jewellery search using eBay Browse API
- Category filtering
- Price sorting
- Responsive luxury-themed UI
- Progressive Web App (PWA) support
- OAuth-secured API integration

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
