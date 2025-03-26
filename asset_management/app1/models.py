from django.db import models

class Employee(models.Model):
    e_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AssetCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specs = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Asset(models.Model):
    asst_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    age = models.IntegerField()
    damaged = models.BooleanField(default=False)
    maintenance_required = models.BooleanField(default=False)

    def __str__(self):
        return f"Asset {self.asst_id} ({self.category.name})"

class Allocated(models.Model):
    e_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    asst_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    delivered = models.BooleanField(default=True)
    feedback = models.TextField(blank=True, null=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.e_id.name} -> {self.asst_id.category.name}"
    
class WaitingList(models.Model):
    e_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    category_id = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in days")
    priority = models.IntegerField(help_text="Higher number means higher priority")

    def __str__(self):
        return f"{self.e_id.name} waiting for {self.category_id.name}"

