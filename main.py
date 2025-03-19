from flask import Flask, request, render_template, redirect
from google.cloud import firestore
import shortuuid

app = Flask(__name__)

# Initialize Firestore
db = firestore.Client()
urls_ref = db.collection('urls')

# Home Page - URL Submission
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_id = shortuuid.ShortUUID().random(length=6)

        # Store in Firestore
        urls_ref.document(short_id).set({"long_url": long_url})
        
        return render_template("short_url.html", short_id=short_id)

    return render_template("index.html")

# Redirect Short URL to Original URL
@app.route("/<short_id>")
def redirect_url(short_id):
    doc = urls_ref.document(short_id).get()

    if doc.exists:
        return redirect(doc.to_dict()["long_url"])
    else:
        return "URL Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)
