from django.test import TestCase
from django.core.urlresolvers import reverse

import json


class POIViewTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_poi = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "id": 1,
  "name": "Newport Lighthouse",
  "alt_name": "",
  "description": "A pretty nice lighthouse",
  "history": "It was built at some time in the past",
  "facts": "It's a lighthouse",
  "location": "POINT (-124.1053399999999982 43.9668739999999971)",
  "street": "123 Fake St",
  "city": "Newport",
  "state": "Oregon",
  "location_description": "out on the cape over there",
  "zip": "11234",
  "website": "",
  "email": "",
  "phone": "",
  "hazards": [1],
  "categories": [1],
  "images": [1],
  "videos": [1],
  "created": "2014-08-08 23:27:05.568395+00:00",
  "modified": "2014-08-08 23:27:05.568395+00:00"
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "POI id 999 was not found.",
    "name": "POI Not Found",
    "debug": "DoesNotExist: POI matching query does not exist.",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('poi-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/poi/1')

    def test_known_poi(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '1'}))

        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_answer = json.loads(self.expected_poi)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)

    def test_poi_not_found(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '999'}))
        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

        expected_answer = json.loads(self.expected_not_found)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)