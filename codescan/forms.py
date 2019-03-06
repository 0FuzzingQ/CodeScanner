from django import forms

class AddTask(forms.Form):

	taskname = forms.CharField(label = 'taskname',required=True)

	
