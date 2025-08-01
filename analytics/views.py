from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from analytics.forms import TaskForm, TaskDataForm, TaskFilesForm, TaskDataFormAdmin, MessageForm
from analytics.models import Task, TaskData, TaskFiles, AdminNotifications, TaskNotifications, Message, MessageNotifications, AdminMessageNotifications
from custom_user.models import User
from django.http import JsonResponse, HttpResponseForbidden,  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from functools import wraps
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.utils.timezone import localtime
import random
from django.db.models import Q

# Create your views here.

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Staff only")
    return _wrapped_view


def homePage(request):
    return render(request, 'analytics/homepage.html')



def TaskCreate(request):
    return render(request, 'analytics/TaskCreate.html')

@login_required
def create_task(request):
    if request.method == 'POST':
        order_form = TaskForm(request.POST)
        data_form = TaskDataForm(request.POST)
        files_form = TaskFilesForm(request.POST, request.FILES)
         # get list of uploaded files

        if order_form.is_valid():
            task = order_form.save(commit=False)
            task.user = request.user
            task.save()
        if data_form.is_valid() and files_form.is_valid():
            taskdata = data_form.save(commit=False)
            taskdata.task = task
            taskdata.save()

            files = request.FILES.getlist('files') 
            for f in files:
                TaskFiles.objects.create(taskdata=taskdata, file=f)

            #return redirect('order_success') 
            return redirect('task-info', task.id, task.slug) 
    else:
        order_form = TaskForm()
        data_form = TaskDataForm()
        files_form = TaskFilesForm()

    return render(request, 'analytics/TaskCreate.html', {
        'order_form': order_form,
        'data_form': data_form,
        'files_form': files_form
    })


@login_required
def task_detail(request, id, slug):
     task = Task.objects.get(id=id, slug=slug)
     if not task.paid:
         return redirect('task-checkout', task.id) 
     else:
        if request.method == 'POST':
            data_form = TaskDataForm(request.POST)
            files_form = TaskFilesForm(request.POST, request.FILES)
            if data_form.is_valid() and files_form.is_valid():
                taskdata = data_form.save(commit=False)
                taskdata.task = task
                taskdata.save()

                files = request.FILES.getlist('files') 
                for f in files:
                    TaskFiles.objects.create(taskdata=taskdata, file=f)
                return redirect('task-info', task.id, task.slug)     
        else:
            TaskData.objects.filter(task=task, is_mod=True, read=False).update(read=True)
            data_form = TaskDataForm()
            files_form = TaskFilesForm()
            taskdatas = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
            taskdata_qs = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
            taskdata_with_files = [
            {
                'taskdata': td,
                'files': TaskFiles.objects.filter(taskdata=td)  # or td.taskfiles_set.all()
            }
            for td in taskdata_qs
        ]
            context = {
            'task': task,
            'data_form': data_form,
            'files_form': files_form,
            'taskdata_with_files': taskdata_with_files,
            'taskdatas': taskdatas
        }
        return render(request, 'analytics/task-detail.html', context)
     
     


@login_required
def task_update(request, id, slug):
     task = Task.objects.get(id=id, slug=slug)
     if request.method == 'POST':
        order_form = TaskForm(request.POST, instance=task)
        if order_form.is_valid():
             #obj = form.save(commit=False)
             order_form.save()
             return redirect('task-detail', task.id, task.slug) 
     else:
        order_form = order_form(instance=task)
     return render(request, 'analytics/TaskCreate.html',  {'order_form': order_form})



