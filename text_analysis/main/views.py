from django.http import HttpResponse, JsonResponse

from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods

from main import mecab_utils
from main.forms import ReadingForm, ParseForm


@cache_control(max_age=86400)
@require_http_methods(["GET", "POST", "OPTIONS"])
def reading(request):
    if request.method == "GET":
        form = ReadingForm(request.GET)
    elif request.method == "POST":
        form = ReadingForm(request.POST)
    elif request.method == "OPTIONS":
        return HttpResponse({}, status=204)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')
    nbest_num = form.cleaned_data.get('nbest_num')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.reading_sentence(sentence, nbest_num),
    }

    return JsonResponse(ret)


@cache_control(max_age=86400)
@require_http_methods(["GET", "POST", "OPTIONS"])
def parse(request):
    if request.method == "GET":
        form = ParseForm(request.GET)
    elif request.method == "POST":
        form = ParseForm(request.POST)
    elif request.method == "OPTIONS":
        return HttpResponse("", status=204)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')
    nbest_num = form.cleaned_data.get('nbest_num')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.parse_sentence(sentence, nbest_num),
    }

    return JsonResponse(ret)


def handler400(request):
    res = JsonResponse({'error': {'code': 'bad_request',
                                  'message': "400 Bad Request"}}, status=400)
    return res


def handler403(request):
    res = JsonResponse({'error': {'code': 'permission_denied',
                                  'message': "403 Permission Denied"}}, status=403)
    return res


def handler404(request):
    res = JsonResponse({'error': {'code': 'not_found',
                                  'message': "404 Not Found"}}, status=404)
    return res


def handler500(request):
    res = JsonResponse({'error': {'code': 'server_error',
                                  'message': "500 Internal Server Error"}}, status=500)
    return res
