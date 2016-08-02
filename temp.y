import csv
from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from chuck.accounts.models import ManagementCompany, ListingsProviderGroup
from chuck.accounts.models import Unit

def display_bool(value):
    if value is True:
        return 'Y'
    elif value is False:
        return 'N'
    return ''

def display_none(value):
    if value is None:
        return ''
    return value


class Command(BaseCommand):
    args = "<output_file>"
    help = "Generates a csv of units for the given management company"
    option_list = BaseCommand.option_list + (
        make_option('--company', dest='company', action='store'),
        make_option('--lpg', dest='lpg', action='store'),
        make_option('--neighborhood', dest='neighborhood', action='store'),

        make_option('--available-only', dest='available_only', action='store_true'),
        make_option('--rented-last-month', dest='rented_last_month', action='store_true'),

        make_option('--req-sqft', dest='req-sqft', action='store_true'),

        make_option('--random', dest='random', action='store'),
    )

    def handle(self, *args, **options):
        output_file = args[0]

        qs = Unit.objects.full_related()
        if options['company']:
            co = ManagementCompany.objects.get(pk=options['company'])
            qs = qs.for_management_company(co)
        if options['lpg']:
            lpg = ListingsProviderGroup.objects.get(pk=options['lpg'])
            qs = qs.filter(building__management_company__in=lpg.listings_providers.all())
        if options['neighborhood']:
            qs = qs.filter(building__primary_neighborhood_id=options['neighborhood'])

        if options['req-sqft']:
            qs = qs.filter(square_footage__isnull=False)

        if options['available_only']:
            qs = qs.available()
        elif options['rented_last_month']:
            qs = qs.filter(status_updated__gte=datetime.now() - timedelta(days=30), status=Unit.UNIT_RENTED)

        qs = qs.filter(building__region_id__in=[2,3,4,5])

        if options['random']:
            qs = qs.order_by('?')[:int(options['random'])]


        writer = csv.writer(open(output_file, 'w'))
        headers = [
            'City',
            'Neighborhood',
            'Street Address',
            'Unit Number',
            'Layout',
            'Square Footage',
            'Price',
            'Date Available',
            'Amenities',
            'Source',
        ]
        writer.writerow(headers)
        for unit in qs:
            cols = [
                unit.building.city,
                unit.building.primary_neighborhood.name if unit.building.primary_neighborhood else '',
                unit.building.street_address,
                unit.unit_number,
                unit.get_layout_display(),
                unicode(display_none(unit.square_footage)),
                unicode(display_none(unit.price)),
                unit.date_available.isoformat() if unit.date_available else '',
                ', '.join(unit.amenities),
                unit.building.management_company.get_datasource_display(),
            ]
            writer.writerow([s.encode("utf-8") if s is not None else '' for s in cols])
        self.stdout.write("Created unit export\n")
