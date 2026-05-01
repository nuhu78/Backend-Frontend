from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('categories', views.CourseCategoryViewSet, basename='categories')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollments')
router.register('admin/users', views.AdminUserViewSet, basename='admin-users')


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




   
   path('lessons/',views.LessonListCreateView.as_view(),name='lesson-list-create'),
   path('lessons/<int:pk>/',views.LessonRetrieveUpdateDestroyAPIView.as_view(),name='lesson-detail'),

   path('assignments/',views.AssignmentListCreateView.as_view(),name='assignment-list-create'),
   path('assignments/<int:pk>/',views.AssignmentRetrieveUpdateDestroyAPIView.as_view(),name='assignment-detail'),

   path('submissions/',views.SubmissionListCreateView.as_view(),name='submission-list-create'),
   path('submissions/<int:pk>/',views.SubmissionRetrieveUpdateDestroyAPIView.as_view(),name='submission-detail'),
   
   path('results/',views.ResultsListCreateView.as_view(),name='results-list-create'),
   path('results/<int:pk>/',views.ResultsRetrieveUpdateDestroyAPIView.as_view(),name='results-detail'),
]

urlpatterns += router.urls
