from fastapi import FastAPI
from app.api.v1.routes import router  # 👈 no aliasing

app = FastAPI(title="Shopify Insights Fetcher")

# include routes
app.include_router(router, prefix="/api/v1", tags=["brand"])

@app.get("/")
def root():
    return {"message": "Shopify Insights Fetcher is running!"}
