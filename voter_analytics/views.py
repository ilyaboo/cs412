from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from django.utils.dateparse import parse_date

class VotersListView(ListView):
    ''' view to display voters data '''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 50
    
    def get_queryset(self):
    
        # start with entire queryset
        qs = super().get_queryset().order_by('first_name')

        # filter by party affiliation
        party = self.request.GET.get('party_affiliation_search')
        if party:
            qs = qs.filter(party_affiliation=party)

        # filter by minimum year of birth
        min_yob = self.request.GET.get('min_yob')
        print(min_yob)
        if min_yob:
            qs = qs.filter(date_of_birth__year__gte=int(min_yob))

        # filter by maximum year of birth
        max_yob = self.request.GET.get('max_yob')
        if max_yob:
            qs = qs.filter(date_of_birth__year__lte=int(max_yob))

        # filter results by voter_score field
        vs = self.request.GET.get('voter_score_search')
        if vs != None:
            if vs != "":
                vs = int(vs)
                qs = qs.filter(voter_score = vs)

        # filtering by elections participated in
        if self.request.GET.get('2020_state', None) == "on":
            qs = qs.filter(v20state = True)

        if self.request.GET.get('2021_town', None) == "on":
            qs = qs.filter(v21town = True)

        if self.request.GET.get('2021_primary', None) == "on":
            qs = qs.filter(v21primary = True)

        if self.request.GET.get('2022_general', None) == "on":
            qs = qs.filter(v22general = True)

        if self.request.GET.get('2023_town', None) == "on":
            qs = qs.filter(v23town = True)

        return qs
    
    def get_context_data(self, **kwargs):
        # overriden to include unique values for party affiliations

        context = super().get_context_data(**kwargs)

        unique_parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['unique_parties'] = unique_parties
        context['years'] = range(1900, 2025)

        # Preserve filter parameters for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_params'] = query_params.urlencode()

        return context
    
class VoterDetailView(DetailView):
    ''' view to display a voter '''

    template_name = 'voter_analytics/voter_profile.html'
    model = Voter
    context_object_name = 'voter'