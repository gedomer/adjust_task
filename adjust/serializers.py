from django.utils.translation import gettext as _
from rest_framework import serializers

from .helpers import tokenize_query
from .models import Metric, PlatformType


SORT_ALLOWED_FIELDS = [field.name for field in Metric._meta.fields] + ['cpi']
COLUMN_ALLOWED_FIELDS = SORT_ALLOWED_FIELDS
GROUP_ALLOWED_FIELDS = ['date', 'channel', 'country', 'os', 'cpi']
FILTER_ALLOWED_FIELDS = ['date_from', 'date_to', 'channel', 'country', 'os']


class FilterBySerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    os = serializers.ListField(child=serializers.ChoiceField(choices=PlatformType.AS_CHOICES), required=False)
    channel = serializers.ListField(child=serializers.CharField(), required=False)
    country = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError({'detail': _('Start date can not be greater than finish date.')})
        return attrs


class QueryParamsSerializer(serializers.Serializer):
    filter_by = serializers.CharField(required=False)
    group_fields = serializers.CharField(required=False)
    sorted_by = serializers.CharField(required=False)
    columns = serializers.CharField(required=False)

    def validate_filter_by(self, filter_by):
        query, err = tokenize_query(filter_by)
        if err:
            raise serializers.ValidationError(_('Invalid query'))

        serializer = FilterBySerializer(data=query)
        if not serializer.is_valid(raise_exception=False):
            raise serializers.ValidationError(serializer.errors)
        return serializer.validated_data

    def validate_sorted_by(self, sorted_by):
        sort_key = sorted_by[1:] if sorted_by.startswith('-') else sorted_by
        if sort_key.lower() not in SORT_ALLOWED_FIELDS:
            raise serializers.ValidationError({'detail': _('Invalid sort choice.')})
        return sorted_by

    def validate_group_fields(self, group_fields):
        group_fields = group_fields.split(',')
        for field in group_fields:
            if field.lower() not in GROUP_ALLOWED_FIELDS:
                raise serializers.ValidationError({'detail': _('Invalid group choice.')})
        return group_fields

    def validate_columns(self, columns):
        columns = columns.split(',')
        for column in columns:
            if column.lower() not in COLUMN_ALLOWED_FIELDS:
                raise serializers.ValidationError({'detail': _('Invalid column choice.')})
        return columns


class MetricSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        custom_fields = kwargs.pop('custom_fields', None)
        if custom_fields:
            for field_name in set(self.fields.keys()) - set(custom_fields):
                self.fields.pop(field_name)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Metric
        fields = [
            'date',
            'channel',
            'country',
            'os',
            'impressions',
            'clicks',
            'installs',
            'spend',
            'revenue',
            'cpi',
        ]
