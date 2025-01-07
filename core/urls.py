from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Codial Gamification App's API",
        default_version='v1',
        description="Codial Gamification App's API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="otabekpm@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('users/get-me/', UserDetailView.as_view(), name='user-details'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('mentors/get-me/', MentorDetailView.as_view(), name='mentor-details'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/get-me/', StudentDetailView.as_view(), name='student-details'),
    path('students/update/', StudentUpdateView.as_view(), name='student-update'),
    path('point-types/', PointTypeListView.as_view(), name='point-type-list'),
    path('give-points/', GivePointListView.as_view(), name='give-point-list'),
    path('give-points/create/', GivePointCreateView.as_view(), name='give-point-create'),
]
