from django.shortcuts import render
from django.shortcuts import redirect

from sublet.models import CASUser, Listing
from sublet.forms import NewUserForm, ListingForm

# MAIN LANDING PAGE
def landing(request):
	return render(request, 'index.html')

# MAIN HOME PAGE
def home(request):
	# Confirm session has user logged in
	user = verifyUser(request)
	if user.first_time:
		return redirect('/sublet/newuser')
	return render(request, 'home.html')

# NEW USER PAGE
def newuser(request):
	# Confirm session has user logged in
	user = verifyUser(request)
	error = ""
	# Check form submission
	if request.method == "POST":
		NUForm = NewUserForm(request.POST)
		# Validate form data
		if NUForm.is_valid():
			# Update DB + redirect to main home
			user = CASUser.objects.get(username=request.user)
			user.first_name = NUForm.cleaned_data['first_name']
			user.last_name = NUForm.cleaned_data['last_name']
			user.first_time = False
			user.save()
			return redirect('/sublet')
		# Generate error message
		error = "Invalid form content."
	return render(request, 'newuser.html', {"error": error})

# CREATE LISTING PAGE
def create_listing(request):
	# Create response dictionary
	response = {}
	response["form"] = ListingForm()
	response["error"] = ""
	response["success"] = ""
	# Check if user already has listing
	try:
		# Retrieve existing listing
		existinglist = Listing.objects.get(owner=request.user)
		response["form"] = ListingForm(instance=existinglist)
		response["created"] = True
	except Listing.DoesNotExist:
		response["created"] = False

	# Check form submission
	if request.method == "POST":
		if "delete" in request.POST:
			# Delete user's listing
			Listing.objects.filter(owner=request.user).delete()
			response["form"] = ListingForm()
			response["success"] = "Successfully removed listing."
		else:
			# Otherwise create/update listing
			response["form"] = ListingForm(request.POST)
			# Validate form data
			if response["form"].is_valid():
				# Save to DB + generate success message
				listing = Listing(owner=request.user)
				listing.address = response["form"].cleaned_data['address']
				listing.rent = response["form"].cleaned_data['rent']
				listing.bedrooms = response["form"].cleaned_data['bedrooms']
				listing.bathrooms = response["form"].cleaned_data['bathrooms']
				listing.distance = response["form"].cleaned_data['distance']
				listing.save()
				# Set response messages
				response["success"] = "Successfully created listing."
				response["created"] = True
			else:
				# Set fail response message
				response["error"] = "Make sure contents of form are valid."
	return render(request, 'create.html', response)

# VIEW LISTING PAGE
def view(request):
	# Retrieve and pass listings to HTML
	listings = Listing.objects.all()
	return render(request, 'view.html', {'listings': listings})


# CAS CALLBACK FUNCTION FOR LOG IN
def processAuthUser(tree):
	# Parse username
	username = tree[0][0].text
	try:
		# User already exists so retrieve
		user = CASUser.objects.get(username=username)
	except CASUser.DoesNotExist:
		# Create new user
		email = username.lower() + '@rpi.edu'
		user = CASUser(username=username,email=email,first_time=True)
		user.save()

# Check if user is allowed to use service
def verifyUser(request):
	try:
		# Return CASUser object
		return CASUser.objects.get(username=request.user)
	except CASUser.DoesNotExist:
		# Redirect to log in page
		return redirect('/sublet/login')