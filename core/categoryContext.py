from core.models import Category


def get_cats(request):
    catListMain = Category.objects.all().order_by('-id')[:3]
    return{'catListMain':catListMain}