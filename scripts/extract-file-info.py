#!/usr/bin/env python
import pandas as pd
import json
import os

def get_files(request):
    files = []
    for comm in request["communications"]:
        if (comm["response"] == True) and len(comm["files"]):
            comm_files = comm["files"][:]
            for cf in comm_files:
                cf["communication_id"] = comm["id"]
                cf["request_id"] = request["id"]
            files += comm_files
    return pd.DataFrame(files)

if __name__ == "__main__":
    HERE = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(HERE, "../data/muckrock-requests.json")

    with open(json_path) as f:
        files = pd.concat([ get_files(req)
            for req in json.load(f)]).reset_index(drop=True)

    files.to_csv(
        os.path.join(HERE, "../data/muckrock-files.csv"),
        encoding="utf-8",
        index=False
    )
