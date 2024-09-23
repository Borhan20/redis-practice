from contextlib import asynccontextmanager
import fastapi
from redis import Redis
import httpx 
import json

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Startup logic
    app.state.redis = Redis(host='localhost', port=6379)
    app.state.http_client = httpx.AsyncClient()
    
    yield  # Application runs during this period
    
    # Shutdown logic
    app.state.redis.close()
    await app.state.http_client.aclose()

app = fastapi.FastAPI(lifespan=lifespan)

# app = fastapi.FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     app.state.redis = Redis(host='localhost', port=6379)
#     app.state.http_client = httpx.AsyncClient()

# @app.on_event("shutdown")
# async def shutdwon_event():
#     app.state.redis.close()

@app.get("/entries")
async def read_item():
     
     value = app.state.redis.get("entries")
     if value is None:     
        response = await app.state.http_client.get('https://fakestoreapi.com/products')
        value = response.json()
        data_str = json.dumps(value)
        app.state.redis.set("entries",data_str)
    # return JSONResponse(content= jsonable_encoder(response))
     return json.loads(value)