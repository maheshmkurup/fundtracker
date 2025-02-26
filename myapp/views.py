from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from myapp.forms import SignUpForm,SignInForm,ExpenseForm

from django.contrib.auth import authenticate,login,logout

from myapp.models import Expense

from django.db.models import Sum,Count

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator

from django.contrib import messages

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=SignUpForm(form_data)

        if form_instance.is_valid():

            form_instance.save()

            print("xxxAccount Createdxxx")

            messages.success(request,"Account has been Successfully Created!")

            return redirect("register")

        else:

            print("xxxFailedxxx")

            messages.error(request,"Account Creation Failed Please try again!")

            return render(request,"register.html",{"form":form_instance})
        

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=SignInForm(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance:

                login(request,user_instance)

                print(">>>>>Login Successfull!")

                messages.success(request,"Login Success!")

                return redirect("index")
            
            else:

                print(">>>>>Login Failed!")

                messages.error(request,"Login failed Please try again!")

                return render(request,"signin.html",{"form":form_instance})
            
@method_decorator(signin_required,name="dispatch")

class IndexView(View):

    def get(self,request,*args,**kwargs):

        total_expense=Expense.objects.filter(owner=request.user).values("amount").aggregate(total=Sum("amount"))

        print(total_expense)

        category_summary=Expense.objects.filter(owner=request.user).values("category").annotate(total=Sum("amount"),count=Count("category")).order_by("-total")

        print(category_summary) 

        context={
            "total_expense":total_expense.get("total"),
            "category_summary":category_summary
        }

        return render(request,"index.html",context)

@method_decorator(signin_required,name="dispatch")    

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

@method_decorator(signin_required,name="dispatch")  

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        qs=Expense.objects.filter(owner=request.user).order_by("-created_at")

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=ExpenseForm(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Expense.objects.create(**data,owner=request.user)

            messages.success(request,"New Expense Created Successfully!")

            return redirect("expense-add")
        
        else:

            messages.error(request,"Expense Creation Failed!")

            return render(request,"expense_add.html",{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"Expense deleted Successfully!")

        return redirect("expense-add")

@method_decorator(signin_required,name="dispatch")  

class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_obj)

        return render(request,"expense_update.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_obj=Expense.objects.get(id=id)

        form_data=request.POST

        form_instance=ExpenseForm(form_data,instance=expense_obj)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Expense Updated Successfully!")

            return redirect("expense-add")
        
        else:

            messages.success(request,"Expense Update Failed!")

            return render(request,"expense-update.html",{"form":form_instance})






            


            

            





    



