from django.shortcuts import render, redirect
from .forms import FeedbackForm

def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = request.user
            obj.save()
            return redirect("patient-dashboard")
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback_form.html", {"form": form})
