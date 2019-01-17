import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_lm.settings")
import django
django.setup()
import csv
from datetime import datetime
from portal.models import Employee, Date, Attendance, ValueModel
errors = 0
emp_added = 0
for row in csv.DictReader(open('new_at_csv/new_nov_18.csv', 'r')):
    for col in row:
        name = row.get('Name')
        if col == 'Name':
            print('Employee -->>>', name, ' : ', col, '-', row[col])
        else:
            try:
                emp = Employee.objects.get_or_create(Name=name)[0]
                date_format = datetime.strptime(col.strip(), '%m/%d/%Y')
                date = Date.objects.get_or_create(My_Date=date_format)[0]
                value = float(row[col])
                if value == 0.0:
                    if emp.Leave_Balance < 1:
                        value_add = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Leave')[0]
                    else:
                        value_add = ValueModel.objects.get_or_create(Fixed_Name='Paid_Leave')[0]
                elif value == 0.5:
                    if emp.Leave_Balance < 0.5:
                        value_add = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Half_Day')[0]
                    else:
                        value_add = ValueModel.objects.get_or_create(Fixed_Name='Paid_Half_Day')[0]
                elif value == 1.0:
                    value_add = ValueModel.objects.get_or_create(Fixed_Name='Full_Day')[0]
                att = Attendance.objects.create(Date=date, Value=value_add, User=emp)
                print(att.Value)
                att.User.save()
                print(att)
            except:
                errors += 1
                print(errors, '----------------------------------------------->>>', name, ' : ', col, '-', row[col])