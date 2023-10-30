from .models import Category


def categories(request):
    """
    Retrieves all the categories from the database that have no parent category.

    Args:
        request: The HTTP request object.

    Returns:
        A dictionary containing the retrieved categories with the key 'categories'.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}