from django.shortcuts import render, redirect
from django.db.models import Sum, Max
from django.http import JsonResponse
from django.utils import timezone
from .models import Lga, Ward, PollingUnit, AnnouncedPuResults, Party

def polling_unit_result(request):
    polling_units = PollingUnit.objects.filter(lga_id__gt=0).order_by('polling_unit_name')
    
    selected_pu_id = request.GET.get('pu_id')
    results = []
    selected_pu = None
    
    if selected_pu_id and selected_pu_id.isdigit():
        selected_pu = PollingUnit.objects.filter(uniqueid=int(selected_pu_id)).first()
        if selected_pu:
            results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=str(selected_pu.uniqueid))
        
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
    
    if selected_lga_id and selected_lga_id.isdigit():
        selected_lga = Lga.objects.filter(lga_id=int(selected_lga_id)).first()
        
        pu_uniqueids = list(
            PollingUnit.objects.filter(lga_id=int(selected_lga_id))
            .values_list('uniqueid', flat=True)
        )
        
        str_pu_ids = [str(uid) for uid in pu_uniqueids if uid is not None]
        
        party_totals = (
            AnnouncedPuResults.objects.filter(
                polling_unit_uniqueid__in=str_pu_ids
            )
            .values('party_abbreviation')
            .annotate(total_score=Sum('party_score'))
            .order_by('party_abbreviation')
        )
        
        grand_total = sum(item['total_score'] for item in party_totals if item['total_score'])

    context = {
        'lgas': lgas,
        'selected_lga': selected_lga,
        'party_totals': party_totals,
        'grand_total': grand_total,
    }
    return render(request, 'lga_summed_result.html', context)


def get_wards(request, lga_id):
    wards = list(Ward.objects.filter(lga_id=lga_id).values('ward_id', 'ward_name'))
    return JsonResponse(wards, safe=False)


def add_polling_unit(request):
    if request.method == 'POST':
        lga_id = request.POST.get('lga_id')
        ward_id = request.POST.get('ward_id')
        pu_name = request.POST.get('polling_unit_name')
        pu_number = request.POST.get('polling_unit_number')
        entered_by = request.POST.get('entered_by', 'Admin')
        
        max_pu = PollingUnit.objects.aggregate(Max('uniqueid'))['uniqueid__max'] or 0
        next_uniqueid = max_pu + 1
        
        new_pu = PollingUnit.objects.create(
            uniqueid=next_uniqueid,
            polling_unit_name=pu_name,
            polling_unit_number=pu_number,
            lga_id=int(lga_id),
            ward_id=int(ward_id),
            polling_unit_id=0,
            entered_by_user=entered_by,
            date_entered=timezone.now(),
            user_ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1')
        )
        
        parties = Party.objects.all()
        for party in parties:
            score = request.POST.get(f'party_{party.partyid}', 0)
            if score:
                party_abbr = str(party.partyid).strip()[:4]
                
                AnnouncedPuResults.objects.create(
                    polling_unit_uniqueid=str(new_pu.uniqueid),
                    party_abbreviation=party_abbr,
                    party_score=int(score),
                    entered_by_user=entered_by,
                    date_entered=timezone.now(),
                    user_ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1')
                )
                
        return redirect('polling_unit_result')

    lgas = Lga.objects.filter(state_id=25).order_by('lga_name')
    parties = Party.objects.all()
    
    return render(request, 'add_polling_unit.html', {
        'lgas': lgas,
        'parties': parties
    })