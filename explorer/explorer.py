import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

NODE_URL = "http://127.0.0.1:8000"

app = FastAPI()


def get_chain():
    return requests.get(f"{NODE_URL}/chain").json()


def get_validators():
    return requests.get(f"{NODE_URL}/validators").json()


@app.get("/", response_class=HTMLResponse)
def dashboard():

    chain = get_chain()
    validators = get_validators()

    html = "<h1>Proof of Utility Explorer</h1>"

    html += "<h2>Network Stats</h2>"
    html += f"Blocks: {chain['length']}<br>"

    html += "<h2>Validators</h2>"

    for v, data in validators.items():

        html += f"""
        <p>
        Node: {v}<br>
        Utility: {data['utility']}<br>
        Reputation: {round(data['reputation'],2)}
        </p>
        """

    html += "<h2>Latest Blocks</h2>"

    for block in chain["chain"][-5:]:

        html += f"""
        <div style='border:1px solid gray;padding:10px;margin:10px'>
        Block: {block['index']}<br>
        Validator: {block['validator']}<br>
        Hash: {block['hash']}
        </div>
        """

    return html
