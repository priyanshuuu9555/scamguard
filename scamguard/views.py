from django.http import HttpResponse

def home(request):
    return HttpResponse("ScamGuard API is running")
