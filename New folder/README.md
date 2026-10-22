# Emotion Detector — Ready-to-run student project

A Flask web application that analyzes text for anger, disgust, fear, joy, and sadness.

## Run in VS Code (Windows)

Open the project folder in VS Code, then open Terminal → New Terminal and run:

```powershell
py -m pip install -r requirements.txt
py server.py
```

Open this address in your browser: http://127.0.0.1:5000

To stop the server, return to the terminal and press `Ctrl+C`.

## How results work

- The app first tries the course's Watson NLP Emotion Prediction API.
- If the API is reachable, the page labels the result as a Watson API result.
- If the API cannot be reached, the page uses a small keyword-based local demo estimate so the interface remains demonstrable. This estimate is not the Watson model and is not suitable for scientific or real-world decisions.

## Run tests

```powershell
py -m unittest discover -s tests -v
```

## Note about network access

The Watson endpoint may be restricted or unavailable from some networks/environments. A local fallback is included for a working demonstration, but if an assignment grader requires the official API, run it in the course-provided environment or restore access to the endpoint.
