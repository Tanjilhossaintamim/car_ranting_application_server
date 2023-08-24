from django_filters import FilterSet

from store.models import Car


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            "catagory": ['exact'],
            "price": ['gt', 'lt']
        }
