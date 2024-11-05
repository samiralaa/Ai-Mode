# face_recognition/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.verify, name='verify'),
    path('upload/', views.upload, name='upload'),
    path('get-uploaded/', views.get_uploaded, name='get_uploaded'),
    path('compare/', views.compare, name='compare'),
    path('recognition/', views.recognition, name='recognition'),
]


# public function login(Request $request)
#     {
#         $request->validate([
#             'email' => 'required|string|email',
#             'password' => 'required|string',
#             'login_video' => 'required|file|mimes:mp4,avi|max:20000' // Validate video file
#         ]);

#         $credentials = $request->only('email', 'password');

#         if (Auth::attempt($credentials)) {
#             $user = Auth::user();
#             $loginVideoPath = $request->file('login_video')->store('login_videos');

#             // Compare videos using API
#             $response = Http::post('https://finger-print-face-recognition.herokuapp.com/compare', [
#                 'video1' => Storage::path($user->face_video_path),
#                 'video2' => Storage::path($loginVideoPath)
#             ]);

#             if ($response->json('match')) {
#                 return response()->json(['message' => 'Login successful']);
#             } else {
#                 return response()->json(['message' => 'Face mismatch'], 401);
#             }
#         }

#         return response()->json(['message' => 'Invalid credentials'], 401);
#     }