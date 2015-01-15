import json
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestReadingApi(TestCase):
    def _getTargetURL(self, *args, **kwargs):
        return reverse('reading', args=args, kwargs=kwargs)

    def test_it(self):
        res = self.client.get(self._getTargetURL(), {'sentence': '今日は良い天気ですね。'})
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.content.decode())
        self.assertEqual(res_data['items'][0]['reading'], 'キョウハヨイテンキデスネ。')


class TestParseApi(TestCase):
    def _getTargetURL(self, *args, **kwargs):
        return reverse('parse', args=args, kwargs=kwargs)

    def test_it(self):
        res = self.client.get(self._getTargetURL(), {'sentence': '今日は良い天気ですね。'})
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.content.decode())
        self.assertEqual(res_data['items'][0]['all']['reading'], 'キョウハヨイテンキデスネ。')
