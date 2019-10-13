from django.shortcuts import render
from django.shortcuts import redirect
from sublet.models import CASUser


# MAIN LANDING PAGE
def landing(request):
	return render(request, 'index.html')

# MAIN USER/LISTINGS HOME PAGE
def home(request):
	user = verifyUser(request)
	if user.first_time:
		return redirect('/sublet/newuser')
	return render(request, 'home.html')

# MAIN USER/LISTINGS HOME PAGE
def newuser(request):
	user = verifyUser(request)
	return render(request, 'newuser.html')


# None View Methods (Middleware)
def processAuthUser(tree):
	username = tree[0][0].text
	try:
		user = CASUser.objects.get(username=username)
	except CASUser.DoesNotExist:
		email = username.lower() + '@rpi.edu'
		user = CASUser(username=username,email=email)
		user.save()

# Check if user is allowed to use service
def verifyUser(request):
	try:
		return CASUser.objects.get(username=request.user)
	except CASUser.DoesNotExist:
		return redirect('/sublet/login')