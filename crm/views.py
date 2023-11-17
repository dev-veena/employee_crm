from django.shortcuts import render,redirect
from django.views.generic import View
from crm.forms import EmployeeForm,EmployeesModelForm,RegistrationForm,LoginForm
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# -----------decorators-----------------
def Signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper    
# ------------------

# Create your views here
@method_decorator(Signin_required,name="dispatch")
class EmployeeCreateView(View):
    
    def get(self,request,*args,**kwargs):
        form=EmployeesModelForm()
        return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=EmployeesModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            # Employees.objects.create(**form.cleaned_data) #orm query explicite ayu kodukanata athinu pakaram form.save() use akam
            #or
            form.save() 
            messages.success(request,"Added Successfully")
            print('created')
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"Failed to add employee")
            return render(request,"emp_add.html",{"form":form})
# -----------------------------------------------------------------------------------
@method_decorator(Signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
            qs=Employees.objects.all()
            departments=Employees.objects.all().values_list("department",flat=True).distinct()
            print(departments)
            print(request.GET)
            if "department" in request.GET:
                dept=request.GET.get("department")
                print(dept)
                qs=qs.filter(department__iexact=dept)
                print(qs)  
            return render(request,"emp_list.html",{"data":qs,"department":departments})
    def post(self,request,*args,**kwargs):
        name=request.POST.get('box')
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,'emp_list.html',{'data':qs})        
# ---------------------------------------------------------------------------------
@method_decorator(Signin_required,name="dispatch")
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        # kwargs={pk:5}
        id=kwargs.get('pk')
        qs=Employees.objects.get(id=id)
        return render(request,'emp_details.html',{'data':qs})
    
#-----------------------------------------------------------------------------------------
@method_decorator(Signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Employees.objects.get(id=id).delete()
        messages.success(request,"employee deleted")
        return redirect("emp-all") 
#-------------------------------------------------------------------------------------------
@method_decorator(Signin_required,name="dispatch")
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Employees.objects.get(id=id)
        form=EmployeesModelForm(instance=obj)
        return render(request,'emp_edit.html',{'form':form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Employees.objects.get(id=id)
        form=EmployeesModelForm(request.POST,instance=obj,files=request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request,'update successfully')
            return redirect('emp-detail',pk=id)
        else:
            messages.error(request,"error to update")
            return render(request,'emp_edit.html',{'form':form})
#-------------------------------------------------------------------------
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            # create_user -pswd encript cheyyan
            messages.success(request,"created successfully")
            print('success')
            return render(request,'register.html',{'form':form})
        else:
            messages.error(request,"create failed")

            print("failed")
            return render(request,'register.html',{'form':form})
        
# ---------------------------
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
           # print(form.cleaned_data) --->#{'username': 'django', 'password': 'password@123'}
           usr_name=form.cleaned_data.get('username')
           pwd=form.cleaned_data.get('password')
           print(usr_name,pwd)
           user_obj=authenticate(request,username=usr_name,password=pwd)
           print(user_obj)
           if user_obj:
               print("valid")
               login(request,user_obj)
               return redirect('emp-all')
        #    else:
        #        print('invalid')    
        #    return render(request,'login.html',{'form':form})
        # else:
        #     messages.error(request,"invalid credential")
        #     return render(request,'login.html',{'form':form})
        messages.error(request,"invalid credential")
        return render(request,'login.html',{'form':form})
# -------------------------------------------------
@method_decorator(Signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)    
        return redirect('signin')
# -----------------------------------------------------
