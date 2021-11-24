from django.test import TestCase
from django.urls import reverse
from adjust.factories import MetricFactory
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import tokenize_query
from .serializers import FilterBySerializer


class ValidationTestCase(TestCase):

    def test_valid_tokenize_query(self):
        self.assertIsNone(tokenize_query('country:CA')[1])
        self.assertIsNone(tokenize_query('os:ios;country:US;date_from:2017-01-02')[1])
        self.assertIsNone(tokenize_query('os:android')[1])

        self.assertEqual(tokenize_query('date_from:2017-01-02')[0]['date_from'], '2017-01-02')
        self.assertEqual(tokenize_query('os:android')[0]['os'], ['android'])

    def test_invalid_tokenize_query(self):
        self.assertIsNotNone(tokenize_query('country:CA;')[1])
        self.assertIsNotNone(tokenize_query('os=ios,')[1])
        self.assertIsNotNone(tokenize_query('')[1])
        self.assertIsNotNone(tokenize_query(';;')[1])
        self.assertIsNotNone(tokenize_query(',')[1])
        self.assertIsNotNone(tokenize_query(None)[1])


class FilterBySerializerTests(TestCase):

    def test_date_from_is_greater_than_date_to(self):
        data = {
            'date_from': '2017-01-06',
            'date_to': '2017-01-05'
        }
        serializer = FilterBySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_operating_system_choices(self):
        data = {
            'os': ['omerOS']
        }
        serializer = FilterBySerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data['os'] = ['android']
        serializer = FilterBySerializer(data=data)
        self.assertTrue(serializer.is_valid())


class MetricApiTestCase(APITestCase):

    def setUp(self):
        self.path = reverse('core:metrics-api')

    def test_order_by(self):
        MetricFactory.create_batch(size=3)

        response = self.client.get(self.path + '?sorted_by=date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dates = [r['date'] for r in response.data]
        self.assertEqual(dates, sorted(dates))

        response = self.client.get(self.path + '?sorted_by=-date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dates = [r['date'] for r in response.data]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_filter_by(self):
        MetricFactory.create_batch(os='android', size=3)
        MetricFactory.create_batch(os='ios', size=7)

        response = self.client.get(self.path + '?filter_by=os:android')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(self.path + '?filter_by=os:ios')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
