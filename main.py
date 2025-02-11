from routes import Usuario, Audios, Clicks, Disfonias, Enfermedades, Frases, Surveys, Sylabus, Auth
from db import db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 

origins = [
    "http://127.0.0.1:4200",
    "http://localhost:4200",
    "https://lara-frontend-omega.vercel.app"
]

async def get_db():
    if db is None:
        raise RuntimeError("La conexión a MongoDB no está inicializada.")
    return db

app = FastAPI()

@app.get("/check_connection")
async def check_connection():
    try:
        from db import db
        collections = await db.list_collection_names()
        return {"status": "Conexión exitosa a MongoDB", "collections": collections}
    except Exception as e:
        return {"status": "Error de conexión", "error": str(e)}
    
# Registrar rutas
app.include_router(Auth.router, prefix="/login", tags=["Login"])
app.include_router(Usuario.router, prefix="/usuarios", tags=["Usuario"])
app.include_router(Audios.router, prefix="/audios", tags=["Audios"])
app.include_router(Clicks.router, prefix="/clicks", tags=["Clicks"])
app.include_router(Disfonias.router, prefix="/disfonias", tags=["Disfonias"])
app.include_router(Enfermedades.router, prefix="/enfermedades", tags=["Enfermedades"])
app.include_router(Frases.router, prefix="/frases", tags=["Frases"])
app.include_router(Surveys.router, prefix="/surveys", tags=["Surveys"])
app.include_router(Sylabus.router, prefix="/sylabus", tags=["Sylabus"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)