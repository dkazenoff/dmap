from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User


# Create your views here.
def home(request):
	return render(request, 'index.html')


def processAuthUser(tree):
	username = tree[0][0].text
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		email = username.lower() + '@rpi.edu'
		user = User(username=username,email=email)
		user.save()

def verifyUser(request):
	try:
		user = User.objects.get(username=request.user)
	except User.DoesNotExist:
		return redirect('/sublet/login')
	# Add logic to check if user is allowed here
	return render(request, 'home.html')