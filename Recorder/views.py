from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models.functions import Now
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.conf import settings
from .forms import RevenueForm, HistoryForm
from .forms import ExpendForm
from .forms import LabourForm
from .models import Revenue
from .models import Expend
from .models import Labour
from datetime import date
from django.db.models import Q
import datetime
import requests
import sys
import csv
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.mail import send_mail
from PIL import Image
# Create your views here.


def data_filter(model, date, user, period='day'):
    if period == 'day':
        data = model.objects.filter(Date__gte=date, user=user)
        return data
    elif period == 'month':
        data = model.objects.filter(Date__month=date, user=user)
        return data



def index(request):
    if request.method == 'GET':
        RForm = RevenueForm()
        EForm = ExpendForm()
        LForm = LabourForm()
        return render(request, 'index.html',{'RForm':RForm,'EForm':EForm, 'LForm':LForm})
    else:
        if request.POST.get('revenue'):
            form = RevenueForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.user = request.user
                newform.save()
                return redirect('index')
        elif request.POST.get('expend'):
            form = ExpendForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.user = request.user
                newform.save()
                return redirect('index')
        elif request.POST.get('labour'):
            form = LabourForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.user = request.user
                newform.save()
                return redirect('index')
        else:
            return redirect('total')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password2 == password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used, try another one')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used, try another one')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def Redelete(request, pk):
    obj = get_object_or_404(Revenue, pk=pk, user=request.user)
    obj.delete()
    return redirect('total')

def Exdelete(request, pk):
    obj = get_object_or_404(Expend, pk=pk, user=request.user)
    obj.delete()
    return redirect('total')

def Ladelete(request, pk):
    obj = get_object_or_404(Labour, pk=pk, user=request.user)
    obj.delete()
    return redirect('total')


def total(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            revenues = data_filter(Revenue, datetime.date.today(), request.user)
            expenses = data_filter(Expend, datetime.date.today(), request.user)
            labours = data_filter(Labour, datetime.date.today(), request.user)
            rev_num = 0
            ex_num = 0
            la_num = 0
            total_revenue = 0
            total_expense = 0
            total_labour = 0
            data = []
            profit = 0
            for revenue in revenues:
                total_revenue += float(revenue.PriceAmount)
                rev_num += 1
            for expense in expenses:
                total_expense += float(expense.PriceAmount)
                ex_num += 1
            for labour in labours:
                total_labour += float(labour.PriceAmount)
                la_num += 1
            profit = float(total_revenue) - float(total_expense) - float(total_labour)

            data.append(round(total_revenue))
            data.append(round(total_expense))
            data.append(round(total_labour))

            return render(request, 'total.html',{'revenues':revenues, 'expenses':expenses,'labours':labours, 'total_revenue':total_revenue, 'total_expense':total_expense, 'total_labour':total_labour, 'profit':profit,'data':data,'rev_num':rev_num,'ex_num':ex_num,'la_num':la_num})
    else:
        emaillist = []
        usersmail = request.user.email
        emaillist.append(usersmail)
        revenues = data_filter(Revenue, datetime.date.today(), request.user)
        expenses = data_filter(Expend, datetime.date.today(), request.user)
        labours = data_filter(Labour, datetime.date.today(), request.user)
        total_revenue = 0
        total_expense = 0
        total_labour = 0
        data = []
        profit = 0
        for revenue in revenues:
            total_revenue += float(revenue.PriceAmount)
        for expense in expenses:
            total_expense += float(expense.PriceAmount)
        for labour in labours:
            total_labour += float(labour.PriceAmount)
        profit = float(total_revenue) - float(total_expense) - float(total_labour)
        send_mail(
            '今日营业表现',
            '总收入: RM'+ str(total_revenue) +'。 总开销: RM'+ str(total_expense) +'。 总人工: RM'+ str(total_labour)+'。 利润: RM'+ str(profit),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emaillist)

        return redirect('total')



def pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)
    revenues = data_filter(Revenue, datetime.date.today(), request.user)
    expenses = data_filter(Expend, datetime.date.today(), request.user)
    labours = data_filter(Labour, datetime.date.today(), request.user)
    total_revenue = 0
    total_expense = 0
    total_labour = 0
    profit = 0
    for revenue in revenues:
        total_revenue += float(revenue.PriceAmount)
    for expense in expenses:
        total_expense += float(expense.PriceAmount)
    for labour in labours:
        total_labour += float(labour.PriceAmount)
    Final_lines = 'RM'+str(total_revenue) + ' - ' + 'RM'+str(total_expense) + ' - ' 'RM'+str(total_labour)
    profit = float(total_revenue) - float(total_expense) - float(total_labour)
    rev_lines = ['Sales']
    ex_lines = ['Expense']
    la_lines = ['Labour']


    for revenue in revenues:
        rev_lines.append('RM'+str(revenue.PriceAmount)+'  --  '+str(revenue.Date))

    rev_lines.append('Total: '+'RM'+str(total_revenue))

    for expense in expenses:
        ex_lines.append('RM'+str(expense.PriceAmount)+'  --  '+str(expense.Supplier))

    ex_lines.append('Total: '+'RM'+str(total_expense))

    for labour in labours:
        la_lines.append('RM'+str(labour.PriceAmount)+'  --  '+str(labour.LabourName))

    la_lines.append('Total: '+'RM'+str(total_labour))

    for line in rev_lines:
        if line == 'Sales':
            textob.setFont('Helvetica-Bold', 17)
            textob.textLine(line)
            textob.textLine('')
        else:
            textob.setFont('Helvetica', 14)
            textob.textLine(line)
            textob.textLine('')

    for line in ex_lines:
        if line == 'Expense':
            textob.setFont('Helvetica-Bold', 17)
            textob.textLine(line)
            textob.textLine('')
        else:
            textob.setFont('Helvetica', 14)
            textob.textLine(line)
            textob.textLine('')

    for line in la_lines:
        if line == 'Labour':
            textob.setFont('Helvetica-Bold', 17)
            textob.textLine(line)
            textob.textLine('')
        else:
            textob.setFont('Helvetica', 14)
            textob.textLine(line)
            textob.textLine('')

    textob.textLine('PROFIT: '+Final_lines+' = '+'RM'+str(profit))

    date = str(datetime.date.today())

    p.drawText(textob)
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=date+'.pdf')

