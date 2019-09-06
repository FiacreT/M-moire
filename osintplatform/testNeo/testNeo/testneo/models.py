from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty
# Create your models here.

class Book(StructuredNode):
    title = StringProperty(unique_index=True)
    published = DateProperty()