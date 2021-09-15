from django.shortcuts import render
from .forms import ImgUploadForm
from .pixel import process_image, img_to_datauri


def index(request):
    if request.method == 'POST':
        form = ImgUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_orig_b = form.cleaned_data['image'].read()
            color = form.cleaned_data['color']
            img_masked_b, counts = process_image(img_orig_b, color)
            form = ImgUploadForm()
            context = {'img_orig': img_to_datauri(img_orig_b),
                       'img_masked': img_to_datauri(img_masked_b),
                       'form': form}
            context.update(counts)
            return render(request, 'app/index.html', context)
    else:
        form = ImgUploadForm()
    return render(request, 'app/index.html', {'form': form})
