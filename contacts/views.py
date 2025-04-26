from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import  Contact
from.formz import Contactform
from django.views.decorators.http import require_http_methods #this will be foe the hx post merthod we will be using
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage
# from .utils import upload_image_to_backblaze # Import your image upload utility function
# Create your views here.

@login_required
def index(request):
    contacts = request.user.contacts.all().order_by("-created_at")#to oderr by most recent
    # if request.method == "POST":
    #     contact_id = request.POST.get("Contact-id")
    #     if contact_id:
    #         contactz = Contact.objects.filter(id = contact_id).first()
    #         if contactz and contactz.user == request.user:
    #             print(request.POST)
    #             print(contact_id)
    #             contactz.delete()
    #         else:
    #             return HttpResponse("You don't have permission to delete this post.", status=403)



    context = {"contacts":contacts,'form': Contactform }
    # we can bootup the form here as an instance
    return render(request, 'contacts.html', context)
#we wanna create a partialsnippe

# @login_required
# def search_contacts(request):
#     import time #this 4 spinners
#     time.sleep(1)
#     search_query = request.GET.get("search", "").strip()  # Get search input
#     contacts = request.user.contacts.filter(
#         Q(name__icontains=search_query) | Q(email__icontains=search_query))
#     # ) /if search_query else request.user.contacts.none()

#     return render(request, "partials/contact-list.html", {"contact": contacts})
@login_required
def search_contacts(request):
    import time  # For simulating spinners
    time.sleep(1)

    search_query = request.GET.get("search", "").strip()  # Get search input
    
    # ✅ Show all contacts if search is empty
    if search_query:
        contacts = request.user.contacts.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )
    else:
        contacts = request.user.contacts.all()  # Show all contacts when cleared

    return render(request, "partials/contact-list.html", {"contacts": contacts})



from django.db import IntegrityError
from .utils import upload_document_to_backblaze


from django.core.exceptions import ValidationError

@login_required
@require_http_methods(["POST"])
def create_contact(request):
    form = Contactform(request.POST, request.FILES)
    
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user  # Assign the user
        
        # Handle document upload if a document is provided
        if request.FILES.get('document'):
            try:
                document = request.FILES['document']
                # Upload the document to Backblaze
                backblaze_url = upload_document_to_backblaze(document)
                
                # Store the full, absolute URL to the document
                contact.document_url = backblaze_url
                
                # Log success for debugging
                print(f"Document uploaded successfully: {backblaze_url}")
                
            except ValidationError as e:
                print(f"Document validation error: {str(e)}")
                form.add_error('document', str(e))
                response = render(request, 'partials/add-contact-modal.html', {"form": form})
                response['HX-Retarget'] = "#contact_modal"
                response['HX-Reswap'] = 'outerHTML'
                response['HX-Trigger-After-Settle'] = 'fail'
                return response
            except Exception as e:
                print(f"Document upload exception: {str(e)}")
                form.add_error('document', f"Failed to upload document: {str(e)}")
                response = render(request, 'partials/add-contact-modal.html', {"form": form})
                response['HX-Retarget'] = "#contact_modal"
                response['HX-Reswap'] = 'outerHTML'
                response['HX-Trigger-After-Settle'] = 'fail'
                return response

        try:
            contact.save()  # Save inside try-except to catch duplicate errors
        except IntegrityError:
            form.add_error('email', "This email is already in your contacts.")
            response = render(request, 'partials/add-contact-modal.html', {"form": form})
            response['HX-Retarget'] = "#contact_modal"
            response['HX-Reswap'] = 'outerHTML'
            response['HX-Trigger-After-Settle'] = 'fail'
            return response

        # Successful creation response
        response = render(request, 'partials/contact-row.html', {"contact": contact})
        response['HX-Trigger'] = 'success'
        return response
    else:
        # Render form with validation errors
        response = render(request, 'partials/add-contact-modal.html', {"form": form})
        response['HX-Retarget'] = "#contact_modal"
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response


# from .utils import upload_image_to_backblaze # Import your image upload utility function
# Handle image upload if an image is provided
# if self.request.FILES.get('picture'):
#   picture = self.request.FILES['picture']
# # Upload the image to Backblaze
# backblaze_url =upload_image_to_backblaze(picture)

# if backblaze_url:
# # Update the profile picture URL
# profile.profile_picture = backblaze_url




#  acoording to the video   
# @login_required
# @require_http_methods(['DELETE'])
# def deletecontact(request, pk):
#     contact = get_object_or_404(Contact, pk =pk , user =request.user)
#     contact.delete()
#     response = HttpResponse(status =204)
#     response['Hx-Trigger'] = 'contact-deleted'
#     return response

