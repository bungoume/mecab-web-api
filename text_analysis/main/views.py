from django.http import JsonResponse

from main import mecab_utils
from main.forms import ReadingForm, ParseForm


def reading(request):
    form = ReadingForm(request.GET)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.reading_sentence(sentence),
    }

    return JsonResponse(ret)


def parse(request):
    form = ParseForm(request.GET)
    if not form.is_valid():
        return JsonResponse(
            {"error": {"code": "form_invalid", "errors": form.errors}}, status=400)

    sentence = form.cleaned_data.get('sentence')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.parse_sentence(sentence),
    }

    return JsonResponse(ret)
