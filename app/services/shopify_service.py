import httpx
from bs4 import BeautifulSoup
from app.models.brand import BrandContextResponse, Product, FAQ

class ShopifyInsightsService:
    async def fetch_insights(self, website_url: str) -> BrandContextResponse:
        # Ensure valid url (convert HttpUrl to string if needed)
        website_url = str(website_url)

        if not website_url.startswith("http"):
            raise ValueError("Invalid website URL")

        # Fetch products.json
        products_url = website_url.rstrip("/") + "/products.json"
        async with httpx.AsyncClient() as client:
            r = await client.get(products_url, timeout=10)
            if r.status_code != 200:
                raise ValueError("Website not found or invalid Shopify store")

            data = r.json()
            products = [
                Product(
                    id=p.get("id"),
                    title=p.get("title"),
                    handle=p.get("handle"),
                    price=p.get("variants", [{}])[0].get("price"),
                    url=website_url.rstrip("/") + "/products/" + p.get("handle", "")
                )
                for p in data.get("products", [])
            ]

        # Fetch home page (hero products, policies, etc.)
        async with httpx.AsyncClient() as client:
            resp = await client.get(website_url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            brand_name = soup.title.string if soup.title else "Unknown"

            # Example parsing social links
            socials = {}
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "instagram.com" in href:
                    socials["instagram"] = href
                elif "facebook.com" in href:
                    socials["facebook"] = href
                elif "tiktok.com" in href:
                    socials["tiktok"] = href

        return BrandContextResponse(
            brand_name=brand_name,
            product_catalog=products,
            hero_products=products[:3],  # naive: top 3 as hero
            privacy_policy=None,
            refund_policy=None,
            faqs=[FAQ(question="Do you offer COD?", answer="Yes, most stores do.")],
            social_handles=socials,
            contact_details={},
            about=None,
            important_links={}
        )

shopify_service = ShopifyInsightsService()

async def fetch_brand_context(website_url: str):
    return await shopify_service.fetch_insights(str(website_url))
