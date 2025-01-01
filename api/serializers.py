# serializers.py
from rest_framework import serializers
from .models import CustomUser, Graduate
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import sys
from cloudinary.forms import CloudinaryFileField


class GraduateRegistrationSerializer(serializers.Serializer):
    # Fields for the CustomUser
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(max_length=6, read_only=True)
    is_verified = serializers.BooleanField(default=False)

    # Fields for the Graduate profile
    phone_number = serializers.CharField(max_length=15)
    date_of_birth = serializers.DateField()
    # is_verified = serializers.BooleanField(default=False)
    # otp = serializers.CharField(max_length=6, )
    gender = serializers.CharField(max_length=10)
    profile_picture = CloudinaryFileField(required=True)
    address = serializers.CharField(max_length=255)
    institution = serializers.CharField(max_length=255)
    course_studied = serializers.CharField(max_length=255)
    year_of_graduation = serializers.DateField()
    degrees_obtained = serializers.ListField(
        child=serializers.ChoiceField(
            # or a simpler approach
            choices=[('BSc', 'BSc'), ('SSCE', 'SSCE'), ('OND', 'OND'), ('HND', 'HND')])
    )
    skills = serializers.CharField(max_length=255)
    experience = serializers.CharField(max_length=255)
    aspirations = serializers.CharField(max_length=255)
    preffered_job = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[('Job1', 'Job1'), ('Job2', 'Job2'), ('Job3', 'Job3')])
    )
    relocate = serializers.CharField(max_length=255)
    cv = CloudinaryFileField(required=True)
    relocation_availability = serializers.CharField(max_length=255)
    comments = serializers.CharField(required=False)
    reference = serializers.CharField(max_length=255)
    reference_phone_number = serializers.CharField(max_length=15)
    reference_relationship = serializers.CharField(max_length=225)
    reference_1 = serializers.CharField(max_length=255)
    reference_phone_number_1 = serializers.CharField(max_length=15)
    reference_relationship_1 = serializers.CharField(max_length=225)

    def create(self, validated_data):
        """
        1. Create a CustomUser.
        2. Create a Graduate linked to that user.
        """
        # Extract user fields
        email = validated_data.pop('email')
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')

        is_verified = validated_data.pop('is_verified')

        # Create the user
        user = CustomUser.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,

            is_verified=is_verified
        )
        profile_picture = validated_data.get('profile_picture')
        if profile_picture:
            # Opens the image with Pillow to proces it
            image = Image.open(profile_picture)

            #  resizes the image if larger than 800x800
            max_size = (800, 800)
            image.thumbnail(max_size, Image.LANCZOS)

            # Save to memory buffer
            image_io = io.BytesIO()
            # You can choose 'JPEG' or use image.format if you want the same format
            image.save(image_io, format='JPEG', quality=90)
            image_io.seek(0)

            processed_image = InMemoryUploadedFile(
                file=image_io,
                field_name='profile_picture',
                name='processed.jpg',              # A new filename
                content_type='image/jpeg',         # Or 'image/png' if you used PNG
                size=sys.getsizeof(image_io),
                charset=None
            )
            validated_data['profile_picture'] = processed_image
        # Create the Graduate profile (the rest of the fields)
        graduate = Graduate.objects.create(
            user=user,
            **validated_data

        )

        return graduate  # or return user if you want

    def to_representation(self, instance):
        """
        Show any fields you want in the response,
        e.g., the Graduate’s ID, user’s email, etc.
        """
        return {
            "graduate_id": str(instance.id),
            "email": instance.user.email,
            "full_name": instance.user.full_name,
            "phone_number": instance.phone_number,
            "cv": instance.cv,
            "profile_picture":  instance.profile_picture if instance.profile_picture else None,
            "address": instance.address,
            # ... any other fields
        }
