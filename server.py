import uvicorn
from src import create_app
from src.utils import settings

app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