def crsl(request):
    return render(request,'crsl.html')

def history(request):
    if request.method == 'GET':
        HForm = HistoryForm()
        today = date.today()
        revenues = Revenue.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
        expenses = Expend.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
        labours = Labour.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
        total_rev = 0
        total_ex = 0
        total_lb = 0
        for rev in revenues:
            total_rev += float(rev.PriceAmount)
        for ex in expenses:
            total_ex += float(ex.PriceAmount)
        for lb in labours:
            total_lb += float(lb.PriceAmount)
        profit = float(total_rev) - float(total_ex) - float(total_lb)
        Roundoff_Profit = format(profit, '.2f')
        return render(request, 'history.html', {'revs':revenues, 'exs':expenses, 'lbs':labours,'total_rev':total_rev,'total_ex':total_ex,'total_lb':total_lb, 'RFprofit':Roundoff_Profit, 'HForm':HForm})
    else:
        try:
            global xrevs
            global xexs
            global xlbs
            today = date.today()
            revenues = Revenue.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
            expenses = Expend.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
            labours = Labour.objects.filter(user=request.user, Date__month=today.month).order_by('-Date', '-Time')
            total_rev = 0
            total_ex = 0
            total_lb = 0
            for rev in revenues:
                total_rev += float(rev.PriceAmount)
            for ex in expenses:
                total_ex += float(ex.PriceAmount)
            for lb in labours:
                total_lb += float(lb.PriceAmount)
            profit = float(total_rev) - float(total_ex) - float(total_lb)
            Roundoff_Profit = format(profit, '.2f')
            From_Date = request.POST['From_Date']
            Until_Date = request.POST['Until_Date']
            xrevs = Revenue.objects.filter(user=request.user, Date__range=[From_Date, Until_Date]).order_by('-Date', '-Time')
            xexs = Expend.objects.filter(user=request.user, Date__range=[From_Date, Until_Date]).order_by('-Date', '-Time')
            xlbs = Labour.objects.filter(user=request.user, Date__range=[From_Date, Until_Date]).order_by('-Date', '-Time')
            total_xrev = 0
            total_xex = 0
            total_xlb = 0
            for xrev in xrevs:
                total_xrev += float(xrev.PriceAmount)
            for xex in xexs:
                total_xex += float(xex.PriceAmount)
            for xlb in xlbs:
                total_xlb += float(xlb.PriceAmount)
            xprofit = float(total_xrev) - float(total_xex) - float(total_xlb)
            Roundoff_XProfit = format(xprofit, '.2f')
            return render(request, 'history.html', {'From_Date':From_Date, 'Until_Date':Until_Date, 'xrevs':xrevs, 'xexs':xexs,
                                                    'xlbs':xlbs, 'total_xrev':total_xrev,'total_xex':total_xex,'total_xlb':total_xlb,
                                                    'RFXprofit':Roundoff_XProfit, 'revs':revenues, 'exs':expenses, 'lbs':labours,'total_rev':total_rev,
                                                    'total_ex':total_ex,'total_lb':total_lb, 'RFprofit':Roundoff_Profit})
        except:
            messages.info(request, 'Please insert Date Period')
            return redirect('history')


