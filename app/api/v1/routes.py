from fastapi import APIRouter, HTTPException
from app.models.brand import BrandContextRequest, BrandContextResponse
from app.services.shopify_service import fetch_brand_context

router = APIRouter()

@router.post("/fetch-brand-data", response_model=BrandContextResponse)
async def fetch_brand_data(request: BrandContextRequest):
    try:
        data = await fetch_brand_context(request.website_url)
        return data
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
