import csv

from django.core.management.base import BaseCommand

from adjust.models import Metric


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='specify an excel file path',
        )

    def read_csv(self, file_path):
        output = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                output.append(row)
        return output

    def handle(self, *args, **options):
        file_path = options.get('file')

        data = self.read_csv(file_path)
        header = data[0]
        metrics = []
        for row in data[1:]:
            metrics.append(Metric(**dict(zip(header, row))))

        Metric.objects.bulk_create(metrics, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Import completed.'))
