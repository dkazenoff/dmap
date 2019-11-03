from django.shortcuts import render
from django.shortcuts import redirect
from sublet.models import CASUser, Listing

from sublet.forms import NewUserForm, ListingForm


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
			user.first_name = NUForm.cleaned_data['first_name']
			user.last_name = NUForm.cleaned_data['last_name']
			user.first_time = False
			user.save()
			return redirect('/sublet')
		error = "Invalid form content."
	return render(request, 'newuser.html', {"error": error})

def create_listing(request):
	# Format output dictionary
	output = {}
	output["form"] = ListingForm()
	output["error"] = ""
	output["success"] = ""
	# Check if current user already has a listing
	try:
		existinglist = Listing.objects.get(owner=request.user)
		output["form"] = ListingForm(instance=existinglist)
		output["created"] = True
	except Listing.DoesNotExist:
		output["created"] = False

	# Check form submission
	if request.method == "POST":
		print(request.POST)
		if "delete" in request.POST:
			Listing.objects.filter(owner=request.user).delete()
			output["form"] = ListingForm()
			output["success"] = "Successfully removed listing."
		else:
			output["form"] = ListingForm(request.POST)
			# Confirm valid data
			if output["form"].is_valid():
				listing = Listing(owner=request.user)
				listing.address = output["form"].cleaned_data['address']
				listing.rent = output["form"].cleaned_data['rent']
				listing.bedrooms = output["form"].cleaned_data['bedrooms']
				listing.bathrooms = output["form"].cleaned_data['bathrooms']
				listing.distance = output["form"].cleaned_data['distance']
				listing.save()
				# Set output messages
				output["success"] = "Successfully created listing."
				output["created"] = True
			else:
				# Set fail output messages
				output["error"] = "Make sure contents of form are valid."
	return render(request, 'create.html', output)

def view(request):
	listings = Listing.objects.all()
	return render(request, 'view.html', {'listings': listings})


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