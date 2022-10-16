from .models import Settings


def settings(request):
    """
    This context processor is used to add the forum settings to the context. This allows the forum settings to be accessed
    in templates by using the settings variable.

    Args:
        request: The request object.

    Returns:
        dict: The forum settings.

    """
    return {'settings': Settings.load()}
