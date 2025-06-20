from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import httpx
import uvicorn

app = FastAPI()

form_html = """
    <html>
    <body>
        <h2>Sign Up</h2>
        <form method="post" action="/signup">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Sign Up">
        </form>
        <p>{message}</p>
    </body>
    </html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=form_html.format(message=""))

@app.post("/signup", response_class=HTMLResponse)
async def signup(username: str = Form(...), password: str = Form(...)):
    data = {"username": username, "password": password}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("http://127.0.0.1:5050/signup", json=data)
        msg = res.json().get("message", "Signup failed.")
    except Exception as e:
        msg = f"Error contacting backend: {str(e)}"
    return HTMLResponse(content=form_html.format(message=msg))

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
