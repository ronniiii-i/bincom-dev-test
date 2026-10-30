from django.shortcuts import render
from django.db.models import Sum
from .models import Lga, PollingUnit, AnnouncedPuResults

def polling_unit_result(request):
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


def lga_summed_result(request):
    lgas = Lga.objects.filter(state_id=25).order_by('lga_name')
    selected_lga_id = request.GET.get('lga_id')
    
    party_totals = []
    selected_lga = None
    grand_total = 0
    
    if selected_lga_id:
        selected_lga = Lga.objects.filter(lga_id=selected_lga_id).first()
        
        pu_uniqueids = PollingUnit.objects.filter(
            lga_id=selected_lga_id
        ).values_list('uniqueid', flat=True)
        
        party_totals = AnnouncedPuResults.objects.filter(
            polling_unit_uniqueid__in=[str(uid) for uid in pu_uniqueids]
        ).values('party_abbreviation').annotate(
            total_score=Sum('party_score')
        ).order_by('party_abbreviation')
        
        grand_total = sum(item['total_score'] for item in party_totals if item['total_score'])

    context = {
        'lgas': lgas,
        'selected_lga': selected_lga,
        'party_totals': party_totals,
        'grand_total': grand_total,
    }
    return render(request, 'lga_summed_result.html', context)