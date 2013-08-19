import json
from django.test import TestCase
from django.core.urlresolvers import reverse

test_db = 'default'


class ViewTest(TestCase):
    """
    test if all views are working
    """
    list_views = [
        'datasets',
        'images',
        'transients',
        'extractedsources',
        'runningcatalogs',
        'monitoringlists',
    ]

    detail_views = [
        'transient',
        'dataset',
        'extractedsource',
        'runningcatalog',
        'monitoringlist',
        'image',
        'bigimage'
    ]

    def test_database_view(self):
        response = self.client.get(reverse('databases',))
        self.assertEqual(response.status_code, 200)

    def test_list_views(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}))
            self.assertEqual(response.status_code, 200)

    def test_list_csv_views(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}) +
                                       "?format=csv")
            self.assertEqual(response.status_code, 200)
            for row in response.content.split():
                columns = row.split(',')



    def test_list_json_views(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}) +
                                       "?format=json")
            self.assertEqual(response.status_code, 200)
            try:
                json.loads(response.content)
            except ValueError as e:
                self.fail("can't parse json view %s: %s" % (list_view, e))


    def test_list_views_with_dataset(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}) +
                                       "?dataset=1")
            self.assertEqual(response.status_code, 200)

    def test_detail_views(self):
        for detail_view in self.detail_views:
            response = self.client.get(reverse(detail_view,
                                               kwargs={'db': test_db,
                                                       'pk': 1}))
            self.assertEqual(response.status_code, 200)

    def test_extracted_sources_pixel(self):
         response = self.client.get(reverse('extracted_sources_pixel',
                                            kwargs={'db': test_db,
                                                    'image_id': 1}))
         self.assertEqual(response.status_code, 200)


    def test_extractedsource_plot(self):
         response = self.client.get(reverse('extractedsource_plot',
                                            kwargs={'db': test_db,
                                                    'extractedsource_id': 1}))
         self.assertEqual(response.status_code, 200)

    def test_image_plot(self):
         response = self.client.get(reverse('image_plot',
                                            kwargs={'db': test_db,
                                                    'image_id': 1}))
         self.assertEqual(response.status_code, 200)

    def test_transient_plot(self):
         response = self.client.get(reverse('transient_plot',
                                            kwargs={'db': test_db,
                                                    'transient_id': 1}))
         self.assertEqual(response.status_code, 200)

    def test_lightcurve_plot(self):
         response = self.client.get(reverse('lightcurve_plot',
                                            kwargs={'db': test_db,
                                                    'runningcatalog_id': 1}))
         self.assertEqual(response.status_code, 200)

    def test_scatter_plot(self):
         response = self.client.get(reverse('scatter_plot',
                                            kwargs={'db': test_db,
                                                    'dataset_id': 1}))
         self.assertEqual(response.status_code, 200)
