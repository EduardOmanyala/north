from django.db.models import Q
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
import requests





# Create your views here.
def dashMain(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    tasks = Task.objects.filter((Q(complete=False) | (Q(complete=True) & Q(completion_date__gte=seven_days_ago))), user=request.user).order_by('-created_at')
    return render(request, 'dash/dash.html', {'tasks':tasks})

def dashBase(request):
    return render(request, 'dash/base.html')



@login_required
def task_detail(request, id, slug):
     task = Task.objects.get(id=id, slug=slug)
     if not task.paid:
         pass
         #return redirect('task-checkout', task.id) 
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
                return redirect('taskDetail', task.id, task.slug)     
        else:
            TaskData.objects.filter(task=task, read=False).update(read=True)
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
        return render(request, 'dash/task-detail.html', context)
     


# Replace these with your actual keys
CONSUMER_KEY = 'qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW'
#T7WTrodyFfIH9AmBH4vCxUlgf0YuFXWL
CONSUMER_SECRET = 'osGQ364R49cXKeOYSpaOnT++rHs='

# Set to either 'sandbox' or 'live'
APP_ENVIRONMENT = 'sandbox'
IPN_CALLBACK_URL = 'https://https://the-northstar.com/payrequests'
CALLBACK_URL = 'https://12eb-41-81-142-80.ngrok-free.app/pesapal/response-page.php'

@csrf_exempt
def get_pesapal_token(request):
    if APP_ENVIRONMENT == 'sandbox':
        api_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    elif APP_ENVIRONMENT == 'live':
        api_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"
    else:
        return JsonResponse({"error": "Invalid APP_ENVIRONMENT"}, status=400)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {
        "consumer_key": CONSUMER_KEY,
        "consumer_secret": CONSUMER_SECRET,
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        token = response_data.get("token")
        return JsonResponse({"token": token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_auth_token():
    if APP_ENVIRONMENT == 'sandbox':
        token_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    elif APP_ENVIRONMENT == 'live':
        token_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"
    else:
        raise Exception("Invalid APP_ENVIRONMENT")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "consumer_key": CONSUMER_KEY,
        "consumer_secret": CONSUMER_SECRET,
    }

    response = requests.post(token_url, json=payload, headers=headers)
    response.raise_for_status()
    token = response.json().get("token")
    return token
    


@csrf_exempt
def register_ipn(request):
    try:
        token = get_auth_token()

        if APP_ENVIRONMENT == 'sandbox':
            ipn_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
        elif APP_ENVIRONMENT == 'live':
            ipn_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"
        else:
            return JsonResponse({"error": "Invalid APP_ENVIRONMENT"}, status=400)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "url": IPN_CALLBACK_URL,
            "ipn_notification_type": "POST",
        }

        response = requests.post(ipn_url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return JsonResponse({"ipn_id": data.get("ipn_id")})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
def initiate_payment(request):
    try:
        token = get_auth_token()

        if APP_ENVIRONMENT == 'sandbox':
            submit_url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"
        elif APP_ENVIRONMENT == 'live':
            submit_url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"
        else:
            return JsonResponse({"error": "Invalid APP_ENVIRONMENT"}, status=400)

        merchant_reference = str(random.randint(1, 1000000000000000000))

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "id": merchant_reference,
            "currency": "KES",
            "amount": 10.00,
            "description": "Payment description goes here",
            "callback_url": CALLBACK_URL,
            "notification_id": IPN_ID,
            "branch": "UMESKIA SOFTWARES",
            "billing_address": {
                "email_address": "alvo967@gmail.com",
                "phone_number": "0768168060",
                "country_code": "KE",
                "first_name": "Alvin",
                "middle_name": "Odari",
                "last_name": "Kiveu",
                "line_1": "Pesapal Limited",
                "line_2": "",
                "city": "",
                "state": "",
                "postal_code": "",
                "zip_code": ""
            }
        }

        # response = requests.post(submit_url, json=payload, headers=headers)
        # response.raise_for_status()
        # return JsonResponse(response.json(), status=response.status_code)
    
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()

        redirect_url = response.json().get("redirect_url")
        return redirect(redirect_url)  # ✅ Redirect directly

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




     
     
