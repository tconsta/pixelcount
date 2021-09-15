from django import forms


class ImgUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image', required=True)
    color = forms.CharField(label='Color in hex', required=False)
