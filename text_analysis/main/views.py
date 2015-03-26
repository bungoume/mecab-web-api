from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from main import mecab_utils
from main.forms import ReadingForm, ParseForm


@require_http_methods(["GET", "POST"])
def reading(request):
    form = ReadingForm(request.REQUEST)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.reading_sentence(sentence),
    }

    return JsonResponse(ret)


@require_http_methods(["GET", "POST"])
def parse(request):
    form = ParseForm(request.REQUEST)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.parse_sentence(sentence),
    }

    return JsonResponse(ret)
