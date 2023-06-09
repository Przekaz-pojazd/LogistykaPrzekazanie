import datetime
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import (
    Truck,
    TruckEquipment,
    SemiTrailer,
    SemiTrailerEquipment,
    VehicleReceivment,
    TruckComplainPhoto,
    SemiTrailerComplainPhoto,
    FaultReportPhoto
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

    def update(self, instance, validated_data):
        instance.surname = validated_data.get('surname', instance.surname)
        instance.city = validated_data.get('city', instance.city)
        instance.region = validated_data.get('region', instance.region)
        instance.email = validated_data.get('email', instance.email)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.mobile_phone = validated_data.get('mobile_phone', instance.mobile_phone)
        instance.username = validated_data.get('username', instance.username)
        instance.is_staff = validated_data.get('staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.own_truck = validated_data.get('own_truck', instance.own_truck)
        instance.save()
        return instance
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

    def create(self, validated_data):
        equipment = SemiTrailerEquipment.objects.create(**validated_data)
        return equipment

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
        instance.registration_number = validated_data.get(
            'registration_number',
             instance.registration_number)
        instance.driven_length = validated_data.get('driven_length',
                                                    instance.driven_length)
        instance.production_date = validated_data.get('production_date',
                                                      instance.production_date)
        instance.avaiable = validated_data.get('avaiable', instance.avaiable)
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

    def create(self, validated_data):
        equipment = TruckEquipment.objects.create(**validated_data)
        return equipment


"""
    Sami trucks serializers
"""
class SemiTrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailer
        fields = '__all__'

    def check_existance(self, validated_data):
        samitrailer = SemiTrailer.objects.filter(**validated_data)
        if not samitrailer:
            return False
        return True

    def create(self, validated_data):
        return SemiTrailer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.production_year = validated_data.get('production_year',
                                                      instance.production_year)
        instance.registration_number = validated_data.get('registration_number',
                                                          instance.registration_number)
        instance.semi_note = validated_data.get('semi_note', instance.semi_note)
        instance.avaiable = validated_data.get('avaiable', instance.avaiable)
        instance.save()
        print("naura")
        return instance


class VehicleReceivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleReceivment
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user')
        receivments = VehicleReceivment.objects.filter(user=user)
        truck = validated_data.get('truck')
        if truck:
            print("esa121")
            truck.set_availability('Zaje')
            truck.save()
        semi_truck = validated_data.get('semi_trailer')
        semi_truck.set_availability('Zaje')
        semi_truck.save()
        print(semi_truck)
        receivments_status_end = receivments.values_list('data_ended', flat=True)
        print(receivments_status_end)
        user_receivements_exist = any(receivments is None for receivments in receivments_status_end)
        print(user_receivements_exist)
        if not user_receivements_exist:
            vehicle = VehicleReceivment.objects.create(**validated_data)
            return vehicle
        raise IntegrityError("Record exist in db maybe all is reserved")

    def finish_action(self, validated_data):
        user = validated_data.get('user')
        truck = validated_data.get('truck')
        if truck.avaiable == ["Zaje", "Awar"]:
            truck.set_availability('Woln')
        else:
            truck.set_availability('Woln')
        truck.save()
        semi_trailer = validated_data.get('semi_trailer')
        if semi_trailer.avaiable ==  ["Zaje", "Awar"]:
            semi_trailer.set_availability("Woln")
        else:
            semi_trailer.set_availability('Woln')
        semi_trailer.save()
        print('zamiana stanów')
        try:
            receivment_statement = VehicleReceivment.objects.create(**validated_data)
            return receivment_statement
        except IntegrityError:
            print("Data exist in db or data is not properly")

    def finish_by_admin(self, instance, validated_data):
        print('Zakonczenie przez admina')
        instance.data_ended = validated_data.get('data_ended')
        instance.user = validated_data.get('user')
        instance.save()

    def update(self, instance, validated_data):
        instance.date_ended = validated_data.get('date_ended', instance.date_ended)
        instance.save()
        return instance

    def update_target(self,instance, validated_data):
        instance.target_address = validated_data.get('target_address',
                                                     instance.target_address)
        instance.save()
    def update_complain_state(self, instance, validated_data):
        instance.complain = validated_data.get('complain', instance.complain)
        instance.save()
        return instance

    def check_existance(self, validated_data):
        truck = VehicleReceivment.objects.filter(**validated_data)
        print(not truck)
        if not truck:
            return False
        return True


class TruckPhotoComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckComplainPhoto
        fields = '__all__'

    def create(self, validated_data):
        print(type(self.fields))
        if isinstance(validated_data.get('receivment'),VehicleReceivment):
            print("Hello world")
        print(validated_data.get('receivment'))
        print(validated_data.get('truck_photo'))
        photo = TruckComplainPhoto.objects.create(receivment=validated_data.get('receivment'),
                                                  truck_photo=validated_data.get('truck_photo'))
        return photo

class SemiTrailerComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailerComplainPhoto
        fields = "__all__"

    def create(self, validated_data):
        complain_photo = SemiTrailerComplainPhoto.objects.create(
            receivment=validated_data.get('receivment'),
            semitrailer_photo=validated_data.get('semitrailer_photo'))
        return complain_photo

class FaultReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultReportPhoto
        fields = '__all__'

    def create(self, validated_data):
        fault_photo = FaultReportPhoto.objects.create(
            receivment=validated_data.get('receivment'),
            photo=validated_data.get('photo'))
        return fault_photo
