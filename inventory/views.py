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

    filterset_fields = ["vehicle__brand", "vehicle__year", "vehicle__fuel_type", "price", "quantity"]
    ordering_fields = ["price", "quantity"]
    search_fields = ["vehicle__brand", "vehicle__model"]
    
    
    def get_queryset(self):
        
        queryset = CompanyInventory.objects.filter(company=self.request.user.company)
        

        min_price = self.request.query_params.get("price__gte")
        max_price = self.request.query_params.get("price__lte")

        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass


        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte= max_price) 
            except ValueError:
                pass


        return queryset


    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company , created_by = self.request.user)               



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
    