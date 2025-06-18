# Created by Rejone Hossen | Premium Task Manager | 2025

def dark_mode(request):
    dark_mode = request.COOKIES.get('darkMode', 'false') == 'true'
    return {'dark_mode': dark_mode}