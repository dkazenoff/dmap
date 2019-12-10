"""Module to allow website to pull informtion to display"""
import uuid
import base64

from django.shortcuts import render
from django.shortcuts import redirect

from sublet.models import CASUser, Listing, Image
from sublet.forms import UserSettingsForm, ListingForm, ImageForm

# MAIN LANDING PAGE
def landing(request):
    """Function to display the landing page"""
    return render(request, 'index.html')

# MAIN HOME PAGE
def home(request):
    """Function to display the home page"""
    # Confirm session has user logged in
    user = verifyUser(request)
    if user.first_time:
        return redirect('/sublet/usermenu')
    return render(request, 'home.html')

def user_menu(request):
    """Function to display user menu"""
    # Confirm session has user logged in
    user_obj = verifyUser(request)
    # Create response for template
    response = {}
    response["newuser"] = user_obj.first_time
    response["form"] = UserSettingsForm(instance=user_obj, label_suffix='')
    # Check form submission
    if request.method == "POST":
        if "skip" in request.POST:
            # Skip first time user settings
            user_obj.first_time = False
            user_obj.save()
            return redirect('/sublet')
        else:
            response["form"] = UserSettingsForm(request.POST, label_suffix='')
            # Validate form data
            if response["form"].is_valid():
                # Save changes to DB
                user_obj.first_name = response["form"].cleaned_data['first_name']
                user_obj.last_name = response["form"].cleaned_data['last_name']
                user_obj.phone = response["form"].cleaned_data['phone']
                user_obj.first_time = False
                user_obj.save()
                # If first time saving, redirect to home page
                if response["newuser"]:
                    return redirect('/sublet')
                # Generate response in general use
                response["success"] = "Successfully saved changes."
    return render(request, 'newuser.html', response)

# CREATE NEW LISTING
# User will be redirected to form for editing
def create_listing(request):
    """Function to create listing then redirect to profile page"""
    # Confirm session has user logged in
    user_obj = verifyUser(request)
    list_uuid = uuid.uuid4().hex
    listing = Listing(list_id=list_uuid, owner=user_obj)
    listing.save()
    # Manage session info
    request.session["created"] = True
    return redirect("/sublet/manage/"+list_uuid)

# DELETE EXISTING LISTING
# User will be redirected to manage page
def delete_listing(request, list_id):
    """Function to delete lisitng then redirect to profile page"""
    # Delete user's listing
    Listing.objects.get(list_id=list_id).delete()
    return redirect("/sublet/manage/")

# UPDATE EXISTING LISTING
# User will be redirected to manage page
def update_listing(request, list_id):
    """Function to update a listing then redirect"""
    # Update user's listing
    form = ListingForm(request.POST, label_suffix='')
    listing = Listing.objects.get(list_id=list_id)
    # Validate form data
    if form.is_valid():
        # Move data from form to model
        listing.address = form.cleaned_data['address']
        listing.rent = form.cleaned_data['rent']
        listing.bedrooms = form.cleaned_data['bedrooms']
        listing.bathrooms = form.cleaned_data['bathrooms']
        listing.distance = form.cleaned_data['distance']
        listing.form_completion = True
    else:
        # If invalid form, then completion is false
        listing.form_completion = False
    # Manage session info
    request.session["updated"] = listing.form_completion
    # Save all changes to DB
    listing.save()
    return redirect("/sublet/manage/"+list_id)

# HANDLE SESSIONS DATA
def handle_sessions(request):
    """Handle session function"""
    response = {}
    if request.session.has_key("updated"):
        response["updated"] = request.session["updated"]
        del request.session["updated"]
    if request.session.has_key("created"):
        response["created"] = request.session["created"]
        del request.session["created"]
    return response

