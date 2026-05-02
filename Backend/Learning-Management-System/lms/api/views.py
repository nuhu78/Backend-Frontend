from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Course, Enrollment, Lesson, Results, Submission, Teacher, Student, Profile, Assignment, CourseCategory
from .serializers import AdminUserSerializer, TeacherSerializer, StudentSerializer, RegisterSerializer, loginSerializer,CourseSerializer, EnrollmentSerializer, LessonSerializer, AssignmentSerializer, SubmissionSerializer, ResultsSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, CourseCategorySerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date

from .permissions import (
    get_user_role,
    IsAdminRole,
    IsAdminOrInstructor,
    IsStudentRole,
    IsCourseOwnerOrAdmin,
    IsEnrollmentOwnerOrAdminOrInstructor,
    IsLessonOwnerOrAdminOrInstructor,
    IsAssignmentOwnerOrAdminOrInstructor,
    IsSubmissionOwnerOrAdminOrInstructor,
    IsResultOwnerOrAdminOrInstructor,
)

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password



# Create your views here.
class TeacherListCreateView(generics.ListCreateAPIView):
    """View to list and create teachers."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes=[IsAuthenticated]

class TeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a teacher."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes=[IsAuthenticated]

class StudentListCreateView(generics.ListCreateAPIView):
    """View to list and create students."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes=[IsAuthenticated]

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a student."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes=[IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = loginSerializer(data={
            'identifier': request.data.get('identifier') or request.data.get('username') or request.data.get('phone'),
            'password': request.data.get('password'),
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        identifier = serializer.validated_data['identifier']
        password = serializer.validated_data['password']

        user = User.objects.filter(username=identifier).first()

        if user is None:
            user = User.objects.filter(profile__phone=identifier).first()

        if user is None or not check_password(password, user.password):
            return Response({
                'error': 'Invalid username, phone, or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all().order_by('name')
    serializer_class = CourseCategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]

        return [IsAdminRole()]

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Course.objects.all().order_by('-created_at')

        if role == 'INSTRUCTOR':
            return Course.objects.filter(instructor=user).order_by('-created_at')

        return Course.objects.filter(is_published=True).order_by('-created_at')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]

        if self.action == 'create':
            return [IsAdminOrInstructor()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCourseOwnerOrAdmin()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Enrollment.objects.all().order_by('-enrolled_at')

        if role == 'INSTRUCTOR':
            return Enrollment.objects.filter(
                course__instructor=user
            ).order_by('-enrolled_at')

        return Enrollment.objects.filter(
            student=user
        ).order_by('-enrolled_at')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]

        if self.action == 'create':
            return [IsStudentRole()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [
                permissions.IsAuthenticated(),
                IsEnrollmentOwnerOrAdminOrInstructor()
            ]

        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')

        if not course_id:
            return Response({
                'error': 'Course ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id, is_published=True)
        except Course.DoesNotExist:
            return Response({
                'error': 'Course not found or not published'
            }, status=status.HTTP_404_NOT_FOUND)

        already_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

        if already_enrolled:
            return Response({
                'error': 'You are already enrolled in this course'
            }, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course
        )

        serializer = self.get_serializer(enrollment)

        return Response({
            'message': 'Enrollment successful',
            'enrollment': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated()]

        return [IsStudentRole()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user) 

class LessonListCreateView(generics.ListCreateAPIView):
    """View to list and create lessons."""
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Lesson.objects.select_related('course').all().order_by('id')

        if role == 'INSTRUCTOR':
            return Lesson.objects.select_related('course').filter(course__instructor=user).order_by('id')

        return Lesson.objects.select_related('course').filter(course__is_published=True).order_by('id')

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAdminOrInstructor()]

    def perform_create(self, serializer):
        serializer.save()

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a lesson."""
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.select_related('course').all()

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsLessonOwnerOrAdminOrInstructor()]

class AssignmentListCreateView(generics.ListCreateAPIView):
    """View to list and create assignments."""
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Assignment.objects.select_related('course', 'lesson').all().order_by('id')

        if role == 'INSTRUCTOR':
            return Assignment.objects.select_related('course', 'lesson').filter(course__instructor=user).order_by('id')

        return Assignment.objects.select_related('course', 'lesson').filter(course__is_published=True).order_by('id')

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAdminOrInstructor()]

    def perform_create(self, serializer):
        serializer.save()

class AssignmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete an assignment."""
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.select_related('course', 'lesson').all()

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsAssignmentOwnerOrAdminOrInstructor()]

class SubmissionListCreateView(generics.ListCreateAPIView):
    """View to list and create submissions."""
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Submission.objects.select_related('student', 'assignment', 'assignment__course').all().order_by('id')

        if role == 'INSTRUCTOR':
            return Submission.objects.select_related('student', 'assignment', 'assignment__course').filter(
                assignment__course__instructor=user
            ).order_by('id')

        return Submission.objects.select_related('student', 'assignment', 'assignment__course').filter(
            student__email=user.email
        ).order_by('id')

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsStudentRole()]

    def create(self, request, *args, **kwargs):
        if get_user_role(request.user) != 'STUDENT':
            return Response({
                'error': 'Only students can create submissions'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student, _ = Student.objects.get_or_create(
            email=request.user.email,
            defaults={
                'name': request.user.username,
                'enrollment_date': date.today(),
            }
        )

        submission = serializer.save(student=student)
        output = self.get_serializer(submission)

        return Response({
            'message': 'Submission created successfully',
            'submission': output.data,
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        student, _ = Student.objects.get_or_create(
            email=self.request.user.email,
            defaults={
                'name': self.request.user.username,
                'enrollment_date': date.today(),
            }
        )
        serializer.save(student=student)

class SubmissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a submission."""
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Submission.objects.select_related('student', 'assignment', 'assignment__course').all()

        if role == 'INSTRUCTOR':
            return Submission.objects.select_related('student', 'assignment', 'assignment__course').filter(
                assignment__course__instructor=user
            )

        return Submission.objects.select_related('student', 'assignment', 'assignment__course').filter(
            student__email=user.email
        )

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsSubmissionOwnerOrAdminOrInstructor()]

class ResultsListCreateView(generics.ListCreateAPIView):
    """View to list and create results."""
    serializer_class = ResultsSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').all().order_by('id')

        if role == 'INSTRUCTOR':
            return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').filter(
                submission__assignment__course__instructor=user
            ).order_by('id')

        return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').filter(
            submission__student__email=user.email
        ).order_by('id')

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAdminOrInstructor()]

    def perform_create(self, serializer):
        serializer.save()

class ResultsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a result."""
    serializer_class = ResultsSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == 'ADMIN':
            return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').all()

        if role == 'INSTRUCTOR':
            return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').filter(
                submission__assignment__course__instructor=user
            )

        return Results.objects.select_related('submission', 'submission__student', 'submission__assignment', 'submission__assignment__course').filter(
            submission__student__email=user.email
        )

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsResultOwnerOrAdminOrInstructor()]

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                'message': serializer.validated_data['message']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                'message': serializer.validated_data['message']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminRole]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        return Response({
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'inactive_users': User.objects.filter(is_active=False).count(),
            'role_counts': {
                'ADMIN': User.objects.filter(profile__role='ADMIN').count(),
                'INSTRUCTOR': User.objects.filter(profile__role='INSTRUCTOR').count(),
                'STUDENT': User.objects.filter(profile__role='STUDENT').count(),
            },
        })


class DashboardSummaryView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({
            'users_total': User.objects.count(),
            'courses_total': Course.objects.count(),
            'published_courses': Course.objects.filter(is_published=True).count(),
            'categories_total': CourseCategory.objects.count(),
            'enrollments_total': Enrollment.objects.count(),
            'active_enrollments': Enrollment.objects.filter(is_active=True).count(),
            'role_counts': {
                'ADMIN': User.objects.filter(profile__role='ADMIN').count(),
                'INSTRUCTOR': User.objects.filter(profile__role='INSTRUCTOR').count(),
                'STUDENT': User.objects.filter(profile__role='STUDENT').count(),
            },
        })   