def period_record_csv(request):
    try:
        response = HttpResponse(content_type='text/csv',
                                headers={'Content-Disposition': 'attachment; filename="business_activities.csv"'})
        writer = csv.writer(response)
        pxrevs = xrevs
        pxexes = xexs
        pxlbs = xlbs
        writer.writerow(['REVENUES'])
        writer.writerow(['', 'Price', 'UnitNumber', 'PayerName', 'Date', 'user'])
        for pxrev in pxrevs:
            writer.writerow(['', pxrev.PriceAmount, pxrev.UnitNumber, pxrev.PayerName, pxrev.Date, pxrev.user])
        writer.writerow(['EXPENSES'])
        writer.writerow(['', 'Price', 'Supplier', 'Date'])
        for pxexp in pxexes:
            writer.writerow(['', pxexp.PriceAmount, pxexp.Supplier, pxexp.Date])
        writer.writerow(['LABOURS'])
        writer.writerow(['', 'Price', 'Labour Name', 'Date'])
        for pxlb in pxlbs:
            writer.writerow(['', pxlb.PriceAmount, pxlb.LabourName, pxlb.Date])
        return response
    except NameError:
        messages.info(request,'Please insert Date Period before downloading the file!!!')
        return redirect('history')


def record_csv(request):
    response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="revenue.csv"'})
    writer = csv.writer(response)
    revenues = data_filter(Revenue, datetime.date.today(), request.user)
    expenses = data_filter(Expend, datetime.date.today(), request.user)
    labours = data_filter(Labour, datetime.date.today(), request.user)
    writer.writerow(['','Price', 'UnitNumber','PayerName','Date','user'])
    for rev in revenues:
        writer.writerow(['', rev.PriceAmount, rev.UnitNumber, rev.PayerName,rev.Date,rev.user ])
    writer.writerow(['NEXT ROW'])
    writer.writerow(['', 'Price', 'Supplier', 'Date'])
    for exp in expenses:
        writer.writerow(['', exp.PriceAmount, exp.Supplier, exp.Date])
    writer.writerow(['NEXT ROW'])
    writer.writerow(['', 'Price', 'Labour Name', 'Date'])
    for lb in labours:
        writer.writerow(['', lb.PriceAmount, lb.LabourName, lb.Date])
    return response


def overview(request):
    if request.method == 'GET':
        today = date.today()
        revenues = data_filter(Revenue, today.month, request.user, 'month').order_by('-Date', '-Time')
        weekdays = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0}
        for rev in revenues:
            for day in weekdays:
                if str(rev.Date.weekday()) == day:
                    weekdays[day] += int(rev.PriceAmount)


        profits = []
        for day in weekdays:
            profits.append(weekdays[day])

        return render(request, 'overview.html',{'weekdays':weekdays,'profits': profits})
