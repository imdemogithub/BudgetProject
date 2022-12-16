from django.test import TestCase

# Create your tests here.
import datetime


months = []
mt = []
for m in range(1, 13):
    d = datetime.date(2022, m, 1)
    g = {
        'month_num': m,
        'month_name': d.strftime("%B"),
    }
    months.append(g)
    mt.append((m, d.strftime("%B")))

# print(months)
print(mt)
    