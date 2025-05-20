from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2.sandbox import SandboxedEnvironment
from jinja2 import BaseLoader
import base64
import pickle

env = SandboxedEnvironment(
    loader=BaseLoader(),
    autoescape=True
)

# todo: Remove this "feature"...
def return_method(serialized_data):
    try:
        data = base64.b64decode(serialized_data)
        obj = pickle.loads(data)
        return str(obj)
    except Exception as e:
        return f"Deserialization error: {str(e)}"

env.globals.update({
    "return_method": return_method
})

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

# API endpoint for processing Jinja2 expressions
@app.post("/api/search", response_class=JSONResponse)
async def handle_search(request: Request):
    data = await request.json()
    search_keyword = data.get("searchKeyword", "")

    try:
        # Safe sandboxed evaluation
        template = env.from_string(search_keyword)
        result = template.render()
    except Exception:
        result = "Invalid Expression"

    return {"message": f"Received search input: {search_keyword}", "result": result}
