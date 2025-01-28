from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
def upload_resume(request):
    if request.method == 'POST' and request.FILES['file']:
       uploaded_file = request.FILES['file']
       fs = FileSystemStorage()
       filename = fs.save(uploaded_file.name, uploaded_file)
       return HttpResponse("File uploaded successfully")
    
    return HttpResponse("Something went wrong")