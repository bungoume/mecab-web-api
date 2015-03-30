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


class TestHandler400(TestCase):
    def _callFUT(self, request):
        from main.views import handler400
        return handler400(request)

    def test__it(self):
        import json
        res = self._callFUT('dummy request')
        body = json.loads(res.content.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['error']['code'], 'bad_request')


class TestHandler403(TestCase):
    def _callFUT(self, request):
        from main.views import handler403
        return handler403(request)

    def test__it(self):
        import json
        res = self._callFUT('dummy request')
        body = json.loads(res.content.decode())
        self.assertEqual(res.status_code, 403)
        self.assertEqual(body['error']['code'], 'permission_denied')


class TestHandler404(TestCase):
    def _callFUT(self, request):
        from main.views import handler404
        return handler404(request)

    def test__it(self):
        import json
        res = self._callFUT('dummy request')
        body = json.loads(res.content.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error']['code'], 'not_found')


class TestHandler500(TestCase):
    def _callFUT(self, request):
        from main.views import handler500
        return handler500(request)

    def test__it(self):
        import json
        res = self._callFUT('dummy request')
        body = json.loads(res.content.decode())
        self.assertEqual(res.status_code, 500)
        self.assertEqual(body['error']['code'], 'server_error')
