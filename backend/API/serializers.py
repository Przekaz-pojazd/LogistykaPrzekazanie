from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import (
    Truck,
    TruckEquipment,
    SemiTrailer,
    SemiTrailerEquipment
)
CustomUser = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

        def create(self, clean_data):
            user_obj = CustomUser.objects.create_user(email=clean_data['email'],
                                                      password=clean_data['password'])
            user_obj.save()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValueError('user not found')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


"""
    Trucks Serializers
"""
class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def __delete__(self, instance):
        instance.delete()

class SemiTrailerEquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailerEquipment
        fields = '__all__'


class TruckSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def create(self, validated_data):
        return Truck.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.power = validated_data.get('power', instance.power)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.driven_length = validated_data.get('driven_length', instance.driven_length)
        instance.production_date = validated_data.get('production_date', instance.production_date)
        instance.available = validated_data.get('available', instance.available)
        instance.save()
        return instance

    def check_existance(self, validated_data):
        truck = Truck.objects.filter(**validated_data)
        print(not truck)
        if not truck:
            return False
        return True

class TruckEqupmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckEquipment
        fields = '__all__'
"""
    Sami trucks serializers
"""
class SemiTrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailer
        fields = ('brand', 'model')
