import uvicorn
from pathlib import Path

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    uvicorn.run(
        "main:app",
        app_dir=str(base_dir / "src"),  
        reload=True,
    )