"""Single-instance teaching app. Run on EC2 and access through an SSH tunnel."""

import os
import secrets
from uuid import uuid4

import boto3
import mysql.connector
from botocore.config import Config
from botocore.exceptions import ClientError
from flask import Flask, abort, redirect, render_template_string, request, session, url_for
from mysql.connector import Error as DatabaseError
from mysql.connector import IntegrityError, errorcode
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["LAB_SESSION_KEY"],
    SESSION_COOKIE_SAMESITE="Lax",
    TRUSTED_HOSTS=["127.0.0.1", "localhost"],
    MAX_CONTENT_LENGTH=3 * 1024 * 1024,
)

BUCKET = os.environ["LAB_MEDIA_BUCKET"]
REGION = os.environ.get("AWS_REGION", "us-east-1")
posts_table = boto3.resource("dynamodb", region_name=REGION).Table("posts")
s3 = boto3.client("s3", region_name=REGION, config=Config(signature_version="s3v4"))


def connect(host, password):
    return mysql.connector.connect(
        host=os.environ[host],
        user="admin",
        password=os.environ[password],
        database="educative_db",
        ssl_ca=os.environ["LAB_RDS_CA"],
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        connection_timeout=5,
    )


@app.before_request
def check_form_token():
    if request.method == "POST":
        expected = session.get("form_token")
        supplied = request.form.get("form_token", "")
        if not expected or not secrets.compare_digest(expected.encode(), supplied.encode()):
            abort(400, "Reload the page and submit the form again.")


@app.errorhandler(DatabaseError)
@app.errorhandler(ClientError)
def storage_error(error):
    app.logger.error("Storage request failed: %s", type(error).__name__)
    return "Storage request failed. Check database connectivity, configuration and the EC2 role.", 503


@app.get("/")
def home():
    if "form_token" not in session:
        session["form_token"] = secrets.token_urlsafe(24)
    posts = []
    if "email" in session:
        with connect("LAB_RDS_HOST", "LAB_RDS_PASSWORD") as db, db.cursor() as cursor:
            cursor.execute("SELECT id, username FROM user_post ORDER BY created_at DESC, id LIMIT 25")
            rows = cursor.fetchall()
        for post_id, username in rows:
            item = posts_table.get_item(Key={"post_id": post_id}, ConsistentRead=True).get("Item")
            if item is None:
                continue
            item["username"] = username
            item["image_url"] = None
            if "media_key" in item:
                item["image_url"] = s3.generate_presigned_url(
                    "get_object", Params={"Bucket": BUCKET, "Key": item["media_key"]}, ExpiresIn=300
                )
            posts.append(item)
    return render_template_string(PAGE, posts=posts)


@app.post("/signup")
def signup():
    email = request.form.get("email", "").strip().lower()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if "@" not in email or len(email) > 254 or not 1 <= len(username) <= 80 or not 12 <= len(password) <= 128:
        abort(400, "Enter a demo email, a display name and a password of 12–128 characters.")
    with connect("LAB_AURORA_WRITER", "LAB_AURORA_PASSWORD") as db, db.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                (email, username, generate_password_hash(password)),
            )
        except IntegrityError as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                abort(409, "That demo account already exists. Go back and sign in.")
            raise
        db.commit()
    return redirect(url_for("home", registered="1"))


@app.post("/login")
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if len(email) > 254 or len(password) > 128:
        abort(401, "Check the demo email and password.")
    with connect("LAB_AURORA_READER", "LAB_AURORA_PASSWORD") as db, db.cursor() as cursor:
        cursor.execute("SELECT username, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    if not user or not check_password_hash(user[1], password):
        abort(401, "Check the demo email and password.")
    session.clear()
    session.update(email=email, username=user[0])
    return redirect(url_for("home"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.post("/posts")
def create_post():
    if "email" not in session:
        abort(401)
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not 1 <= len(title) <= 120 or not 1 <= len(content) <= 2000:
        abort(400, "A post needs a title and text within the form limits.")

    post_id = uuid4().hex
    item = {"post_id": post_id, "title": title, "content": content}
    media = request.files.get("media")
    if media and media.filename:
        extensions = {"image/png": "png", "image/jpeg": "jpg"}
        extension = extensions.get(media.mimetype)
        if not extension:
            abort(400, "Choose a PNG or JPEG image.")
        key = f"posts/{post_id}.{extension}"
        s3.upload_fileobj(media.stream, BUCKET, key, ExtraArgs={"ContentType": media.mimetype})
        item["media_key"] = key

    posts_table.put_item(Item=item)
    with connect("LAB_RDS_HOST", "LAB_RDS_PASSWORD") as db, db.cursor() as cursor:
        cursor.execute("INSERT INTO user_post (id, username) VALUES (%s, %s)", (post_id, session["username"]))
        db.commit()
    return redirect(url_for("home"))


PAGE = """
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab 7 · Database demo</title>
<main style="max-width:42rem;margin:2rem auto;padding:0 1rem;font-family:system-ui">
  <h1>Lab 7 · Database demo</h1>
  {% if session.get('email') %}
    <p>Signed in as {{ session.username }}.</p>
    <form method="post" action="{{ url_for('logout') }}">
      <input type="hidden" name="form_token" value="{{ session.form_token }}">
      <button>Sign out</button>
    </form>
    <h2>Write a post</h2>
    <form method="post" action="{{ url_for('create_post') }}" enctype="multipart/form-data">
      <input type="hidden" name="form_token" value="{{ session.form_token }}">
      <p><label>Title <input name="title" maxlength="120" required></label></p>
      <p><label>Text <textarea name="content" maxlength="2000" required></textarea></label></p>
      <p><label>Image (PNG or JPEG) <input type="file" name="media" accept="image/png,image/jpeg"></label></p>
      <button>Publish</button>
    </form>
    <h2>Recent posts</h2>
    {% for post in posts %}
      <article>
        <h3>{{ post.title }}</h3>
        <p>{{ post.username }} · <code>{{ post.post_id }}</code></p>
        <p>{{ post.content }}</p>
        {% if post.image_url %}<img src="{{ post.image_url }}" alt="Attached image" style="max-width:100%">{% endif %}
      </article>
    {% else %}<p>No posts yet.</p>{% endfor %}
  {% else %}
    {% if request.args.get('registered') %}<p>Account created. Sign in below.</p>{% endif %}
    <h2>Sign in</h2>
    <form method="post" action="{{ url_for('login') }}">
      <input type="hidden" name="form_token" value="{{ session.form_token }}">
      <p><label>Demo email <input type="email" name="email" required></label></p>
      <p><label>Demo password <input type="password" name="password" required></label></p>
      <button>Sign in</button>
    </form>
    <h2>Create a demo account</h2>
    <form method="post" action="{{ url_for('signup') }}">
      <input type="hidden" name="form_token" value="{{ session.form_token }}">
      <p><label>Demo email <input type="email" name="email" maxlength="254" required></label></p>
      <p><label>Display name <input name="username" maxlength="80" required></label></p>
      <p><label>Demo password <input type="password" name="password" minlength="12" maxlength="128" required></label></p>
      <button>Create account</button>
    </form>
  {% endif %}
</main>
"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
