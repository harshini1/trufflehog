import subprocess
import azure.functions as func
import logging
from trufflehog3 import cli

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def call_cli():
    try:
        # The command and arguments for running trufflehog3 CLI
        command = [
            "python3", "-m", "trufflehog3.cli",
            "https://github.com/trufflesecurity/test_keys"
        ]

        # Run the command as a subprocess and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 2:
            return f"success.... {result.stdout}"
        else:
            # If there's an error, return stderr as the response
            return f"error.... {result}"
    except Exception as e:
        return f"Exception: {str(e)}"
    
@app.route(route="run_trufflehog")
def run_trufflehog(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    out = call_cli()
    return func.HttpResponse(f"output {out}")