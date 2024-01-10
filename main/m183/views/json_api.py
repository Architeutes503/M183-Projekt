from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Post
import logging
logger = logging.getLogger(__name__)

API_KEY = '1234567890'

@csrf_exempt
def api_view(request):
    if request.method == 'GET':
        api_key = request.GET.get('api_key')
        if api_key == API_KEY:
            posts = Post.objects.filter(status='published').values()
            logger.info("API request: %s" % posts)
            return JsonResponse({'posts': list(posts)})
        else:
            logger.warning("Invalid API Key: %s" % api_key)
            return JsonResponse({'error': 'Invalid API Key'}, status=403)
    else:
        logger.warning("Invalid request method: %s" % request.method)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

