from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleMasterViewSet, CompanyInventoryViewSet, 
    VehicleMasterImageViewSet, CompanyInventoryImageViewSet, VehicleDocumentViewSet
)

# Using DRF's router for automatic URL handling
router = DefaultRouter()
router.register(r'master-inventory', VehicleMasterViewSet, basename='vehicle-master')
router.register(r'company-inventory', CompanyInventoryViewSet, basename='company-inventory')
router.register(r'master-images', VehicleMasterImageViewSet, basename='vehicle-master-images')
router.register(r'company-images', CompanyInventoryImageViewSet, basename='company-inventory-images')
router.register(r'documents', VehicleDocumentViewSet, basename='vehicle-documents')

urlpatterns = [
    path('', include(router.urls)),  # Include all registered endpoints
]
