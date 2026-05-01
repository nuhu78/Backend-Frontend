from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('teacher', views.TeacherListCreateView, basename='teacher')
# router.register('student', views.StudentListCreateView, basename='student')
# router.register('register', views.RegisterView, basename='register')


urlpatterns = [
   # path('', include(router.urls)),
     path('auth/register/',views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),

    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),

   path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('teachers/',views.TeacherListCreateView.as_view(),name='teacher-list-create'),
   path('teachers/<int:pk>/',views.TeacherRetrieveUpdateDestroyView.as_view(),name='teacher-detail'),

   path('students/',views.StudentListCreateView.as_view(),name='student-list-create'),
   path('students/<int:pk>/',views.StudentRetrieveUpdateDestroyView.as_view(),name='student-detail'),



   path('courses/',views.CourseListCreateView.as_view(),name='course-list-create'),
   path('courses/<int:pk>/',views.CourseRetrieveUpdateDestroyView.as_view(),name='course-detail'),

   path('enrollments/',views.EnrollmentListCreateView.as_view(),name='enrollment-list-create'),
   path('enrollments/<int:pk>/',views.EnrollmentRetrieveUpdateDestroyView.as_view(),name='enrollment-detail'),

   path('lessons/',views.LessonListCreateView.as_view(),name='lesson-list-create'),
   path('lessons/<int:pk>/',views.LessonRetrieveUpdateDestroyAPIView.as_view(),name='lesson-detail'),

   path('assignments/',views.AssignmentListCreateView.as_view(),name='assignment-list-create'),
   path('assignments/<int:pk>/',views.AssignmentRetrieveUpdateDestroyAPIView.as_view(),name='assignment-detail'),

   path('submissions/',views.SubmissionListCreateView.as_view(),name='submission-list-create'),
   path('submissions/<int:pk>/',views.SubmissionRetrieveUpdateDestroyAPIView.as_view(),name='submission-detail'),
   
   path('results/',views.ResultsListCreateView.as_view(),name='results-list-create'),
   path('results/<int:pk>/',views.ResultsRetrieveUpdateDestroyAPIView.as_view(),name='results-detail'),
   
]