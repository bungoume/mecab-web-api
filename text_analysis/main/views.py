from django.http import JsonResponse


def parse(request):
    text = request.GET.get('text', '')

    ret = {
        'text': text,
    }

    return JsonResponse(ret)
