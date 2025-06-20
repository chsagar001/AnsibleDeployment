from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
import os
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Define the expected input format
class SignupRequest(BaseModel):
    username: str
    password: str

# Create a MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'sagar'),
        password=os.getenv('DB_PASSWORD', 'sagar123'),
        database=os.getenv('DB_NAME', 'testdb')
    )

# Route to handle user signup
@app.post("/signup")
async def signup(payload: SignupRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if user already exists
        cursor.execute("SELECT * FROM usernames WHERE username = %s", (payload.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")

        # Insert new user
        cursor.execute(
            "INSERT INTO usernames (username, password) VALUES (%s, %s)",
            (payload.username, payload.password)
        )
        conn.commit()
        return {"status": "success", "message": "User signed up"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.get("/data")
async def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, password FROM usernames")
        rows = cursor.fetchall()
        return {
            "db_status": "DB connected successfully",
            "message": "Hello from FastAPI Backend",
            "usernames": rows
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"db_status": f"DB connection failed: {str(e)}"})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)