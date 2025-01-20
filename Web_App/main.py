from fastapi import FastAPI
import status, machines, submit, tasks

app = FastAPI()
app.include_router(status.router_status)
app.include_router(machines.router_machines)
app.include_router(submit.router_submit)
app.include_router(tasks.router_tasks)

# Check if the script is run directly and start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8585, log_level="info")