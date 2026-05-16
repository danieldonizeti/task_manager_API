from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Bem-vindo á Task Manager API',
        'status': 'Servidor rodando',
        'endpoints': {
            'users': reverse('user-list', request=request),
            'tasks': reverse('tasks-list', request=request),
        }
    })

from django.http import JsonResponse

def container_check(request):
    try:
        with open("/proc/1/cgroup", "rt") as fh:
            content = fh.read()
            is_container = any(s in content for s in ["docker", "kubepods", "containerd"])
    except Exception:
        is_container = False

    return JsonResponse({"in_container": is_container})