from fastapi import FastAPI
import status

app = FastAPI()
app.include_router(status.router)

# Check if the script is run directly and start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8585, log_level="info")