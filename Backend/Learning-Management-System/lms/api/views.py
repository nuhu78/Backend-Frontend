from django.shortcuts import render
from rest_framework import generics
from .models import Course, Enrollment, Lesson, Results, Submission, Teacher, Student, Profile, Assignment
from .serializers import TeacherSerializer, StudentSerializer, RegisterSerializer, loginSerializer,CourseSerializer, EnrollmentSerializer, LessonSerializer, AssignmentSerializer, SubmissionSerializer, ResultsSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



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
    """User registration view."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """Login view using phone and password."""

    def post(self, request):
        serializer = loginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            profile = Profile.objects.get(phone=phone)
            user = profile.user
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid phone or password'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Invalid phone or password'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'tokens': tokens
        })

def get_tokens_for_user(user):
    """Helper to get JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class profileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response({     
        'username': request.user.username,
        'phone': profile.phone,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    })
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer  
    permission_classes=[IsAuthenticated]
class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer  
    permission_classes=[IsAuthenticated]    

class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer  
    permission_classes=[IsAuthenticated]
class EnrollmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer  
    permission_classes=[IsAuthenticated]    

class LessonListCreateView(generics.ListCreateAPIView):
    """View to list and create lessons."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a lesson."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class AssignmentListCreateView(generics.ListCreateAPIView):
    """View to list and create assignments."""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

class AssignmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete an assignment."""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

class SubmissionListCreateView(generics.ListCreateAPIView):
    """View to list and create submissions."""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

class SubmissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a submission."""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

class ResultsListCreateView(generics.ListCreateAPIView):
    """View to list and create results."""
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    permission_classes = [IsAuthenticated]

class ResultsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a result."""
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    permission_classes = [IsAuthenticated]