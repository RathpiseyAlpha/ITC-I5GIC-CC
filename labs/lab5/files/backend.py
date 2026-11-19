"""The Lab 5 social-post microservice. Vite proxies requests to this local API."""

import os
from uuid import uuid4

import boto3
import mysql.connector
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, status
from mysql.connector import Error as DatabaseError
from mysql.connector import IntegrityError, errorcode
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from werkzeug.security import check_password_hash, generate_password_hash


app = FastAPI(title="Lab 5 · Social Posts Microservice")
app.add_middleware(SessionMiddleware, secret_key=os.environ["LAB_SESSION_KEY"], max_age=1800)

REGION = os.environ.get("AWS_REGION", "us-east-1")
BUCKET = os.environ["LAB_MEDIA_BUCKET"]
posts = boto3.resource("dynamodb", region_name=REGION).Table("posts")
s3 = boto3.client("s3", region_name=REGION, config=Config(signature_version="s3v4"))


def connect(host, password):
    return mysql.connector.connect(
        host=os.environ[host], user="admin", password=os.environ[password], database="educative_db",
        ssl_ca=os.environ["LAB_RDS_CA"], ssl_verify_cert=True, ssl_verify_identity=True,
        connection_timeout=5,
    )


@app.exception_handler(DatabaseError)
@app.exception_handler(ClientError)
@app.exception_handler(BotoCoreError)
async def storage_error(request, error):
    return JSONResponse(
        status_code=503, content={"detail": "Check database connectivity and your AWS Academy CLI credentials."}
    )


class Login(BaseModel):
    email: str
    password: str


class Signup(Login):
    username: str


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: Signup):
    email = user.email.strip().lower()
    username = user.username.strip()
    if "@" not in email or len(email) > 254 or not 1 <= len(username) <= 80 or not 12 <= len(user.password) <= 128:
        raise HTTPException(400, "Use a demo email, a display name and a password of 12–128 characters.")
    with connect("LAB_AURORA_WRITER", "LAB_AURORA_PASSWORD") as db, db.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                (email, username, generate_password_hash(user.password)),
            )
        except IntegrityError as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                raise HTTPException(409, "This demo email is already registered.") from error
            raise
        db.commit()
    return {"message": "User created successfully"}


@app.post("/login")
def login(user: Login, request: Request):
    email = user.email.strip().lower()
    if len(email) > 254 or len(user.password) > 128:
        raise HTTPException(401, "Invalid demo email or password.")
    with connect("LAB_AURORA_READER", "LAB_AURORA_PASSWORD") as db, db.cursor() as cursor:
        cursor.execute("SELECT username, password_hash FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
    if row is None or not check_password_hash(row[1], user.password):
        raise HTTPException(401, "Invalid demo email or password.")
    request.session.clear()
    request.session["username"] = row[0]
    return {"message": [email, row[0]]}


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Signed out"}


@app.post("/create_post")
def create_post(
    request: Request, title: str = Form(), content: str = Form(), media: UploadFile | str | None = File(None)
):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(401, "Sign in to create a post.")
    title, content = title.strip(), content.strip()
    if not 1 <= len(title) <= 120 or not 1 <= len(content) <= 2000:
        raise HTTPException(400, "Enter a title up to 120 characters and text up to 2,000 characters.")

    post_id = uuid4().hex
    item = {"post_id": post_id, "title": title, "content": content}
    # The Vite client sends a text value instead of a file when no image is selected.
    if media is not None and not isinstance(media, str) and media.filename:
        extension = {"image/png": "png", "image/jpeg": "jpg"}.get(media.content_type)
        if not extension or not media.size or media.size > 2 * 1024 * 1024:
            raise HTTPException(400, "Choose a PNG or JPEG image up to 2 MiB.")
        key = f"posts/{post_id}.{extension}"
        s3.upload_fileobj(media.file, BUCKET, key, ExtraArgs={"ContentType": media.content_type})
        item["media"] = key

    posts.put_item(Item=item)
    with connect("LAB_RDS_HOST", "LAB_RDS_PASSWORD") as db, db.cursor() as cursor:
        cursor.execute("INSERT INTO user_post (id, username) VALUES (%s, %s)", (post_id, username))
        db.commit()
    return {"message": "Post created successfully", "post_id": post_id}


@app.get("/get_posts")
def get_posts(request: Request):
    if "username" not in request.session:
        raise HTTPException(401, "Sign in to list posts.")
    with connect("LAB_RDS_HOST", "LAB_RDS_PASSWORD") as db, db.cursor() as cursor:
        cursor.execute("SELECT id, username FROM user_post ORDER BY created_at DESC, id LIMIT 25")
        rows = cursor.fetchall()
    results = []
    for post_id, username in rows:
        item = posts.get_item(Key={"post_id": post_id}, ConsistentRead=True).get("Item")
        if item is None:
            continue
        item["username"] = username
        if "media" in item:
            item["media"] = s3.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET, "Key": item["media"]}, ExpiresIn=300
            )
        results.append(item)
    return results
