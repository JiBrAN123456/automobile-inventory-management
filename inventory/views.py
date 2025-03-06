from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import VehicleMaster, CompanyInventory, VehicleMasterImage, CompanyInventoryImage, VehicleDocument
from .serializers import (
    VehicleMasterSerializer, CompanyInventorySerializer, 
    VehicleMasterImageSerializer, CompanyInventoryImageSerializer, VehicleDocumentSerializer
)

class VehicleMasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleMaster.objects.all()
    serializer_class = VehicleMasterSerializer
    permission_classes = [permissions.AllowAny]



class CompanyInventoryViewSet(viewsets.ModelViewSet):    
    queryset = CompanyInventory.objects.none()
    serializer_class = CompanyInventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyInventory.objects.filter(company= self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company= self.request.user.company, created_by= self.request.user)


class VehicleMasterImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleMasterImage.objects.all()
    serializer_class = VehicleMasterImageSerializer
    permission_classes = [permissions.AllowAny]


class CompanyInventoryImageViewSet(viewsets.ModelViewSet):
    queryset = CompanyInventoryImage.objects.all()
    serializer_class = CompanyInventoryImageSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return CompanyInventoryImage.objects.filter(inventory__company=self.request.user.company)
    

class VehicleDocumentViewSet(viewsets.ModelViewSet):
    queryset = VehicleDocument.objects.all()
    serializer_class = VehicleDocumentSerializer 
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return VehicleDocument.objects.filter(inventory__company=self.request.user.company)  