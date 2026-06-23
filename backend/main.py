from fastapi import FastAPI
from dotenv import load_dotenv
from api import router as api_router
from database import engine, Base


load_dotenv()
app = FastAPI(
    title="AI Assistant Server",
    description="This is the backend server for the AI Assistant application.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def root():
    return {"message": "AI Assistant Server is running."}


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(api_router, prefix="/api")
