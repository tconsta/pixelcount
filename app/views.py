from django.shortcuts import render
from .forms import ImgUploadForm


def index(request):
    form = ImgUploadForm()
    context = {'form': form}
    return render(request, 'app/index.html', context)
