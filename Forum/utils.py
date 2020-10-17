from django.contrib.auth import login
from django.views.generic import ListView
from django.http import Http404


from .forms import *


class MyPaginator(object):

    pages = object

    def get_pages(self,):
        num_pages = self.pages.paginator.num_pages
        number = self.pages.number
        if num_pages < 10:
            return (range(1, num_pages + 1))
        elif number > num_pages - 5:
            return (range(num_pages - 8, num_pages + 1))
        else:
            return (range(number - 4, number + 4))



