from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Teacher, Student, Profile, Course, Enrollment, Lesson, Assignment,Submission,Results, CourseCategory
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

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
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        default='STUDENT'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        role = validated_data.pop('role')
        phone = validated_data.pop('phone', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        profile = Profile.objects.create(user=user, role=role)

        if phone:
            profile.phone = phone
            profile.save(update_fields=['phone'])

        return user
    
class loginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)    
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'description']


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source='instructor.username',
        read_only=True
    )
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_name',
            'instructor',
            'instructor_name',
            'level',
            'price',
            'is_published',
            'created_at',
        ]
        read_only_fields = ['instructor', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.username',
        read_only=True
    )
    course_title = serializers.CharField(
        source='course.title',
        read_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'student_name',
            'course',
            'course_title',
            'enrolled_at',
            'is_active',
        ]
        read_only_fields = ['student', 'enrolled_at']
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
    role = serializers.CharField(source='profile.role', required=False)
    phone = serializers.CharField(source='profile.phone', required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(source='profile.address', required=False, allow_blank=True, allow_null=True)
    bio = serializers.CharField(source='profile.bio', required=False, allow_blank=True, allow_null=True)

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

    def to_representation(self, instance):
        Profile.objects.get_or_create(user=instance)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.address = profile_data.get('address', profile.address)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()

        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'No user found with this email'
            })

        uid = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

        send_mail(
            subject='LMS Password Reset',
            message=f'Use this link to reset your password: {reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        attrs['message'] = 'Password reset link sent successfully'
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except Exception:
            raise serializers.ValidationError({
                'error': 'Invalid reset link'
            })

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({
                'error': 'Invalid or expired token'
            })

        user.set_password(new_password)
        user.save()

        return {
            'message': 'Password reset successful'
        }    
    
class AdminUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'date_joined',
        ]

    def to_representation(self, instance):
        Profile.objects.get_or_create(user=instance)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        profile, _ = Profile.objects.get_or_create(user=instance)

        if 'role' in profile_data:
            profile.role = profile_data['role']
            profile.save(update_fields=['role'])

        return instance   