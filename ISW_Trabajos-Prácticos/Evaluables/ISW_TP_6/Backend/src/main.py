from fastapi import FastAPI
from routers.inscripciones import router as inscripciones_router  # <- ojo acá
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Actividades API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(inscripciones_router, tags=["inscripciones"])

@app.get("/health")
def health():
    return {"status": "ok"}