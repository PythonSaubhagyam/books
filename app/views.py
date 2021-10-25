from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def index(request):
    cat=category.objects.all()
    slid=Slider.objects.all()
    sub=Subcategory.objects.order_by('cname')
    best=Books.objects.filter(best_seller=True)
    act=Books.objects.filter(cname=3).order_by('release_date')
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        status=My.objects.filter(user=user_info)
        cart=Cart.objects.filter(user=user_info)
        if request.session['subto']:
            subtotal=request.session['subto']
            return render(request,'index.html',{'cat':cat,'slid':slid,'best':best,'act':act,'status':status,'sub':sub,'cart':cart,'subtotal':subtotal})
        return render(request,'index.html',{'cat':cat,'slid':slid,'best':best,'act':act,'status':status,'sub':sub,'cart':cart})
    else:
        return render(request,'index.html',{'cat':cat,'slid':slid,'best':best,'act':act,'sub':sub})

def shop(request):
    cat=category.objects.all()
    cid=request.GET.get("cid")
    pro=Books.objects.filter(cname__id=cid)
    return render(request,'shop.html',{'cat':cat,'pro':pro})

def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        
        obj=Register(fname=fname,lname=lname,email=email,password=password)
        obj.save()
        return redirect('/')
            
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        pass1=request.POST['pass1']
        try:
            user_info=Register.objects.get(email=email)
            if user_info.password==pass1:
                request.session['user']=email
                return redirect('/')
            else:
                return render(request,'login.html',{'error':"Invalid Password"})    
        except:
            return render(request,'login.html',{'error':"Invalid Email"})        
    return render(request,'login.html')


def account(request):
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)  
        data1=My.objects.filter(user=user_info)
        context={'user_info':user_info,'data1':data1}
    return render(request,'my-account.html',context)

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')

def addtocart(request,id):
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        pro=Books.objects.get(id=id)
        cartexist=Cart.objects.filter(book__id=pro.id)
        if cartexist:
            return redirect('showcart')
        else:
            Cart(user=user_info,book=pro,subtotal=pro.price).save()
            return redirect('showcart')
        return render(request,'cart.html')
    else:
        return redirect('login')

def showcart(request):
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        c1=Cart.objects.filter(user__id=user_info.id)
        list1=[]
        subtotal=0
        for i in c1:
            list1.append(i.book.price)
            subtotal+=i.subtotal
            
        l1=sum(list1)
        request.session['subto']=subtotal
        context={'c1':c1,'subtotal':subtotal}
        return render(request,'cart.html',context)
    else:
        return redirect('login')

def checkout(request):
    cat=category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        c1=Cart.objects.filter(user__id=user_info.id)
        c2=My.objects.filter(user__id=user_info.id)
        l1=[]
        for j in c2:
            l1.append(j.book2.id)
        print(l1)
        for i in c1:
           
            if i.book.id in l1:
                return render(request,'checkout.html',{'error':f"book {i.book.book_name} already exist"})
                continue
            else:
                Myorder(user=user_info,book1=i.book).save()
                My(user=user_info,book2=i.book,read=True).save()
                Cart.delete()
                return redirect('index')
            # Books(read_status=True).save()
        
        
    return render(request,'checkout.html',{'c1':c1,'cat':cat})

def bookdetail(request):
    cat=category.objects.all()
    cid=request.GET.get('cid')
    data=Books.objects.get(pk=cid)
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        status=My.objects.filter(user=user_info)
        return render(request,'product-details.html',{'data':data,'status':status,'cat':cat})
    else:
        return render(request,'product-details.html',{'data':data,'cat':cat})


def mybooks(request):
    cat=category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        data1=My.objects.filter(user=user_info)
    return render(request,'mybook.html',{'data1':data1,'cat':cat})

def plus(request,id):
    l1=Cart.objects.get(id=id)
    total=l1.book.price
    l1.quantity+=1
    l1.subtotal=total*l1.quantity
    l1.save()
    return redirect('showcart')

def minus(request,id):
    l1=Cart.objects.get(id=id)
    total=l1.book.price
    l1.quantity-=1
    l1.subtotal=total*l1.quantity
    l1.save()
    return redirect('showcart')

def remove(request,id):
    l1=Cart.objects.get(id=id)
    l1.delete()
    return redirect('showcart')

def search(request):
    if request.method=='POST':
        sch=request.POST['sch']
        
    return render(request,'search.html')