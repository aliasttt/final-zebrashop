from.models import *
from django import forms
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأیید رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = RegisterModel
        fields = ['name', 'lastname', 'password1', 'password2', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تأیید آن مطابقت ندارند.")

        return cleaned_data


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductsModel
        fields = ['name', 'descriptions', 'image']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = ['name', 'lastname', 'phone', 'address']  # فیلدهای مورد نیاز
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),  # غیرقابل ویرایش
            'lastname': forms.TextInput(attrs={'readonly': 'readonly'}),  # غیرقابل ویرایش
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),  # غیرقابل ویرایش
            'address': forms.TextInput(attrs={'placeholder': 'آدرس خود را وارد کنید.'}), 
             } # قابل ویرایش 
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # برچسب‌ها را خالی می‌کند 


class AddressSelectionForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = ['name', 'lastname', 'phone', 'address', 'city']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True  # آدرس اختیاری است
        self.fields['city'].required = True  # شهر الزامی است
        self.fields['name'].disabled = True  # نام غیرقابل ویرایش
        self.fields['lastname'].disabled = True  # نام خانوادگی غیرقابل ویرایش
        self.fields['phone'].disabled = True  # شماره تلفن غیرقابل ویرایش



CITY_CHOICES = [
    ('tehran', 'تهران'),
    ('tabriz', 'تبریز'),
    ('isfahan', 'اصفهان'),
    ('shiraz', 'شیراز'),
    ('mashhad', 'مشهد'),
    ('ahvaz', 'اهواز'),
    ('karaj', 'کرج'),
    ('kermanshah', 'کرمانشاه'),
    ('hamedan', 'همدان'),
    ('zahedan', 'زاهدان'),
    ('yazd', 'یزد'),
    ('rasht', 'رشت'),
    ('ardabil', 'اردبیل'),
    ('kerman', 'کرمان'),
    ('gorgan', 'گرگان'),
    ('borujerd', 'بروجرد'),
    ('qazvin', 'قزوین'),
    ('zanjan', 'زنجان'),
    ('savojbolagh', 'ساوجبلاغ'),
    ('sanandaj', 'سنندج'),
    ('sari', 'ساری'),
    ('jajrom', 'جاجرم'),
    ('babol', 'بابلسر'),
    ('noshahr', 'نوشهر'),
    ('gilan', 'گیلان'),
    ('kashan', 'کاشان'),
    ('kavar', 'کاوار'),
    ('khorasan', 'خراسان'),
    ('fars', 'فارس'),
    ('bushehr', 'بوشهر'),
    ('qom', 'قم'),
    ('kordestan', 'کردستان'),
    ('ilam', 'ایلام'),
    ('chaharmahal', 'چهارمحال'),
    ('markazi', 'مرکزی'),
    ('alborz', 'البرز'),
    ('north_khorasan', 'خراسان شمالی'),
    ('south_khorasan', 'خراسان جنوبی'),
    ('golestan', 'گلستان'),
    ('semnan', 'سمنان'),
]

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = ['name', 'lastname', 'phone', 'address', 'city']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderReviewForm, self).__init__(*args, **kwargs)
        
        if user:
            self.instance = user
            self.fields['address'].required = True
            self.fields['city'].required = True
            self.fields['name'].disabled = True
            self.fields['lastname'].disabled = True
            self.fields['phone'].disabled = True

        self.fields['address'].widget.attrs.update({'placeholder': 'آدرس خود را وارد کنید.'})
        self.fields['city'].widget = forms.Select(choices=CITY_CHOICES)