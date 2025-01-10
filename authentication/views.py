import os
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm

from django.shortcuts import render
from django.http import FileResponse
from .models import ExcelFile
from django.contrib.auth import logout
from .forms import ExcelFileForm
import pandas as pd  # Import pandas library to handle Excel files
from .models import ExcelFile
import pandas as pd
from .models import Event
import joblib


def upload_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        print("File uploaded:", excel_file.name)  # Debugging output
        if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
            # Read the Excel file using pandas
            try:
                df = pd.read_excel(excel_file)
                # Process the DataFrame 'df' as needed
                # For example, you can save it to the database using Django model
                # Example: ExcelFile.objects.create(file=excel_file)
                messages.success(
                    request, 'Excel file uploaded and processed successfully.')
                print("Excel file processed successfully.")  # Debugging output
            except Exception as e:
                messages.error(
                    request, f'Error processing the Excel file: {str(e)}')
                print("Error processing Excel file:",
                      str(e))  # Debugging output
        else:
            messages.error(request, 'Please upload a valid Excel file.')
    else:
        messages.error(request, 'No file uploaded.')
    # Redirect to the admin change list page
    return redirect('admin:yourapp_excelfile_changelist')


def logout_view(request):
    logout(request)
    # Redirect to the home page or any other page after logout
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user with the provided credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If authentication is successful, log the user in
                login(request, user)
                print("Login success")  # Debugging output
                # Redirect to a specific page after login
                return redirect('nav')
            else:
                print("Login error")  # Debugging output
                form.add_error(None, "Invalid username or password.")
                # Add an error if authentication fails
                messages.error(
                    request, 'Please enter a valid username or password.')
    else:
        form = LoginForm()  # Create a new form instance for GET requests

    return render(request, 'login.html', {'form': form})


def register_views(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Registration success')  # Debugging output
            # Redirect to the login page after successful registration
            return redirect('login')
        else:
            print('Registration not success. Errors:',
                  form.errors)  # Debugging output
    else:
        form = UserRegistrationForm()  # Create a new form instance for GET requests

    return render(request, 'register_test.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your password was successfully updated!')
            # Redirect to the profile page or any other page after changing password
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

# Placeholder view for logout


# Placeholder view for nav
def nav_view(request):
    return render(request, 'nav.html')


def home(request):

    return render(request, 'home.html')


def excel_file_view(request, file_id):
    excel_file = ExcelFile.objects.get(id=file_id)
    # Assuming 'file_field' is the FileField in your ExcelFile model
    file_path = excel_file.file_field.path
    return FileResponse(open(file_path, 'rb'))


def excel_file_list(request):
    excel_files = ExcelFile.objects.all()
    return render(request, 'excel_file_list.html', {'excel_files': excel_files})


def servicce(request):
    return render(request, 'servicce.html')


def about(request):
    return render(request, 'about.html')


def duphome(request):
    return render(request, 'duphome.html')


def displayxl(request):
    excel_dir = os.path.join(settings.MEDIA_ROOT, 'excel_files')

    # List to hold HTML tables
    html_tables = []

       # Iterate through each Excel file in the directory
    for filename in os.listdir(excel_dir):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(excel_dir, filename)
            # Read the Excel file
            df = pd.read_excel(file_path)
                # Convert the DataFrame to an HTML table
            html_table = df.to_html(classes='table table-striped')
                # Add the table to the list with the filename as a header
            html_tables.append((filename, html_table))

        # Pass the HTML tables to the template
    context = {'html_tables': html_tables}
    return render(request, 'displayxl.html', context)


def events_and_trainings(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


def prediction(request):
    context = {}
    if request.method == 'POST':
        cgpa = float(request.POST.get('cgpa'))
        mooc_courses = int(request.POST.get('mooc_courses'))
        internships = int(request.POST.get('internships'))

        # Keep the input values in the context
        context['cgpa'] = cgpa
        context['mooc_courses'] = mooc_courses
        context['internships'] = internships

        model_path = os.path.join(settings.BASE_DIR, 'model_campus_placemen')
        model = joblib.load(model_path)
        new_data = pd.DataFrame({
            'CGPA': [cgpa],
            'Number of MOOC Courses': [mooc_courses],
            'Number of Internships': [internships]
        })

        prediction = model.predict(new_data)[0]
        probabilities = model.predict_proba(new_data)[0]

        
        context.update({
            'prediction': 'Placed' if prediction == 1 else 'Not Placed',
            'probability_placed': f"{probabilities[1]:.2%}",
            'probability_not_placed': f"{probabilities[0]:.2%}",
        })
    
    return render(request, 'prediction.html', context)




def notifications(request):
    events = Event.objects.all().order_by('-date')  # Fetch all events, ordering by date (newest first)
    context = {
        'events': events
    }
    return render(request, 'notifications.html', context)