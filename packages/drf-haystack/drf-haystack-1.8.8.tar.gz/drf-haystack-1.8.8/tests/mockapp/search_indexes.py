# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from haystack import indexes

from .models import MockLocation, MockPerson, MockPet, MockAllField


class MockLocationIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    address = indexes.CharField(model_attr="address")
    city = indexes.CharField(model_attr="city")
    zip_code = indexes.CharField(model_attr="zip_code")

    autocomplete = indexes.EdgeNgramField()
    coordinates = indexes.LocationField(model_attr="coordinates")

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.address, obj.city, obj.zip_code
        ))

    def get_model(self):
        return MockLocation

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created__lte=timezone.now()
        )


class MockPersonIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    firstname = indexes.CharField(model_attr="firstname", faceted=True)
    lastname = indexes.CharField(model_attr="lastname", faceted=True)
    birthdate = indexes.DateField(model_attr="birthdate", faceted=True)
    letters = indexes.MultiValueField(faceted=True)
    full_name = indexes.CharField()
    description = indexes.CharField()

    autocomplete = indexes.EdgeNgramField()
    created = indexes.FacetDateTimeField(model_attr="created")

    @staticmethod
    def prepare_full_name(obj):
        return " ".join((obj.firstname, obj.lastname))

    @staticmethod
    def prepare_letters(obj):
        return [x for x in obj.firstname]

    @staticmethod
    def prepare_description(obj):
        return " ".join((obj.firstname, "is a nice chap!"))

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((obj.firstname, obj.lastname))

    def get_model(self):
        return MockPerson

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created__lte=timezone.now()
        )


class MockPetIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    species = indexes.CharField(model_attr="species")
    has_rabies = indexes.BooleanField(indexed=False)
    description = indexes.CharField()

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_description(obj):
        return " ".join((obj.name, "the", obj.species))

    @staticmethod
    def prepare_has_rabies(obj):
        return True if obj.species == "Dog" else False

    @staticmethod
    def prepare_autocomplete(obj):
        return obj.name

    def get_model(self):
        return MockPet


class MockAllFieldIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=False)
    charfield = indexes.CharField(model_attr="charfield")
    integerfield = indexes.IntegerField(model_attr="integerfield")
    floatfield = indexes.FloatField(model_attr="floatfield")
    decimalfield = indexes.DecimalField(model_attr="decimalfield")
    boolfield = indexes.BooleanField(model_attr="boolfield")
    datefield = indexes.DateField(model_attr="datefield")
    datetimefield = indexes.DateTimeField(model_attr="datetimefield")
    multivaluefield = indexes.MultiValueField()

    @staticmethod
    def prepare_multivaluefield(obj):
        return obj.charfield.split(' ', 1)

    def get_model(self):
        return MockAllField
