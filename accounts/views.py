from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import UserProfileForm, UploadFileForm, LanguageSelectionForm
from .models import Profile, File
from .services import convert_pdf_to_audio

import os
import PyPDF2
from gtts import gTTS


# All views here!
def index(request):
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
	profile = Profile.objects.filter(user=request.user)
	return render(request, 'dashboard.html')


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.profile)
        print(f'deets: {form}')
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})



@login_required(login_url='login')
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('convert', file_id=file.id)
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


@login_required(login_url='login')
def convert_file_views(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    print(f'File => {file}')
    if request.method == 'POST':
        form = LanguageSelectionForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            print(f'chosen lang: {language}')
            audio_file_path = convert_pdf_to_audio(file.pdf_file.path, language)
            file.audio_file.save(audio_file_path, file.pdf_file.name)
            file.save()

            #audio_file_path = convert_pdf_to_audio(file.pdf_file.path, language)
            #file.audio_file.save(audio_file_path, file.pdf_file.name, content_type='audio/mpeg', file_name='audio_file.mp3')
            #file.audio_file.name = audio_file_path
            print(f'audio file => {audio_file_path}')
            #audio_file_path = convert_pdf_to_audio(file.pdf_file.path, language)
            #file.audio_file = audio_file_path

            file.save()
            return redirect('save', file_id=file.id)
    else:
        form = LanguageSelectionForm()
    return render(request, 'convert_file.html', {'form': form})


@login_required(login_url='login')
def convert_file_view(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)

    if request.method == 'POST':
        form = LanguageSelectionForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            
            try:
                audio_file_path = convert_pdf_to_audio(file.pdf_file.path, language)
                print(f'audio file path => {audio_file_path}')

                # Update the audio_file field with the generated audio file
                file.audio_file.name = audio_file_path

                # Save the file
                file.save()

                return redirect('save', file_id=file.id)
            except ValidationError as e:
                form.add_error(None, str(e))
                print(f'error => {e}')
    else:
        form = LanguageSelectionForm()

    return render(request, 'convert_file.html', {'form': form})



@login_required(login_url='login')
def save_file_view(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    # Your code to handle saving the file
    return render(request, 'save_file.html', {'file': file})


def file_list_view(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})
