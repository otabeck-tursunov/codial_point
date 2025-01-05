from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .serializers import *
from .permissions import *


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]  # Hammasi ko'ra oladi


class GroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Group.objects.all()
        elif hasattr(user, 'mentor'):
            return Group.objects.filter(mentor=user.mentor)
        return Group.objects.none()


class MentorDetailView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsMentor]

    def get_object(self):
        return get_object_or_404(Mentor, user=self.request.user)


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        elif hasattr(user, 'mentor'):
            return Student.objects.filter(group__mentor=user.mentor)
        return Student.objects.none()


class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        return get_object_or_404(Student, user=self.request.user)


class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        # Faqat o'z useriga tegishli bo'lgan studentni qaytaradi
        return Student.objects.get(user=self.request.user)


class PointTypeListView(generics.ListAPIView):
    queryset = PointType.objects.all()
    serializer_class = PointTypeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Hammasi ko'ra oladi


class GivePointListView(generics.ListAPIView):
    serializer_class = GivePointSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return GivePoint.objects.all()
        elif hasattr(user, 'mentor'):
            return GivePoint.objects.filter(mentor=user.mentor)
        elif hasattr(user, 'student'):
            return GivePoint.objects.filter(student=user.student)
        return GivePoint.objects.none()


class GivePointCreateView(generics.CreateAPIView):
    serializer_class = GivePointSerializer
    permission_classes = [IsMentor]

    def perform_create(self, serializer):
        user = self.request.user
        mentor = user.mentor

        # Validatsiya: mentor faqat o'z guruhidagi studentlarga ball berishi kerak
        student = serializer.validated_data['student']
        if student.group.mentor != mentor:
            raise serializers.ValidationError("You can only give points to students in your own groups.")
        serializer.save(mentor=mentor)
