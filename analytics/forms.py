from django import forms
from django.core.exceptions import ValidationError
from .models import Task, TaskData, TaskFiles, Message

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'type', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TaskDataForm(forms.ModelForm):
    class Meta:
        model = TaskData
        fields = ['description',]


class TaskDataFormAdmin(forms.ModelForm):
    class Meta:
        model = TaskData
        fields = ['description', 'is_answer', 'is_status', 'progress']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        max_file_size = 20 * 1024 * 1024  # 20MB in bytes

        if isinstance(data, (list, tuple)):
            cleaned_files = []
            for file in data:
                if file.size > max_file_size:
                    raise ValidationError(f"{file.name} exceeds the 20MB size limit.")
                cleaned_files.append(single_file_clean(file, initial))
            return cleaned_files
        else:
            if data.size > max_file_size:
                raise ValidationError(f"{data.name} exceeds the 20MB size limit.")
            return single_file_clean(data, initial)



# class MultipleFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("widget", MultipleFileInput())
#         super().__init__(*args, **kwargs)

#     def clean(self, data, initial=None):
#         single_file_clean = super().clean
#         if isinstance(data, (list, tuple)):
#             result = [single_file_clean(d, initial) for d in data]
#         else:
#             result = single_file_clean(data, initial)
#         return result

class TaskFilesForm(forms.ModelForm):
    files = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = TaskFiles
        exclude = ['file', 'taskdata']
        #fields = ['file', ]




# class TaskFilesForm(forms.Form):
#     # files = forms.FileField(
#     #     widget=forms.FileInput(attrs={'multiple': True}),  # Use FileInput instead of ClearableFileInput
#     #     required=False  # or True if you want to enforce at least one file
#     # )
#     files = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
#         required=False
#     )

#     def clean_files(self):
#         # Get each file from request.FILES directly
#         files = self.files.getlist('files') if self.files else []
        
#         for f in files:
#             if f.size > 5 * 1024 * 1024:
#                 raise forms.ValidationError(f"File {f.name} exceeds 5MB limit.")
        
#         return files[0] if files else None 
    


#     # def clean_files(self):
#     #     files = self.files.getlist('files')

#     #     for f in files:
#     #         if f.size > 5 * 1024 * 1024:
#     #             raise forms.ValidationError(f"File {f.name} exceeds 5MB limit.")

#     #     return files






# class MultiFileInput(forms.ClearableFileInput):
#     def __init__(self, attrs=None):
#         attrs = attrs or {}
#         attrs['multiple'] = True
#         super().__init__(attrs)

#     def value_from_datadict(self, data, files, name):
#         if hasattr(files, 'getlist'):
#             return files.getlist(name)
#         return None

# class MultiFileField(forms.FileField):
#     widget = MultiFileInput
#     default_error_messages = {
#         'invalid_file': 'Upload a valid file. The file you uploaded was either not a file or a corrupted file.'
#     }

#     def clean(self, data, initial=None):
#         if data and isinstance(data, (list, tuple)):
#             result = []
#             for item in data:
#                 super().clean(item, initial)
#                 result.append(item)
#             return result
#         return super().clean(data, initial)

# class TaskFilesForm(forms.Form):
#     files = MultiFileField(required=False)

#     def clean_files(self):
#         files = self.cleaned_data.get('files', [])
#         for f in files:
#             if f.size > 5 * 1024 * 1024:
#                 raise forms.ValidationError(f"File {f.name} exceeds 5MB limit.")
#         return files


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']