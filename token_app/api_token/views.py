import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@csrf_exempt
def receive_victim_request(request, uuid):
    try:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        payload = {
            'uuid': str(uuid),
            'ip_address': ip_address,
            'user_agent': user_agent,
        }
        print(payload)
        response = requests.post('http://127.0.0.1:3009/tools/canary_token/test/', data=payload)

        return redirect('/404.html')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)