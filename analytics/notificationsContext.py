from analytics.models import TaskNotifications, AdminNotifications, Task



def get_notis(request):
    if request.user.is_authenticated:
        userNots = TaskNotifications.objects.filter(user=request.user, read=False)
        userinfos = TaskNotifications.objects.filter(user=request.user).order_by('-created_at')[:5]
        adminNots = AdminNotifications.objects.filter(read=False)
        admininfos = AdminNotifications.objects.order_by('-created_at')[:5]
    else:
        userNots = None
        userinfos = None
        adminNots = None
        admininfos = None

    if request.user.is_authenticated and request.user.is_staff:
        comp = Task.objects.filter(complete=True).count()
        prog = Task.objects.filter(complete=False).count()
        excel = Task.objects.filter(type='Excel').count()
        spss = Task.objects.filter(type='SPSS').count()
        python = Task.objects.filter(type='Python').count()
        ml = Task.objects.filter(type='Machine Learning').count()
        r = Task.objects.filter(type='R').count()
        mat = Task.objects.filter(type='Matlab').count()
        tab = Task.objects.filter(type='Tableau').count()
    elif request.user.is_authenticated:
        comp = Task.objects.filter(user=request.user, complete=True).count()
        prog = Task.objects.filter(user=request.user, complete=False).count()
        excel = Task.objects.filter(user=request.user, type='Excel').count()
        spss = Task.objects.filter(user=request.user, type='SPSS').count()
        python = Task.objects.filter(user=request.user, type='Python').count()
        ml = Task.objects.filter(user=request.user, type='Machine Learning').count()
        r = Task.objects.filter(user=request.user, type='R').count()
        mat = Task.objects.filter(user=request.user, type='Matlab').count()
        tab = Task.objects.filter(user=request.user, type='Tableau').count()
    else:
        comp = None
        prog = None
        excel = None
        spss = None
        python = None
        ml = None
        r = None
        mat = None
        tab = None
    return{'userNots':userNots, 
           'adminNots':adminNots, 
           'admininfos':admininfos, 
           'userinfos':userinfos,
           'r':r,
            'excel':excel,
            'python':python,
            'ml':ml,
            'spss':spss,
            'mat':mat,
            'tab':tab,
            'comp':comp,
            'prog':prog,
           }


