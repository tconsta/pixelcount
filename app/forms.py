from django import forms
from django.core.exceptions import ValidationError

RGB_LENGTH = 7  # ex '#AABBFF'


class ImgUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image', required=True)
    color = forms.CharField(label='Color in hex',
                            required=False, max_length=RGB_LENGTH,
                            widget=forms.TextInput(attrs={'placeholder': 'ex: F2E5A0 or #F2E5A0'}))
    precision = forms.IntegerField(label='Precision:',
                                   widget=forms.NumberInput(attrs={'type': 'range',
                                                                   'step': '1',
                                                                   'min': '0',
                                                                   'max': '100'}))

    def clean_color(self):
        hexcolor = self.cleaned_data['color'].strip()
        if hexcolor == '':
            return None

        if len(hexcolor) == RGB_LENGTH and not hexcolor.startswith('#'):
            raise ValidationError("Please enter color in the correct format or leave it blank")
        else:
            hexcolor = hexcolor.lstrip('#')
        try:
            int(hexcolor, 16)
        except ValueError:
            raise ValidationError("Please enter color in the correct format or leave it blank")
        return hexcolor
