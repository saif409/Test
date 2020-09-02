from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Surveyor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='surveyer')
    address = models.CharField(max_length=200)
    profile_picture = models.ImageField(null=True,blank=True)
    country = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    email=models.CharField(max_length=100,null=True, blank=True)
    area = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

    def name(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name) if self.user else ""


class Country(models.Model):
    country_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.country_name


class Division(models.Model):
    division_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.division_name


class District(models.Model):
    district_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.district_name


class SubDistrict(models.Model):
    subdistrct_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.subdistrct_name


class Area(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    subdistrict = models.ForeignKey(SubDistrict, on_delete=models.SET_NULL, null=True, blank=True)
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return "{0},{1},{2},{3},{4}".format(self.area_name, self.subdistrict, self.district, self.division, self.country)

    @property
    def address_format(self):
        return "{0},{1},{2},{3},{4}".format(self.area_name, self.subdistrict, self.district, self.division,
                                            self.country)









