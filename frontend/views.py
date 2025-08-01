from django.shortcuts import render, redirect
from analytics.models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.
# def frontEnd(request):
#     if request.user.is_authenticated and request.user.is_staff:
#             return redirect('task-listview-admin')
#     elif request.user.is_authenticated:
#         return redirect('task-listview')
#     else:
#         return render(request, 'frontend/index.html')

def frontEnd(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return redirect('task-listview-admin')
        return redirect('task-listview')
    return render(request, 'frontend/index.html')


def frontEnd2(request):
    return render(request, 'frontend/index.html')



def privacyPolicy(request):
    return render(request, 'frontend/privacy-policy.html')


def termsOfService(request):
    return render(request, 'frontend/tos.html')


@login_required
def profile2(request):
    user = request.user
    email = user.email
    user_since = user.date_joined
    name = user.first_name
    comp = Task.objects.filter(user=request.user, complete=True).count()
    return render(request, 'frontend/profile.html', {'email':email, 'user_since':user_since, 'name':name, 'comp': comp })
