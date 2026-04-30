from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Teacher, Student, Profile, Course, Enrollment, Lesson, Assignment,Submission,Results

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'subject', 'is_active']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'enrollment_date', 'is_active', 'roll_number']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        default='STUDENT'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        Profile.objects.create(user=user, role=role)

        return user
    
class loginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'lesson', 'course', 'due_date']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'student', 'assignment', 'submitted_at', 'content']
        read_only_fields = ['submitted_at']

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['id', 'submission', 'score', 'feedback']

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    phone = serializers.CharField(source='profile.phone', required=False)
    address = serializers.CharField(source='profile.address', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone',
            'address',
            'bio',
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile = instance.profile
        profile.phone = profile_data.get('phone', profile.phone)
        profile.address = profile_data.get('address', profile.address)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()

        return instance