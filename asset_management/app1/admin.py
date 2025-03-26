from django.contrib import admin
from .models import Employee, AssetCategory, Asset, Allocated, WaitingList

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('e_id', 'name', 'designation')
    search_fields = ('name', 'designation')

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'specs')
    search_fields = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asst_id', 'category', 'age', 'damaged', 'maintenance_required')
    list_filter = ('category', 'damaged', 'maintenance_required')
    search_fields = ('category__name',)

@admin.register(Allocated)
class AllocatedAdmin(admin.ModelAdmin):
    list_display = ('e_id', 'asst_id', 'start_date', 'end_date', 'delivered', 'valid')
    list_filter = ('delivered', 'valid')
    

@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ('e_id', 'category_id', 'duration', 'priority')
    list_filter = ('priority',)
    search_fields = ('e_id__name', 'category_id__name')
