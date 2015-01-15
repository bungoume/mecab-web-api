from django.http import JsonResponse

from main import mecab_utils


def reading(request):
    sentence = request.GET.get('sentence', '')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.reading_sentence(sentence),
    }

    return JsonResponse(ret)


def parse(request):
    sentence = request.GET.get('sentence', '')

    ret = {
        'input_sentence': sentence,
        'items': mecab_utils.parse_sentence(sentence),
    }

    return JsonResponse(ret)
