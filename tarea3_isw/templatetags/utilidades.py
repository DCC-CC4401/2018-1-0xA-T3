from django import template
from ..models import Article, Place, User, ArticleLoan
from ..states import LoanStates, ReservationStates, ArticleStates, PlaceStates

register = template.Library()

@register.simple_tag
def ArticuloporId(pk, attr):
    obj = getattr(Article.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def EspacioporId(pk, attr):
    obj = getattr(Place.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def Diccionario(dicc, key):
    return dicc[key]

@register.simple_tag
def UserporId(pk, attr):
    obj = getattr(User.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def GetState(int):
    return LoanStates(int)

@register.simple_tag
def GetStateA(int):
    return ArticleStates(int)

@register.simple_tag
def GetStateR(int):
    return ReservationStates(int)

@register.simple_tag
def GetStateSp(int):
    return PlaceStates(int)




