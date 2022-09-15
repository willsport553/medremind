from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import *

# Create your views here.

def welcome(request):
    return render(request, 'core/welcome.html') 


def login_user(request):
    """Log the user in.
    """
    return render(request, 'core/login.html')


def logout_user(request):
    """Log out the currently logged in user.
    """
    if (request.user.is_authenticated):
        logout(request)
    return redirect(reverse('welcome'))


@login_required
def setup(request):
    """Show the user the pharmacist/patient
    prompt to guide them to setup."""
    return render(request, 'core/setup.html')


@login_required
def redirect_user(request):
    """Redirect the user to the appropriate page
    depending on their role & setup status.
    If pharmacist, redirect to pharmacist home.
    If patient, redirect to patient home.
    If neither flag is set, start user setup because
    this means they have not completed onboarding yet.
    """
    user = request.user
    if (user.is_pharmacist):
        return redirect(reverse('pharmacist:home'))
    elif (user.is_patient):
        return redirect(reverse('patient:home'))
    else:
        return redirect(reverse('setup'))

# Pharmacist Setup


@login_required
def pharmacist_setup(request):
    """Set up a new pharmacist user.
    """
    if request.method == "POST":
        form = PharmacistSetupForm(request.POST)
        if form.is_valid():
            # This license key & class name is valid!
            # Create the class, assign the pharmacist to it,
            # set the is_pharmacist flag, and redirect to pharmacist home.

            # STEP 1: Create new class
            new_class = Class(
                name=form.cleaned_data['class_name'],
                license=License.objects.get(
                    pk=form.cleaned_data['license_key']),
                join_code=Class.generate_join_code()
            )
            new_class.save()

            # STEP 2: Assign pharmacist to class
            request.user.class_id = new_class

            # STEP 3: Set is_pharmacist flag
            request.user.is_pharmacist = True

            # STEP 4: Save it all & redirect to pharmacist home
            request.user.save()
            return redirect(reverse('redirect_user'))

    else:
        form = PharmacistSetupForm()

    return render(request, 'core/pharmacist_setup.html', {'form': form})

# Patient Setup


@login_required
def patient_setup(request):
    """Set up a new patient user.
    """
    if request.method == "POST":
        form = PatientSetupForm(request.POST)
        if form.is_valid():
            # This join code (and the class associated with it) is valid!
            # Set the is_patient flag, associate the patient with the class,
            # and redirect to patient home.

            # STEP 1: Set is_patient flag
            request.user.is_patient = True

            # STEP 2: Associate patient with class
            request.user.class_id = Class.objects.get(
                join_code=form.cleaned_data['join_code'])

            # STEP 3: Save it all & redirect to patient home
            request.user.save()
            return redirect(reverse('redirect_user'))

    else:
        form = PatientSetupForm()

    return render(request, 'core/patient_setup.html', {'form': form})