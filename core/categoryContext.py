from core.models import Category, Blog



def get_cats(request):
    catListMain = Category.objects.all().order_by('-id')[:4]
    mainsfooter = Blog.objects.filter(type="Main").order_by('-created_at')[:2]
    return{'catListMain':catListMain, 'mainsfooter':mainsfooter}