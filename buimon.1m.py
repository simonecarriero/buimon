#!/usr/bin/env python3

# <xbar.title>buimon</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Simone Carriero</xbar.author>
# <xbar.author.github>simonecarriero</xbar.author.github>
# <xbar.desc>GitHub Actions build monitor</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.abouturl>https://github.com/simonecarriero/buimon</xbar.abouturl>

import json
import urllib.request
import urllib.error
from pathlib import Path

def read_config(file_path): 
  with open(file_path, "r") as f: 
    config = json.load(f)
    return (config["github_token"], config["repositories"])

def github_get(token, url):
    request = urllib.request.Request(url, headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"})
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode())

def status_color(status, conclusion):
    if status == "in_progress": return "🟡"
    elif conclusion == "success": return "🟢"
    elif conclusion == "skipped": return "⚪"
    else: return "🔴"

def get_latest_run(token, repo_owner, repo_name, workflow_id):
    resp = github_get(token, f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/runs?per_page=999")
    if not resp.get("workflow_runs"): return ("⚪", [])
    latest_run = resp["workflow_runs"][0]
    color = status_color(latest_run["status"], latest_run["conclusion"])
    resp = github_get(token, f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{latest_run['id']}/jobs?per_page=999")
    jobs = map(lambda x: f"{status_color(x['status'], x['conclusion'])} {x['name']}", resp["jobs"])
    return (latest_run["id"], color, jobs)

def main():
    try:
        (token, repositories) = read_config(Path.home() / ".buimon.json")
        runs = list(map(lambda x: tuple([x["owner"], x["name"]]) + get_latest_run(token, x["owner"], x["name"], x["workflow_id"]), repositories))
        print("".join([color for (_, _, _, color, _) in runs]))
        print("---")
        for (owner, name, run_id, color, jobs) in runs:
            print(f"{color} {name}")
            print(f"--Open in GitHub | href=https://github.com/{owner}/{name}/actions/runs/{run_id}")
            print(f"-----")
            for job in jobs:
               print(f"--{job.replace('|', '-')}") 
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
