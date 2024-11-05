# face_recognition/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import secrets
from pathlib import Path
import glob
import face_recognition
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import modelFaceDetect  # Adjust this import based on your actual model

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def index(request):
    return HttpResponse("hello world ")

@csrf_exempt
def verify(request):
    if request.method == "POST":
        if "known" not in request.FILES:
            return HttpResponse("not found unknown or known image ")
        known = request.FILES["known"]
        known_image = face_recognition.load_image_file(known)
        face2 = face_recognition.face_locations(known_image)
        if not face2:
            return HttpResponse("0")
        return HttpResponse("1")

@csrf_exempt
def upload(request):
    if request.method == "POST":
        if "image" not in request.FILES:
            return HttpResponse("not found image ")
        file = request.FILES["image"]
        name, ext = os.path.splitext(file.name)
        file_name = f"{request.POST['id']}.{secure_filename(ext)}"
        file_path = Path(settings.MEDIA_ROOT, file_name)
        default_storage.save(file_path, ContentFile(file.read()))
        return HttpResponse("1")

@csrf_exempt
def get_uploaded(request):
    files = glob.glob(os.path.join(settings.MEDIA_ROOT, "*"))
    return HttpResponse("\n".join(files))

@csrf_exempt
def compare(request):
    if request.method == "POST":
        if "unknown" not in request.FILES or "known" not in request.FILES:
            return HttpResponse("not found unknown or known image ")
        known = request.FILES["known"]
        unknown = request.FILES["unknown"]
        if not (allowed_file(known.name) and allowed_file(unknown.name)):
            return HttpResponse("file known or unknown extension not valid")

        known_image = face_recognition.load_image_file(known)
        unknown_image = face_recognition.load_image_file(unknown)
        face2 = face_recognition.face_locations(unknown_image)
        known_encoding = face_recognition.face_encodings(known_image)
        unknown_encoding = face_recognition.face_encodings(unknown_image, face2)

        for face_encoding in unknown_encoding:
            results = face_recognition.compare_faces(known_encoding, face_encoding)
            face_distances = face_recognition.face_distance(known_encoding, face_encoding)
            if results[0] and face_distances[0] <= 0.55:
                return HttpResponse("1")
        return HttpResponse("0")

@csrf_exempt
def recognition(request):
    if request.method == "POST":
        if "unknown" not in request.FILES:
            return HttpResponse("not found unknown or known image ")
        unknown = request.FILES["unknown"]
        known_images = glob.glob(os.path.join(settings.MEDIA_ROOT, "*"))
        known_images = [face_recognition.load_image_file(path) for path in known_images]
        unknown_image = face_recognition.load_image_file(unknown)

        known_encoding = [
            face_recognition.face_encodings(known_image)[0] for known_image in known_images
        ]
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        for face_encoding in unknown_encoding:
            results = face_recognition.compare_faces(known_encoding, face_encoding)
            face_distances = face_recognition.face_distance(known_encoding, face_encoding)
            i = 0
            for result in results:
                if result:
                    return HttpResponse(os.path.split(os.path.splitext(known_images[i])[0])[1])
                i += 1
        return HttpResponse("0")
