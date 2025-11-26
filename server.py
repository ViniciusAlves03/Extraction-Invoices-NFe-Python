import uvicorn
from src.app import create_app
from src.utils.config import settings

app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
