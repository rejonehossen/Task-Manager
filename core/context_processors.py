# Created by Rejone Hossen | Premium Task Manager | 2025
from .models import SharedList
def dark_mode(request):
    dark_mode = request.COOKIES.get('darkMode', 'false') == 'true'
    return {'dark_mode': dark_mode}


def shared_list(request):
    my_list = shared_list.objects.all()
    return (
        {
            'shared_list':my_list,
        }
    )