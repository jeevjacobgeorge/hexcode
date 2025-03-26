from django.shortcuts import render
from django.db.models import Count
from .models import Asset, WaitingList, AssetCategory, Allocated
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Asset, WaitingList, Allocated, Employee, AssetCategory
from django.utils import timezone
from datetime import timedelta

def user_dashboard(request):
    # List of available assets (not allocated)
    allocated_assets = Allocated.objects.values_list('asst_id', flat=True)
    available_assets = Asset.objects.exclude(asst_id__in=allocated_assets)

    # Get all asset categories for waiting list option
    asset_categories = AssetCategory.objects.all()

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        category_id = request.POST.get('category_id')

        if not employee_id or not category_id:
            return redirect('user_dashboard')

        employee = Employee.objects.get(e_id=employee_id)
        category = AssetCategory.objects.get(category_id=category_id)

        # Find an available asset of the requested category
        available_asset = Asset.objects.filter(category=category).exclude(asst_id__in=allocated_assets).first()

        if available_asset:
            # Allocate the asset
            allocated = Allocated(
                e_id=employee,
                asst_id=available_asset,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=30)  # Default 30-day allocation
            )
            allocated.save()
        else:
            # Add to waiting list if no asset is available
            waiting = WaitingList(
                e_id=employee,
                category_id=category,
                duration=30,  # Default duration
                priority=5  # Default priority (could be user-defined)
            )
            waiting.save()

        return redirect('user_dashboard')

    context = {
        'available_assets': available_assets,
        'asset_categories': asset_categories,
        'employees': Employee.objects.all(),
    }
    return render(request, 'user_dashboard.html', context)

def admin_dashboard(request):
    # Get available assets (not allocated)
    allocated_assets = Allocated.objects.values_list('asst_id', flat=True)
    available_assets = Asset.objects.exclude(asst_id__in=allocated_assets)

    # Most frequently demanded assets
    frequently_demanded = WaitingList.objects.values('category_id__name').annotate(demand_count=Count('category_id')).order_by('-demand_count')[:5]

    # Demand alerts (high-priority waiting list items)
    demand_alerts = WaitingList.objects.filter(priority__gte=8).order_by('-priority')

    # Assets requiring maintenance or are damaged
    bad_assets = Asset.objects.filter(damaged=True) | Asset.objects.filter(maintenance_required=True)

    # Smart allocation suggestions (top-priority waiting employees)
    smart_suggestions = WaitingList.objects.order_by('-priority', 'date')[:5]

    context = {
        'available_assets': available_assets,
        'frequently_demanded': frequently_demanded,
        'demand_alerts': demand_alerts,
        'bad_assets': bad_assets,
        'smart_suggestions': smart_suggestions,
    }

    return render(request, 'admin_dashboard.html', context)
