import requests
from fastapi import FastAPI, HTTPException
import os
from fuzzywuzzy import fuzz
from functions import *
import subprocess
AIPROXY_TOKEN = None
with open(".env") as f:
    try:
        for line in f:
            l = line.split("=")
            key, value = l[0],l[1]
            AIPROXY_TOKEN = l[1]
            print(AIPROXY_TOKEN)
    except:
        print("Set up enviroment variables")

app = FastAPI()


@app.get("/read")
async def read_file(path : str):
    if not path.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access to file is restricted")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File Not Found")
    file = open(path,"r")
    content = file.read()
    return {"content":content}

@app.post("/run")
async def run_task(task: str):
    try:
        task_output  = get_task_output(AIPROXY_TOKEN, task).lower()
        task = task.lower()
        if "count" in task:
            day = extract_dayname(task)
            count_days(day)
        elif "install" in task:
            package_name = extract_package(task)
            valid_package = get_valid_package_name(package_name)
            if package_name:
                subprocess.run(["pip","install",valid_package])
        else:
            return {"status":"Task is recognized but not implemented"}
        return {"status": "success", "task_output":task_output}
    except Exception as e:
         raise HTTPException(status_code =500, detail =str(e) )
