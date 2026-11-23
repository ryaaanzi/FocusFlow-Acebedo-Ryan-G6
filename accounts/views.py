
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import (
    RegistrationForm,
    ProfileUpdateForm,
    ProfileDetailsForm,
    ActivityRecordForm,
)
from .models import Profile, ActivityRecord


def register_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.create(
                    user=user,
                    role='STUDENT'
                )

            messages.success(
                request,
                'Your FocusFlow account has been created successfully!'
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        messages.success(
            request,
            'You have successfully logged out.'
        )
        return redirect('login')

    return redirect('dashboard')


@login_required
def dashboard_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role == 'ADMIN':
        return redirect('admin_dashboard')

    return redirect('student_dashboard')


@login_required
def student_dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You are not authorized to access this dashboard."
        )

    return render(
        request,
        'accounts/student_dashboard.html',
        {'profile': profile}
    )


@login_required
def admin_dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'ADMIN':
        return HttpResponseForbidden(
            "You are not authorized to access this dashboard."
        )

    return render(
        request,
        'accounts/admin_dashboard.html',
        {'profile': profile}
    )


@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        user_form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileDetailsForm(
            request.POST,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('profile')

    else:
        user_form = ProfileUpdateForm(
            instance=request.user
        )

        profile_form = ProfileDetailsForm(
            instance=profile
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


@login_required
def activity_list(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You are not authorized to access the Activity Tracker."
        )

    activities = ActivityRecord.objects.filter(
        user=request.user
    )

    return render(
        request,
        'accounts/activity_list.html',
        {
            'activities': activities,
        }
    )


@login_required
def activity_create(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You are not authorized to create activity records."
        )

    if request.method == 'POST':
        form = ActivityRecordForm(request.POST)

        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            messages.success(
                request,
                'Activity record added successfully!'
            )

            return redirect('activity_list')

    else:
        form = ActivityRecordForm()

    return render(
        request,
        'accounts/activity_form.html',
        {
            'form': form,
            'page_title': 'Add Activity',
        }
    )


@login_required
def activity_update(request, pk):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You are not authorized to update activity records."
        )

    activity = get_object_or_404(
        ActivityRecord,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = ActivityRecordForm(
            request.POST,
            instance=activity
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Activity record updated successfully!'
            )

            return redirect('activity_list')

    else:
        form = ActivityRecordForm(
            instance=activity
        )

    return render(
        request,
        'accounts/activity_form.html',
        {
            'form': form,
            'page_title': 'Edit Activity',
        }
    )


@login_required
def activity_delete(request, pk):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You are not authorized to delete activity records."
        )

    activity = get_object_or_404(
        ActivityRecord,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        activity.delete()

        messages.success(
            request,
            'Activity record deleted successfully!'
        )

        return redirect('activity_list')

    return render(
        request,
        'accounts/activity_confirm_delete.html',
        {
            'activity': activity,
        }
    )