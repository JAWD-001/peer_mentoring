from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from groups.models import Group


# Create your views here.
def search(request):
    query = request.GET.get("q", "")
    if query:
        user_results = User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )

        group_results = Group.objects.filter(Q(title__icontains=query))
    else:
        user_results = []
        group_results = []

    context = {
        "query": query,
        "user_results": user_results,
        "group_results": group_results,
    }

    return render(request, "search_results.html", context)
