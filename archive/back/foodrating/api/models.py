from django.db import models


class Site(models.Model):
    comp_id = models.ForeignKey("Company", on_delete=models.CASCADE)
    state = models.CharField(max_length=20)
    street = models.CharField(max_length=30, null=True)
    addr_num = models.SmallIntegerField(null=True)
    zip_code = models.SmallIntegerField()


class Company(models.Model):
    name = models.CharField(max_length=20, unique=True)
    comp_type = models.SmallIntegerField(null=True)


class Rating(models.Model):
    food_id = models.ForeignKey("Food", on_delete=models.CASCADE)
    site_id = models.ForeignKey("Site", on_delete=models.SET_NULL)
    cust_id = models.ForeignKey("Customer", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    rating = models.SmallIntegerField()
    date = models.DateField()


class Customer(models.Model):
    email = models.CharField(max_length=40, unique=True)
    pwd = models.CharField(max_length=40)
    frst_name = models.CharField(max_length=20)
    midd_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20)


class Food(models.Model):
    comp_id = models.ForeignKey("Company", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    cuisine = models.SmallIntegerField(null=True)
