from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Carpeta donde se guardan los archivos
CARPETA = Path("subidas")
CARPETA.mkdir(exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Permite abrir/descargar los archivos desde /subidas/nombre
app.mount("/subidas", StaticFiles(directory=CARPETA), name="subidas")


def listar_archivos():
    lista = []
    for archivo in CARPETA.iterdir():
        lista.append({
            "nombre": archivo.name,
            "tamano": f"{archivo.stat().st_size / 1024:.1f} KB",
        })
    return lista


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse(request, "index.html", {"archivos": listar_archivos()})


@app.post("/subir", response_class=HTMLResponse)
async def subir(request: Request, archivo: UploadFile = File(...)):
    contenido = await archivo.read()
    with open(CARPETA / archivo.filename, "wb") as f:
        f.write(contenido)
    return templates.TemplateResponse(request, "_archivos.html", {"archivos": listar_archivos()})