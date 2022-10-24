from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Ad, Response
from .forms import AdForm
from .filters import AdFilter

class AdList(ListView):
    model = Ad
    ordering = '-date_creation'
    template_name = 'Ads/list_ads.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(DetailView):
    model = Ad
    template_name = 'Ads/ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_ad = context['object']
        responses = Response.objects.filter(ad=object_ad)
        context['responses'] = responses
        return context

    def post(self, request, *args, **kwargs):
        if 'add_ad' in request.POST:
            text = request.POST['response']
            ad_resp = Ad.objects.get(id=request.POST['ad_resp'])

            Response.objects.create(user=request.user, ad=ad_resp, text_response=text)
        url = request.META.get('HTTP_REFERER')
        return redirect(url)


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'Ads/ad_create.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        return super().form_valid(form)


class AdEdit(LoginRequiredMixin, UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'Ads/ad_edit.html'
    permission_required = 'Ads.change_ad'


class ResponseSearch(ListView):
    model = Response
    ordering = '-date_creation'
    template_name = 'Ads/responses_to_authors1.html'
    context_object_name = 'responses'
    paginate_by = 10


    def get_queryset(self):
        self.queryset = Response.objects.filter(ad__author=self.request.user)
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required()
def responses_to_author(request):

    responses = Response.objects.filter(ad__author=request.user).order_by('-date_creation')
    author_ads = Ad.objects.filter(author=request.user)
    ads_filter = None

    if request.POST.get('ads', None) and not request.POST.get('ads', None) == 'Все объявление':
        ads_filter = Ad.objects.filter(title_ad=request.POST['ads']).first()
        responses = Response.objects.filter(ad=ads_filter)

    if request.POST.get('accept_response', None):
        response = Response.objects.get(id=request.POST.get('response', None))
        response.accepted = True
        response.save()
        ads_filter = response.ad
        responses = Response.objects.filter(ad=ads_filter)

    if request.POST.get('delete_response', None):
        response = Response.objects.get(id=request.POST.get('response', None))
        response.delete()
        ads_filter = response.ad
        responses = Response.objects.filter(ad=ads_filter)

    context = {
        'responses': responses,
        'author_ads': author_ads,
        'ads_filter': ads_filter,
    }
    return render(request, 'Ads/responses_to_autors.html', context)