@login_required
def task_listView(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    tasks = Task.objects.filter((Q(complete=False) | (Q(complete=True) & Q(completion_date__gte=seven_days_ago)))).order_by('-created_at')
    paginator = Paginator(tasks, 20)  # Show 10 tasks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    dontShowPaginator = paginator.num_pages <= 1
    # comp = Task.objects.filter(user=request.user, complete=True).count()
    # prog = Task.objects.filter(user=request.user, complete=False).count()
    # excel = Task.objects.filter(user=request.user, type='Excel').count()
    # spss = Task.objects.filter(user=request.user, type='SPSS').count()
    # python = Task.objects.filter(user=request.user, type='Python').count()
    # ml = Task.objects.filter(user=request.user, type='Machine Learning').count()
    # r = Task.objects.filter(user=request.user, type='R').count()
    # mat = Task.objects.filter(user=request.user, type='Matlab').count()
    # tab = Task.objects.filter(user=request.user, type='Tableau').count()
    return render(request, 'analytics/TaskList2.html',  {'tasks': tasks, 
                                                        # 'comp':comp,
                                                        # 'r':r,
                                                        # 'excel':excel,
                                                        # 'python':python,
                                                        # 'ml':ml,
                                                        # 'spss':spss,
                                                        # 'mat':mat,
                                                        # 'tab':tab,
                                                        'page_obj': page_obj,
                                                        # 'prog':prog,
                                                        'dontShowPaginator':dontShowPaginator
                                                        })
 


@login_required
def task_checkout(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'analytics/TaskCheckout.html',  {'task': task})




@csrf_exempt
def payCallBack(request, id):
    task = get_object_or_404(Task, id=id)
    
    # You might want to validate the request data here before trusting it
    task.paid = True
    task.save()
    
    return redirect('task-detail', task.id, task.slug) 





@staff_required
def task_listViewAdmin(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    tasks = Task.objects.filter((Q(complete=False) | (Q(complete=True) & Q(completion_date__gte=seven_days_ago)))).order_by('-created_at')
    paginator = Paginator(tasks, 20)  # Show 10 tasks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    dontShowPaginator = paginator.num_pages <= 1
    # completes = Task.objects.filter(complete=True, completion_date__gte=one_week_ago)
    # comp = Task.objects.filter(complete=True).count()
    # prog = Task.objects.filter(complete=False).count()
    # excel = Task.objects.filter(type='Excel').count()
    # spss = Task.objects.filter(type='SPSS').count()
    # python = Task.objects.filter(type='Python').count()
    # ml = Task.objects.filter(type='Machine Learning').count()
    # r = Task.objects.filter(type='R').count()
    # mat = Task.objects.filter(type='Matlab').count()
    # tab = Task.objects.filter(type='Tableau').count()
    return render(request, 'analytics/TaskList.html',  {'tasks': tasks, 
                                                        # 'completes':completes,
                                                        # 'r':r,
                                                        # 'excel':excel,
                                                        # 'python':python,
                                                        # 'ml':ml,
                                                        # 'spss':spss,
                                                        # 'mat':mat,
                                                        # 'tab':tab,
                                                        'page_obj': page_obj,
                                                        # 'comp':comp,
                                                        # 'prog':prog,
                                                        'dontShowPaginator':dontShowPaginator
                                                        })



def BaseTest(request):
    return render(request, 'analytics/emails/welcome.html')




@staff_required
def task_detailAdmin(request, id, slug):
     task = Task.objects.get(id=id, slug=slug)
     if request.method == 'POST':
        data_form = TaskDataFormAdmin(request.POST)
        files_form = TaskFilesForm(request.POST, request.FILES)
        if data_form.is_valid() and files_form.is_valid():
            taskdata = data_form.save(commit=False)
            taskdata.task = task
            taskdata.is_mod = True
            if taskdata.is_answer:
                task.completion_date = timezone.now()
                task.complete = True
            taskdata.save()

            files = request.FILES.getlist('files') 
            for f in files:
                TaskFiles.objects.create(taskdata=taskdata, file=f)

            return redirect('task-info-admin', task.id, task.slug)     
     else:
        TaskData.objects.filter(task=task, is_mod=False, adminRead=False).update(adminRead=True)
        data_form = TaskDataFormAdmin()
        files_form = TaskFilesForm()
        taskdatas = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
        taskdata_qs = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
        taskdata_with_files = [
        {
            'taskdata': td,
            'files': TaskFiles.objects.filter(taskdata=td)  # or td.taskfiles_set.all()
        }
        for td in taskdata_qs
    ]
        context = {
        'task': task,
        'data_form': data_form,
        'files_form': files_form,
        'taskdata_with_files': taskdata_with_files,
        'taskdatas': taskdatas
     }
     return render(request, 'analytics/task-detail-admin.html', context)




@staff_required
def task_detailAdminHT(request, id, slug):
     task = Task.objects.get(id=id, slug=slug)
     if request.method == 'POST':
        data_form = TaskDataFormAdmin(request.POST)
        files_form = TaskFilesForm(request.POST, request.FILES)
        if data_form.is_valid() and files_form.is_valid():
            taskdata = data_form.save(commit=False)
            taskdata.task = task
            taskdata.is_mod = True
            taskdata.save()

            files = request.FILES.getlist('files') 
            for f in files:
                TaskFiles.objects.create(taskdata=taskdata, file=f)
            if request.headers.get('HX-Request'):
                return render(request, 'partials/single_message.html', {'taskdata': taskdata})
                #return redirect('task-info-admin', task.id, task.slug)     
     else:
        TaskData.objects.filter(task=task, adminRead=False).update(adminRead=True)
        data_form = TaskDataFormAdmin()
        files_form = TaskFilesForm()
        taskdatas = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
        taskdata_qs = TaskData.objects.filter(task=task).prefetch_related('taskfiles_set')
        taskdata_with_files = [
        {
            'taskdata': td,
            'files': TaskFiles.objects.filter(taskdata=td)  # or td.taskfiles_set.all()
        }
        for td in taskdata_qs
    ]
        context = {
        'task': task,
        'data_form': data_form,
        'files_form': files_form,
        'taskdata_with_files': taskdata_with_files,
        'taskdatas': taskdatas
     }
     return render(request, 'analytics/task-detail-admin.html', context)







@login_required
def subjectCategories(request, type):
    tasks = Task.objects.filter(user=request.user, type=type).order_by('-created_at')
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dontShowPaginator = paginator.num_pages <= 1
    taskCat = type
    # comp = Task.objects.filter(user=request.user, complete=True).count()
    # prog = Task.objects.filter(user=request.user, complete=False).count()
    # excel = Task.objects.filter(user=request.user, type='Excel').count()
    # spss = Task.objects.filter(user=request.user, type='SPSS').count()
    # python = Task.objects.filter(user=request.user, type='Python').count()
    # ml = Task.objects.filter(user=request.user, type='Machine Learning').count()
    # r = Task.objects.filter(user=request.user, type='R').count()
    # mat = Task.objects.filter(user=request.user, type='Matlab').count()
    # tab = Task.objects.filter(user=request.user, type='Tableau').count()
    return render(request, 'analytics/subject-tasks.html',  {'tasks': tasks, 
                                                        # 'r':r,
                                                        # 'excel':excel,
                                                        # 'python':python,
                                                        # 'ml':ml,
                                                        # 'spss':spss,
                                                        # 'mat':mat,
                                                        # 'tab':tab,
                                                        'taskCat':taskCat,
                                                        'page_obj': page_obj,
                                                        # 'comp':comp,
                                                        # 'prog':prog,
                                                        'dontShowPaginator':dontShowPaginator
                                                        })
    

@login_required
def subjectCategoriesAdmin(request, type):
    tasks = Task.objects.filter(type=type).order_by('-created_at')
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dontShowPaginator = paginator.num_pages <= 1 
    taskCat = type
    # comp = Task.objects.filter(complete=True).count()
    # prog = Task.objects.filter(complete=False).count()
    # excel = Task.objects.filter(type='Excel').count()
    # spss = Task.objects.filter(type='SPSS').count()
    # python = Task.objects.filter(type='Python').count()
    # ml = Task.objects.filter(type='Machine Learning').count()
    # r = Task.objects.filter(type='R').count()
    # mat = Task.objects.filter(type='Matlab').count()
    # tab = Task.objects.filter(type='Tableau').count()
    return render(request, 'analytics/subject-tasks-admin.html',  {'tasks': tasks, 
                                                        # 'r':r,
                                                        # 'excel':excel,
                                                        # 'python':python,
                                                        # 'ml':ml,
                                                        # 'spss':spss,
                                                        # 'mat':mat,
                                                        # 'tab':tab,
                                                        'taskCat':taskCat,
                                                        'page_obj': page_obj,
                                                        # 'comp':comp,
                                                        # 'prog':prog,
                                                        'dontShowPaginator':dontShowPaginator
                                                        })


@login_required
def completeOrNot(request, status):
    status_bool = status.lower() == 'true'
    if request.user.is_staff:
        tasks = Task.objects.filter(complete=status_bool).order_by('-created_at')
        # comp = Task.objects.filter(complete=True).count()
        # prog = Task.objects.filter(complete=False).count()
        # excel = Task.objects.filter(type='Excel').count()
        # spss = Task.objects.filter(type='SPSS').count()
        # python = Task.objects.filter(type='Python').count()
        # ml = Task.objects.filter(type='Machine Learning').count()
        # r = Task.objects.filter(type='R').count()
        # mat = Task.objects.filter(type='Matlab').count()
        # tab = Task.objects.filter(type='Tableau').count()
    else:
        tasks = Task.objects.filter(user=request.user, complete=status_bool).order_by('-created_at')
        # comp = Task.objects.filter(user=request.user, complete=True).count()
        # prog = Task.objects.filter(user=request.user, complete=False).count()
        # excel = Task.objects.filter(user=request.user, type='Excel').count()
        # spss = Task.objects.filter(user=request.user, type='SPSS').count()
        # python = Task.objects.filter(user=request.user, type='Python').count()
        # ml = Task.objects.filter(user=request.user, type='Machine Learning').count()
        # r = Task.objects.filter(user=request.user, type='R').count()
        # mat = Task.objects.filter(user=request.user, type='Matlab').count()
        # tab = Task.objects.filter(user=request.user, type='Tableau').count()

    paginator = Paginator(tasks, 30)  # Show 10 tasks per page
    if status == 'true':
        tag = 'Complete'
    else:
        tag = 'In Progress'

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dontShowPaginator = paginator.num_pages <= 1 
    
    return render(request, 'analytics/completeOrNot.html',  {'tasks': tasks, 
                                                        # 'r':r,
                                                        # 'excel':excel,
                                                        # 'python':python,
                                                        # 'ml':ml,
                                                        # 'spss':spss,
                                                        # 'mat':mat,
                                                        # 'tab':tab,
                                                        'page_obj': page_obj,
                                                        # 'comp':comp,
                                                        # 'prog':prog,
                                                        'dontShowPaginator':dontShowPaginator,
                                                        'tag':tag
                                                        })




@login_required
def fetch_notifications(request):
    userNots = TaskNotifications.objects.filter(user=request.user, read=False)
    userinfos = TaskNotifications.objects.select_related('task').filter(user=request.user).order_by('-created_at')[:5]

    notifications_data = {
        "unread_count": userNots.count(),
        "notifications": [
            {
                "message": obj.message,
                "title":obj.task.title if obj.task else None,
                "task_id": obj.task.id if obj.task else None,
                "task_slug": obj.task.slug if obj.task else None,
                "task_img": static(obj.task.image_path) if obj.task and obj.task.image_path else None,
                "created_at": localtime(obj.created_at).isoformat() 
            }
            for obj in userinfos
        ]
    }
    return JsonResponse(notifications_data)


@require_POST
@login_required
def mark_notifications_read(request):
    TaskNotifications.objects.filter(user=request.user, read=False).update(read=True)
    return JsonResponse({"status": "ok"})


@login_required
def admin_fetch_notifications(request):
    userNots = AdminNotifications.objects.filter(read=False)
    userinfos = AdminNotifications.objects.select_related('task').order_by('-created_at')[:5]

    notifications_data = {
        "unread_count": userNots.count(),
        "notifications": [
            {
                "message": obj.message,
                "title":obj.task.title if obj.task else None,
                "task_id": obj.task.id if obj.task else None,
                "task_slug": obj.task.slug if obj.task else None,
                "task_img": static(obj.task.image_path) if obj.task and obj.task.image_path else None,
                "created_at": localtime(obj.created_at).isoformat() 
            }
            for obj in userinfos
        ]
    }
    return JsonResponse(notifications_data)


@require_POST
@login_required
def admin_mark_notifications_read(request):
    AdminNotifications.objects.filter(read=False).update(read=True)
    return JsonResponse({"status": "ok"})



@login_required
def getMessage(request, m_user):
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = User.objects.get(id=m_user)
            message.isAdmin = True
            message.save()
            return redirect('admin-user-messages', m_user)
    else:
        Message.objects.filter(user=m_user, isAdmin=False, read=False).update(read=True)
        queryset = Message.objects.filter(user=m_user).order_by('-created_at')[:7]
        umessages = list(queryset)
        umessages.reverse()
        message_form = MessageForm()
        return render(request, 'analytics/adminmessage.html', {'umessages':umessages, 'message_form':message_form})
        
@login_required
def newMessage(request):
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('user-messages')
    else:
        Message.objects.filter(user=request.user, isAdmin=True, read=False).update(read=True)
        queryset = Message.objects.filter(user=request.user).order_by('-created_at')[:5]
        umessages = list(queryset)
        umessages.reverse()
        message_form = MessageForm()
        return render(request, 'analytics/usermessages.html', {'umessages':umessages, 'message_form':message_form})
    
@login_required
def listMessages(request):
    umessages = Message.objects.order_by('-created_at')[:50]
    return render(request, 'analytics/messagelist.html', {'umessages':umessages})



def howItWorks(request):
    return render(request, 'analytics/howItWorks.html')
        



@login_required
def admin_fetch_messages(request):
    userNots = AdminMessageNotifications.objects.filter(read=False)
    userinfos = AdminMessageNotifications.objects.order_by('-created_at')[:5]
    
    notifications_data = {
        "unread_count": userNots.count(),
        "notifications": [
            {
                "message": obj.message,
                "user":obj.user.id if obj.user else None,
                "created_at": localtime(obj.created_at).isoformat() 
            }
            for obj in userinfos
        ]
    }
    return JsonResponse(notifications_data)


@require_POST
@login_required
def admin_mark_messages_read(request):
    AdminMessageNotifications.objects.filter(read=False).update(read=True)
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def mark_messages_read(request):
    MessageNotifications.objects.filter(user=request.user, read=False).update(read=True)
    return JsonResponse({"status": "ok"})


@login_required
def user_fetch_messages(request):
    userNots = MessageNotifications.objects.filter(user=request.user, read=False)
    userinfos = MessageNotifications.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    notifications_data = {
        "unread_count": userNots.count(),
        "notifications": [
            {
                "message": obj.message,
                "user":obj.user if obj.user else None,
                "created_at": localtime(obj.created_at).isoformat() 
            }
            for obj in userinfos
        ]
    }
    return JsonResponse(notifications_data)



@require_POST
def status_update(request, id):
    task = Task.objects.get(id=id)
    progress = request.POST.get('progress')
    if progress:
        message_choices = [
             'Thanks for choosing Northstar! Your task is now with an expert. Need to add more details or files? Just reply here - we will ensure your spreadsheets work perfectly!',
            'message two',
             'message three',
             'message four'
         ]
        description = random.choice(message_choices)
        TaskData.objects.create(task=task, description=description, progress=int(progress), is_status=True)
        return redirect('task-info-admin', task.id, task.slug)    
    return HttpResponse('No progress provided', status=400)
