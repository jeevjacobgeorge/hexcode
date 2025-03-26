from django.shortcuts import render
from django.db.models import Count
from .models import Asset, WaitingList, AssetCategory, Allocated
from django.shortcuts import render, redirect
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Asset, Allocated, WaitingList, AssetCategory, Employee
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


# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('user_login')

# User Dashboard - Select Available Assets
@login_required
def user_dashboard(request):
    employee = Employee.objects.get(user=request.user)

    # Get assets that are not allocated
    allocated_assets = Allocated.objects.values_list('asst_id', flat=True)
    available_assets = Asset.objects.exclude(asst_id__in=allocated_assets)

    if request.method == "POST":
        category_id = request.POST.get('category_id')

        # Find the first available asset of that category
        asset = available_assets.filter(category_id=category_id).first()

        if asset:
            # Allocate the asset
            Allocated.objects.create(
                e_id=employee,
                asst_id=asset,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30)  # Assume 30-day allocation
            )
            message = f"Asset {asset.asst_id} allocated successfully!"
        else:
            # Add to waiting list
            WaitingList.objects.create(
                e_id=employee,
                category_id=AssetCategory.objects.get(pk=category_id),
                duration=30,
                priority=5  # Default priority
            )
            message = "No available asset, added to waiting list."

        return render(request, 'user_dashboard.html', {'available_assets': available_assets, 'message': message})

    return render(request, 'user_dashboard.html', {'available_assets': available_assets})
