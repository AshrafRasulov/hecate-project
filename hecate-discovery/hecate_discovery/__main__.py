import uvicorn
from hecate_discovery.server import app

if __name__ == "__main__":
    # Serve the FastAPI app using Uvicorn on the specified host and port 8771
    uvicorn.run(app, host="127.0.0.1", port=8771)