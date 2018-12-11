from django.contrib import admin
from mainapp.models import Dgmtypeeffects, Invtypes, Fitting


@admin.register(Dgmtypeeffects)
class DgmtypeeffectsAdmin(admin.ModelAdmin):
    list_display = ('typeid', 'effectid')


@admin.register(Invtypes)
class InvtypesAdmin(admin.ModelAdmin):
    list_display = ('typeid', 'groupid', 'typename', 'description')


@admin.register(Fitting)
class FittingAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
