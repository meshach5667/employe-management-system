from django.db import models





class Department(models.Model):
    name = models.CharField(max_length=100,null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
   

class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)  
    dept = models.CharField(max_length=100)  
    role = models.CharField(max_length=100)  
    hire_date = models.DateTimeField()

    def __str__(self):
        return "%s %s %s" %(self.first_name, self.last_name, self.phone)