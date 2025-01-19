from fastapi import FastAPI
import status, machines

app = FastAPI()
app.include_router(status.router_status)
app.include_router(machines.router_machines)

# Check if the script is run directly and start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8585, log_level="info")