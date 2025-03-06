from rest_framework import serializers
from .models import VehicleMaster, CompanyInventory, VehicleDocument, VehicleMasterImage, CompanyInventoryImage

# 1️⃣ Master Inventory Serializer
class VehicleMasterSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)  # Include images

    class Meta:
        model = VehicleMaster
        fields = "__all__"

# 2️⃣ Master Inventory Image Serializer
class VehicleMasterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMasterImage
        fields = "__all__"

# 3️⃣ Company Inventory Serializer
class CompanyInventorySerializer(serializers.ModelSerializer):
    vehicle = VehicleMasterSerializer(read_only=True)  # Nested serializer
    images = serializers.StringRelatedField(many=True, read_only=True)  # Include images
    documents = serializers.StringRelatedField(many=True, read_only=True)  # Include documents

    class Meta:
        model = CompanyInventory
        fields = "__all__"

# 4️⃣ Company Inventory Image Serializer
class CompanyInventoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInventoryImage
        fields = "__all__"

# 5️⃣ Vehicle Document Serializer
class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        fields = "__all__"
