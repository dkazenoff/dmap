from django.shortcuts import render
from django.shortcuts import redirect
from sublet.models import CASUser

from sublet.forms import NewUserForm


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
	error = ""
	# Check form submission
	if request.method == "POST":
		NUForm = NewUserForm(request.POST)
		# Confirm valid data
		if NUForm.is_valid():
			# Update DB
			user = CASUser.objects.get(username=request.user)
			user.first_name = NUForm.cleaned_data['first']
			user.last_name = NUForm.cleaned_data['last']
			user.first_time = False
			user.save()
			return redirect('/sublet')
		error = "Invalid form content."
	return render(request, 'newuser.html', {"error": error})


# None View Methods (Middleware)
def processAuthUser(tree):
	username = tree[0][0].text
	try:
		user = CASUser.objects.get(username=username)
	except CASUser.DoesNotExist:
		email = username.lower() + '@rpi.edu'
		user = CASUser(username=username,email=email,first_time=True)
		user.save()

# Check if user is allowed to use service
def verifyUser(request):
	try:
		return CASUser.objects.get(username=request.user)
	except CASUser.DoesNotExist:
		return redirect('/sublet/login')