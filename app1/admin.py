from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



from .models import *
# Register your models here.
def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['userid', 'finaltotal', 'paymode','timestamp']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.userid.name, obj.finaltotal, obj.paymode,obj.timestamp])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"


@admin.register(RegisterModel)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ["name","email","phone","password","address","image","gender","role"]

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["catname"]

@admin.register(color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["colorname","colorcode"]

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pname","catid","product_img","price","description","status","sellerid"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["userid","productid","quantity","totalprice","orderstatus","orderid"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["userid","finaltotal","phone","address","timestamp","status","paymode","razorpay_orderid"]
    list_filter = ['timestamp']
    actions = [export_to_pdf]

@admin.register(Wishlist)
class WishAdmin(admin.ModelAdmin):
    list_display = ["userid","productid","timestamp"]