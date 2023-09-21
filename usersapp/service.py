from django.shortcuts import redirect
from django.urls import reverse_lazy

class IsAdminOrStaff:
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect(reverse_lazy('usersapp:login'))
        
        return super().dispatch(request, *args, **kwargs)