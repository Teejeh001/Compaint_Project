from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentSignupForm, ComplaintForm, AdminResponseForm
from .models import Student, Complaint
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
def home(request):
    return render(request, 'home.html')




def signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to home after signup
    else:
        form = StudentSignupForm()
    return render(request, 'signup.html', {'form': form}) 



# def submit_complaint(request):
#     if request.method == 'POST':
#         # save complaint
#         return redirect('complaint_success')

#     return render(request, 'submit_complaint.html')





def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            matric_no = form.cleaned_data['matric_no']
            try:
                student = Student.objects.get(matric_no=matric_no)
                complaint = Complaint(
                    student=student,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description']
                )
                complaint.save()
                messages.success(request, 'Complaint submitted successfully!')
                return redirect('view_student_complaints')
            except Student.DoesNotExist:
                messages.error(request, 'Matric number not found. Please signup first.')
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})



# dashboard view for students

def dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    complaints = Complaint.objects.filter(student=student).order_by('-created_at')  # <-- fixed here

    return render(request, 'dashboard.html', {
        'student': student,
        'complaints': complaints
    })







def admin_response(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        form = AdminResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('view_complaints')
    else:
        form = AdminResponseForm(instance=complaint)
    return render(request, 'admin_response.html', {'form': form, 'complaint': complaint})


# login view for students
def login_view(request):
    if request.method == 'POST':
        matric_no = request.POST.get('matric_no')
        email = request.POST.get('email')

        try:
            student = Student.objects.get(matric_no=matric_no, email=email)
            request.session['student_id'] = student.id
            return redirect('dashboard')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid matric number or email')

    return render(request, 'login.html')



# logout view for students
def logout_view(request):
    request.session.flush()   # clears all session data
    return redirect('home')




# view complaints submitted by logged-in student
def view_student_complaints(request):
    # ✅ Check if student is logged in
    if 'student_id' not in request.session:
        return redirect('login')

    student_id = request.session['student_id']
    # ✅ Get only complaints submitted by this student
    complaints = Complaint.objects.filter(student__id=student_id).order_by('-id')

    return render(request, 'view_student_complaints.html', {
        'complaints': complaints
    })




# Admin view to see all complaints
@staff_member_required
def view_admin_complaints(request):
    complaints = Complaint.objects.all().order_by('-id')
    return render(request, 'view_admin_complaints.html', {
        'complaints': complaints
    })


# Admin responds or updates status
@staff_member_required
def admin_response(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # Approved or Rejected
        response = request.POST.get('admin_response')

        complaint.status = status
        complaint.admin_response = response
        complaint.save()

        return redirect('view_admin_complaints')

    return render(request, 'admin_response.html', {
        'complaint': complaint
    })