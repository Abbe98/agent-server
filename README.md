# Agent Server

Agent is an Python HTTP API for retrieving information about an user. It uses the user agent string from browsers to return information about the client's OS, browser, and device. It uses the client's IP to return information about the user's location and time zone. Agent was originally developed to aid frontend based AB-testing.

## Setup

```bash
git clone https://github.com/Abbe98/agent-server.git
cd agent-server
pipenv install
pipenv run python3 src/agent.py
```

# Usage

Agent does only have one endpoint, its root. Send a GET request to it to retrieve a JSON response similar to the following one:

```json
{
  "browser": {
    "name": "Opera",
    "version": 48
  }, 
  "device": {
    "brand": null,
    "model": null,
    "name": "Other",
    "touch_capable": false,
    "type": "Desktop"
  },
  "geo": {
    "city": "Stockholm",
    "country": "Sweden",
    "country_code": "SE",
    "ip": "127.0.0.1",
    "latitude": 59.3333,
    "longitude": 18.05,
    "region": "Stockholm",
    "time_zone": "Europe/Stockholm"
  },
  "os": {
    "name": "Mac OS X",
    "version": "10.12.6"
  }
}
```
