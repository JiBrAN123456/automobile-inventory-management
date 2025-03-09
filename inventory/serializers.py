from rest_framework import serializers
from .models import VehicleMaster, CompanyInventory, VehicleDocument, VehicleMasterImage, CompanyInventoryImage



class VehicleMasterImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleMasterImage
        fields = "__all__"


# 1️⃣ Master Inventory Serializer
class VehicleMasterSerializer(serializers.ModelSerializer):
    images = VehicleMasterImageSerializer(many=True,read_only = True)

    class Meta:
        model = VehicleMaster
        fields = "__all__"



# 5️⃣ Vehicle Document Serializer
class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        fields = "__all__"



# 4️⃣ Company Inventory Image Serializer
class CompanyInventoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInventoryImage
        fields = "__all__"



# 3️⃣ Company Inventory Serializer
class CompanyInventorySerializer(serializers.ModelSerializer):
    vehicle = VehicleMasterSerializer(read_only=True)  # Nested serializer
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=VehicleMaster.objects.all(), write_only = True)


    images = CompanyInventoryImageSerializer(many=True, read_only=True)  # Include images
    documents = VehicleDocumentSerializer(many=True, read_only=True)  # Include documents

    class Meta:
        model = CompanyInventory
        fields = "__all__"
        read_only_fields = ["company", "created_by"]
        extra_kwargs = {'vehicle' : {'read_only':True}}

    def create(self,validated_data):

        user = self.context['request'].user
        vehicle_master = validated_data.pop("vehicle_id")

        inventory = CompanyInventory.objects.create(
            company = user.company , created_by = user , vehicle = vehicle_master , **validated_data
        )
        return inventory 
