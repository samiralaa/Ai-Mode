# from dist import pytransform
import os
import secrets
from pathlib import Path
import glob

from flask import Flask, request
from werkzeug.utils import secure_filename
from models import modelFaceDetect
import face_recognition

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "images"
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["get"])
def index():
    return "hello world "


@app.route("/verify", methods=["POST"])
def verify():
    if "known" not in request.files:
        return "not found unknown or known image "
    known = request.files["known"]
    known_image = face_recognition.load_image_file(known)
    face2 = face_recognition.face_locations(known_image)
    if not face2:
        return "0"
    return "1"


@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return "not found image "
    file = request.files["image"]

    name, ext = os.path.splitext(file.filename)
    fileName = f"{request.form['id']}.{secure_filename(ext)}"

    print(fileName)
    file.save(Path(app.config["UPLOAD_PATH"], fileName))
    return "1"


@app.route("/get-uploaded", methods=["get"])
def getUpload():
    return glob.glob("images/*")


@app.route("/compare", methods=["POST"])
def compare():
    if ("unknown" not in request.files) or ("known" not in request.files):
        return "not found unknown or known image "

    known = request.files["known"]
    unknown = request.files["unknown"]
    # print(allowed_file(unknown.filename))
    if known.filename == "" or unknown.filename == "":
        return "has no name in know or unknown"
    if not (known and allowed_file(known.filename)) or not (
        unknown and allowed_file(unknown.filename)
    ):
        return "file known or unknown extension not valid"

    known_image = face_recognition.load_image_file(known)
    unknown_image = face_recognition.load_image_file(unknown)

    face2 = face_recognition.face_locations(unknown_image)

    known_encoding = face_recognition.face_encodings(known_image)
    unknown_encoding = face_recognition.face_encodings(unknown_image, face2)

    print(unknown_encoding)
    for face_encoding in unknown_encoding:

        results = face_recognition.compare_faces(known_encoding, face_encoding)
        print(results)

        face_distances = face_recognition.face_distance(known_encoding, face_encoding)

        # best_match_index = np.argmin(face_distances)
        print(face_distances)
        if results[0] and face_distances[0] <= 0.55:
            return "1"

    return "0"


@app.route("/recognition", methods=["POST"])
def recognition():
    if "unknown" not in request.files:
        return "not found unknown or known image "

    unknown = request.files["unknown"]
    # print(allowed_file(unknown.filename))
    known = glob.glob("images/*")
    print(known)

    known_images = [face_recognition.load_image_file(path) for path in known]
    unknown_image = face_recognition.load_image_file(unknown)

    face2 = face_recognition.face_locations(unknown_image)

    known_encoding = [
        face_recognition.face_encodings(known_image)[0] for known_image in known_images
    ]
    unknown_encoding = face_recognition.face_encodings(unknown_image, face2)

    print(unknown_encoding)
    for face_encoding in unknown_encoding:

        results = face_recognition.compare_faces(known_encoding, face_encoding)
        print(results)

        face_distances = face_recognition.face_distance(known_encoding, face_encoding)
        print(face_distances)

        # best_match_index = np.argmin(face_distances)
        print(face_distances)
        i = 0

        for result in results:
            if result:
                return os.path.split(os.path.splitext(known[i])[0])[1]
            i += 1

    return "0"


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, host="0.0.0.0", port=port)
