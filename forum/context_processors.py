from .models import Settings


def settings(request):
    return {'settings': Settings.load()}
