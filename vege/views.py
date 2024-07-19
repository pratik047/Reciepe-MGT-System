from django.shortcuts import render, redirect

from home.views import contact
from .models import Receipe, Student, SubjectMarks
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib.auth import get_user_model
from django.db.models import Sum
from accounts.models import CustomUser


# @login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description,
        )

        return redirect("/receipes/")

    queryset = Receipe.objects.all()

    if request.GET.get("search"):
        queryset = queryset.filter(receipe_name__icontains=request.GET.get("search"))

    context = {"receipes": queryset}
    return render(request, "receipes.html", context)


@login_required(login_url="/login/")
def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect("/receipes/")


@login_required(login_url="/login/")
def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect("/receipes/")

    context = {"receipes": queryset}
    return render(request, "update_receipe.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not CustomUser.objects.filter(username=username).exists():
            messages.info(request, " Invalid Username")
            return redirect("/login/")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, " Invalid Password")
            return redirect("/login/")

        else:
            login(request, user)
            return redirect("/receipes/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the username already exists
        user = CustomUser.objects.filter(username=username)
        if user.exists():
            # If the username exists, inform the user and redirect to registration page
            messages.info(
                request, "Username already exists. Please choose a different one."
            )
            return redirect("/register/")

        # Create a new user object if the username is unique
        user = CustomUser.objects.create(
            first_name=first_name, last_name=last_name, username=username
        )

        # Set and hash the password for the new user
        user.set_password(password)
        user.save()

        # Display a success message and redirect to the registration page
        messages.success(request, "Registration successful. You can now log in.")
        return redirect("/login/")

    # Render the registration form template for GET requests
    return render(request, "register.html")


def get_student(request):
    queryset = Student.objects.all()

    if request.GET.get("search"):
        search = request.GET.get("search")
        queryset = queryset.filter(
            Q(student_name__icontains=search)
            | Q(department__department__icontains=search)
            | Q(student_id__student_id__icontains=search)
            | Q(student_email__icontains=search)
            | Q(student_age__icontains=search)
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    return render(request, "report/students.html", {"queryset": page_obj})


from .seed import generate_report_card


def see_marks(request, student_id):
    # Generate the report card (assuming this is a function defined elsewhere)
    generate_report_card()

    # Query the SubjectMarks for the specific student using correct lookup
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = queryset.aggregate(total_marks=Sum("marks"))["total_marks"]

    # Calculate the rank of the student
    current_rank = -1
    ranks = Student.objects.annotate(total_marks=Sum("studentmarks__marks")).order_by(
        "-total_marks", "student_age"
    )
    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i += 1

    # Render the template with the context data
    return render(
        request,
        "report/see_marks.html",
        {
            "queryset": queryset,
            "total_marks": total_marks,
            "current_rank": current_rank,
        },
    )
