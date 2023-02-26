from django.shortcuts import redirect

def is_staff(view):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_staff:
            return view(self, request, *args, **kwargs)
        return redirect('/')
    return wrapper