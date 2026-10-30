from django.shortcuts import render
from .models import PollingUnit, AnnouncedPuResults

def polling_unit_result(request):
    # Fetch polling units for dropdown
    polling_units = PollingUnit.objects.filter(lga_id__gt=0).order_by('polling_unit_name')
    
    selected_pu_id = request.GET.get('pu_id')
    results = []
    selected_pu = None
    
    if selected_pu_id:
        selected_pu = PollingUnit.objects.filter(uniqueid=selected_pu_id).first()
        results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=selected_pu_id)
        
    context = {
        'polling_units': polling_units,
        'selected_pu': selected_pu,
        'results': results,
    }
    return render(request, 'polling_unit_result.html', context)