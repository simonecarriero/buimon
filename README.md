# buimon

xbar plugin to monitor GitHub Actions workflows

## Installation

```
curl -L https://raw.githubusercontent.com/simonecarriero/buimon/refs/heads/main/buimon.1m.py > buimon.1m.py && \
    chmod +x buimon.1m.py && \
    mv buimon.1m.py ~/Library/Application\ Support/xbar/plugins/buimon.1.py
```

## Configuration

[Create a GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
and a configuration file at `~/.buimon.json` like the following:

```
{
    "github_token": "<your-token>",
    "repositories": [
        {"owner": "foo", "name": "foo", "workflow_id": "ci.yml"}
    ]
}
```
