from mainapp.utils import menu


def get_mainapp_context(request):
    return {'menu': menu}

