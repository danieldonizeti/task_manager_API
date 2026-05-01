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