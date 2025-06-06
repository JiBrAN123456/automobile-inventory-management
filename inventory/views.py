from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import VehicleMaster, CompanyInventory, VehicleMasterImage, CompanyInventoryImage, VehicleDocument
from .serializers import (
    VehicleMasterSerializer, CompanyInventorySerializer, 
    VehicleMasterImageSerializer, CompanyInventoryImageSerializer, VehicleDocumentSerializer
)
from rest_framework.filters import OrderingFilter , SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.exceptions import NotFound



class VehiclePagination(PageNumberPagination):
      page_size = 20
      page_size_query_param = 'page_size'
      max_page_size = 100    
        
      def paginate_queryset(self, queryset, request, view=None):
          
          try:
              return super().paginate_queryset(queryset, request , view)
          except NotFound:
              self.page = None
              return []

      def get_paginated_response(self, data):
          
          return Response({
              'count': self.page.paginator.count if self.page else 0,
              'results': data 
          })



class VehicleMasterViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = VehicleMaster.objects.all()
    serializer_class = VehicleMasterSerializer
    pagination_class = VehiclePagination  
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter]

    filterset_fields = ['brand', 'year', 'fuel_type' ]
    ordering_fields = ['year', 'brand']
    search_fields = ['brand', 'model']
    
    
    def get_queryset(self):
        queryset = VehicleMaster.objects.all().order_by("id")

        # ✅ Year Filtering Fix (Exclude 2024+ if not requested)
        min_year = self.request.query_params.get("year__gte")
        max_year = self.request.query_params.get("year__lte")

        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        if max_year:
            queryset = queryset.filter(year__lte=max_year)

        # ✅ Search Fix (Case-insensitive)
        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

        return queryset

class CompanyInventoryViewSet(viewsets.ModelViewSet):    
    queryset = CompanyInventory.objects.none()
    serializer_class = CompanyInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VehiclePagination 
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = [
        "vehicle__brand", "vehicle__year", "vehicle__fuel_type", "price", "quantity",
        "created_by__first_name", "created_by__last_name", "created_by__email", "created_by__phone_number"]
    

    ordering_fields = ["price", "quantity", "created_by__first_name", "created_by__last_name"]


    search_fields = ["vehicle__brand", "vehicle__model", "created_by__first_name", "created_by__last_name",  "created_by__phone_number"]

    
    def get_queryset(self):
        
        queryset = CompanyInventory.objects.filter(company=self.request.user.company)
        
        min_year = self.request.query_params.get("vehicle__year__gte")
        max_year = self.request.query_params.get("vehicle__year__lte")

        if min_year:
            queryset = queryset.filter(vehicle__year__gte=min_year)
        if max_year:
            queryset = queryset.filter(vehicle__year__lte=max_year)

        # ✅ Search Fix (Case-insensitive)
        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(vehicle__brand__icontains=search_query) | 
                Q(vehicle__model__icontains=search_query) |
                Q(created_by__first_name__icontains=search_query) | 
                Q(created_by__last_name__icontains=search_query)|
                Q(created_by__phone_number__icontains=search_query)

            )

        return queryset

   # def perform_create(self, serializer):
     #   serializer.save(company=self.request.user.company , created_by = self.request.user)               



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
    