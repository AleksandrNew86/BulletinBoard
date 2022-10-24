import django_filters

from .models import Ad


class AdFilter(django_filters.FilterSet):
    ad_filter = django_filters.ModelChoiceFilter(field_name='ad',
                                                 empty_label='Любое объявление',
                                                 label='Объявление',
                                                 queryset=Ad.objects.all(),
                                                 )


    class Meta:
        model = Ad
        fields = ['ad_filter', ]


