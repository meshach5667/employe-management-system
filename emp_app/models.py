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

class User(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)
    
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
    

class LeaveApplication(models.Model):
        employee = models.ForeignKey(User, on_delete=models.CASCADE)
        start_date = models.DateField()
        end_date = models.DateField()
        reason = models.TextField()

   

        def __str__(self):
            return f"{self.employee.username} - {self.start_date} to {self.end_date}"