# IMAGE UPLOAD HANDLING
# User will be redirected to manage page
def upload_images(request, list_id):
    """Function to upload image to database"""
    #Handle Image Upload
    listing = Listing.objects.get(list_id=list_id)
    total_bytes = 0
    # Gather size of already existing images
    if listing.image_set.count() > 0:
        for entry in listing.image_set.all():
            total_bytes += entry.size
    # Process images
    for image_file in request.FILES.getlist('sublet_images'):
        # Check file size
        if image_file.size + total_bytes > 5000000:
            request.session["exceeded"] = True
            break
        # Check first time
        if total_bytes == 0:
            listing.img_completion = True
            listing.save()
        # Create Image object
        img_uuid = uuid.uuid4().hex
        image = Image.objects.create(img_id=img_uuid, listing=listing)
        # Set Data + Content
        image.name = image_file.name
        image.c_type = image_file.content_type
        image.data = base64.b64encode(image_file.read())
        image.size = image_file.size
        image.save()

    return redirect("/sublet/manage/"+list_id)

# IMAGE UPLOAD HANDLING
# User will be redirected to manage page
def delete_image(request, list_id, img_id):
    """Function to delete image from database"""
    # Gather listing data
    listing = Listing.objects.get(list_id=list_id)
    try:
        # Filtering for image linked to listing id
        Image.objects.get(img_id=img_id, listing=listing).delete()
    except Image.DoesNotExist:
        pass

    # Update boolean
    if listing.image_set.count() == 0:
        listing.img_completion = False
        listing.save()
    return redirect("/sublet/manage/"+list_id)

# MANAGE USER LISTINGS
def listing_menu(request, list_id=0):
    """Function to display user listings"""
    # Confirm session has user logged in
    user_obj = verifyUser(request)
    # Initialize response dictionary
    response = handle_sessions(request)
    # Handle session variables
    response["list_form"] = ListingForm(label_suffix='')
    response["image_form"] = ImageForm(label_suffix='')
    response["image_data"] = []
    response["list_ids"] = []
    statuses = []
    listings = user_obj.listing_set
    response["total"] = listings.count()
    # Manage listing menu
    if response["total"]:
        # Get all listing ids
        for entry in listings.all():
            response["list_ids"].append(entry.list_id)
            statuses.append(entry.form_completion and entry.img_completion)
        if list_id in response["list_ids"]:
            # Load selected listing
            primary_listing = Listing.objects.get(list_id=list_id)
            response["list_form"] = ListingForm(instance=primary_listing, label_suffix='')
            # Gather image data
            total_size = 0
            for image in primary_listing.image_set.all():
                response["image_data"].append((image.img_id, image.name))
                total_size += image.size
            total_size /= 1000000
            response["total_mb"] = round(total_size, 2)
        elif list_id == 0:
            # Set primary listing to user's first
            return redirect("/sublet/manage/"+response["list_ids"][0])
        elif list_id != 0:
            # Redirect user from accessing non-existent/another user's listing
            return redirect("/sublet/manage/")
    response["list_ids"] = list(zip(response["list_ids"], statuses))
    return render(request, 'listing.html', response)

# VIEW LISTING PAGE
def listing_info(request, sort_by="rent"):
    """Function to view listings page"""
    # Retrieve and pass listings to HTML
    reverse = ("_rev" in sort_by)
    sort_by = sort_by.replace("_rev", "")
    listings = Listing.objects.filter(form_completion=True, img_completion=True)
    return render(request, 'view.html', {'listings': listings,
                                         "sort_by": sort_by, "reverse": reverse})

def view_list(request, list_id):
    """Function to view listing, catching case where listing no longer exists"""
    try:
        listing = Listing.objects.get(list_id=list_id, form_completion=True, img_completion=True)
    except Listing.DoesNotExist:
        listing = None

    return render(request, 'sublet.html', {'listing': listing})

# CAS CALLBACK FUNCTION FOR LOG IN
def process_user(tree):
    """CAS callback function, required by CAS library for login"""
    # Parse username
    username = tree[0][0].text
    try:
        # User already exists so retrieve
        user = CASUser.objects.get(username=username)
    except CASUser.DoesNotExist:
        # Create new user
        email = username.lower() + '@rpi.edu'
        user = CASUser(username=username, email=email)
        user.save()

# Check if user is allowed to use service
def verifyUser(request):
    """CAS function to check if user is CAS authorized"""
    try:
        # Return CASUser object
        return CASUser.objects.get(username=request.user)
    except CASUser.DoesNotExist:
        # Check if user already in CAS
        if request.user is not None:
            return CASUser(username=request.user)
        # Otherwise redirect to CAS Auth
        return redirect('/sublet/login/')
