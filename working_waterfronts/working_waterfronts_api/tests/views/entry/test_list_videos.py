from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import Video
from django.contrib.auth.models import User


class ListVideoTestCase(TestCase):
    fixtures = ['thirtythree']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_url_endpoint(self):
        url = reverse('entry-list-videos')
        self.assertEqual(url, '/entry/videos')

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('entry-list-videos'))
        self.assertRedirects(response, '/login?next=/entry/videos')

    def test_list_items(self):
        """
        Tests to see if the list of videos contains the proper
        videos and proper video data
        """

        page_1 = self.client.get(reverse('entry-list-videos')).context
        page_2 = self.client.get(
            '{}?page=2'.format(reverse('entry-list-videos'))).context
        page_3 = self.client.get(
            '{}?page=3'.format(reverse('entry-list-videos'))).context
        page_4 = self.client.get(
            '{}?page=4'.format(reverse('entry-list-videos'))).context
        page_nan = self.client.get(
            '{}?page=NaN'.format(reverse('entry-list-videos'))).context

        self.assertEqual(
            list(page_1['item_list']),
            list(Video.objects.order_by('name')[:15]))

        self.assertEqual(
            list(page_2['item_list']),
            list(Video.objects.order_by('name')[15:30]))

        self.assertEqual(
            list(page_3['item_list']),
            list(Video.objects.order_by('name')[30:33]))

        # Page 4 should be identical to Page 3, as these fixtures
        # have enough content for three pages (15 items per page, 33 items)

        self.assertEqual(
            list(page_3['item_list']),
            list(page_4['item_list']))

        # Page NaN should be identical to Page 1, as Django paginator returns
        # the first page if the page is not an int

        self.assertEqual(
            list(page_1['item_list']),
            list(page_nan['item_list']))
