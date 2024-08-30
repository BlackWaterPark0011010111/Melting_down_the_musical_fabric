from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from .forms import UploadForm, UserRegisterForm
from .models import ConversionHistory
from .utils import convert_pdf_to_tabs

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'profile': request.user})

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            uploaded_file_url = fs.url(filename)
            tabs = convert_pdf_to_tabs(uploaded_file_url)
            history = ConversionHistory.objects.create(
                user=request.user,
                pdf_file=filename,
                converted_tabs=tabs
            )
            return render(request, 'muss/tabs.html', {'tabs': tabs})
    else:
        form = UploadForm()
    return render(request, 'muss/upload.html', {'form': form})

@login_required
def history(request):
    histories = ConversionHistory.objects.filter(user=request.user).order_by('-date_uploaded')
    return render(request, 'muss/history.html', {'histories': histories})

@login_required
def history_detail(request, history_id):
    history = ConversionHistory.objects.get(id=history_id, user=request.user)
    return render(request, 'muss/history_detail.html', {'history': history})
