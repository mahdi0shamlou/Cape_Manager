from fastapi import FastAPI
import status, machines, submit, tasks

app = FastAPI()
app.title="Cape Manager"
app.include_router(status.router_status) # these routes work on status of kvm machines
app.include_router(machines.router_machines) # these routes work on turn off or on in kvm machines
app.include_router(submit.router_submit) # these routes work on submit a task
app.include_router(tasks.router_tasks) # these routes work on details of tasks

# Check if the script is run directly and start the server
if __name__ == "__main__":
    import uvicorn
    import configparser
    import os
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'server.ini')
    # Read configuration from server.ini
    config = configparser.ConfigParser()
    config.read(config_path)

    print("Config path:", config_path)
    print(config.sections())

    # Extract settings
    host = config['server']['host']
    port = int(config['server']['port'])
    log_level = config['server']['log_level']

    uvicorn.run(app, host=host, port=port, log_level=log_level)