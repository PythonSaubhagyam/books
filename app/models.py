from django.db import models

class category(models.Model):
    cname=models.CharField(max_length=200)
    def __str__(self):
        return self.cname

class Slider(models.Model):
    bimg=models.ImageField(upload_to='bimg')

class Books(models.Model):
    cname=models.ForeignKey(category,on_delete=models.CASCADE)
    book_name=models.CharField(max_length=1000)
    author=models.CharField(max_length=500)
    foreword_by=models.CharField(max_length=500,blank=True)
    editer1=models.CharField(max_length=500,blank=True)
    editer2=models.CharField(max_length=500,blank=True)
    publication=models.CharField(max_length=1000)
    release_date=models.DateTimeField()
    best_seller=models.BooleanField(default=False)
    price=models.IntegerField()
    image=models.ImageField(upload_to='bookimg')
    language=models.CharField(max_length=100)
    isbn_13=models.IntegerField()
    isbn_10=models.IntegerField()
    pages=models.IntegerField()
    ebook=models.FileField(upload_to='ebook')
 

class Register(models.Model):
    fname=models.CharField(max_length=500)
    lname=models.CharField(max_length=500)
    email=models.EmailField()
    password=models.CharField(max_length=12)

class Cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.IntegerField()
    
class Myorder(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    book1=models.ForeignKey(Books,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

class My(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    book2=models.ForeignKey(Books,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    read=models.BooleanField(default=True)

class Subcategory(models.Model):
    cname=models.ForeignKey(category,on_delete=models.CASCADE)
    sname=models.CharField(max_length=500)