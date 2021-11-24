from django.db.models import Sum

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Metric
from .serializers import MetricSerializer, QueryParamsSerializer


class MetricAPIView(APIView):

    def _get_filter_kwargs(self, data):
        kwargs = {}

        if not data:
            return kwargs

        date_from = data.pop('date_from', None)
        date_to = data.pop('date_to', None)
        if date_from and date_to:
            kwargs['date__range'] = (date_from, date_to)
        elif date_from:
            kwargs['date__gt'] = date_from
        elif date_to:
            kwargs['date__lt'] = date_to

        for remained_key, value in data.items():
            kwargs[f'{remained_key}__in'] = value

        return kwargs

    def get(self, request):
        '''
        API endpoint to filter search results
        :param request: http object
        :return: json response list of dictionary (json)
        '''

        serializer = QueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = Metric.objects.all()
        data = serializer.validated_data

        serializer_fields = []
        filter_by = data.get('filter_by')
        filter_kwargs = self._get_filter_kwargs(filter_by)
        queryset = queryset.filter(**filter_kwargs)

        group_fields = data.get('group_fields')
        if group_fields:
            queryset = queryset.values(*group_fields)
            serializer_fields.extend(group_fields)

        columns = data.get('columns')
        if columns:
            serializer_fields.extend(columns)
            annotations = {}
            for field in columns:
                if field == 'cpi':
                    annotations[field] = Sum('spend') / Sum('installs')
                else:
                    annotations[field] = Sum(field)
            if annotations:
                queryset = queryset.annotate(**annotations)

        sorted_by = data.get('sorted_by')
        if sorted_by:
            queryset = queryset.order_by(sorted_by)

        serializer_fields = list(set(serializer_fields))
        serializer = MetricSerializer(queryset, many=True, custom_fields=serializer_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)
