from django import forms
from django.contrib import admin
from django.conf import settings
from simple_translation.admin import TranslationAdmin
from cmsplugin_blog.models import Entry, EntryTitle
from cmsplugin_blog.widgets import AutoCompleteTagInput
from cms.forms.widgets import PlaceholderPluginEditorWidget
from django.utils.text import capfirst
from django.template.defaultfilters import title, escape, force_escape, escapejs
from django.forms import CharField
from copy import deepcopy

class EntryForm(forms.ModelForm):
        
    class Meta:
        model = Entry
        widgets = {'tags': AutoCompleteTagInput}
        
    title = forms.CharField()
    slug = forms.SlugField()
    
class M2MPlaceholderAdmin(TranslationAdmin):
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Get PageForm for the Page model and modify its fields depending on
        the request.
        """
        form = super(M2MPlaceholderAdmin, self).get_form(request, obj, **kwargs)
        
        if obj:        
            
            for placeholder_name in obj._meta.get_field('placeholders').placeholders:
                
                placeholder, created = obj.placeholders.get_or_create(slot=placeholder_name)
                
                defaults = {'label': capfirst(placeholder_name), 'help_text': ''}
                defaults.update(kwargs)
                
                widget = PlaceholderPluginEditorWidget(request, self.placeholder_plugin_filter)
                widget.choices = []
                
                form.base_fields[placeholder.slot] = CharField(widget=widget, required=False)   
                form.base_fields[placeholder.slot].initial = placeholder.pk
                
        return form
        
    def get_fieldsets(self, request, obj=None):
        """
        Add fieldsets of placeholders to the list of already existing
        fieldsets.
        """
        given_fieldsets = super(M2MPlaceholderAdmin, self).get_fieldsets(request, obj=None)

        if obj: # edit
            for placeholder_name in obj._meta.get_field('placeholders').placeholders:
                given_fieldsets += [(title(placeholder_name), {'fields':[placeholder_name], 'classes':['plugin-holder']})]

        return given_fieldsets
        
                
class EntryAdmin(M2MPlaceholderAdmin):
    
    form = EntryForm
    
    prepopulated_fields = {}
        
    list_display = ('description', 'languages', 'is_published')
    list_editable = ('is_published',)
    
    def __init__(self, *args, **kwargs):
        super(EntryAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields.update({'slug': ('title',)})
        
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(EntryAdmin, self).get_fieldsets(request, obj=obj)
        fieldsets[0] = (None, {'fields': (
            'language',
            'is_published',
            'pub_date',
            'title',
            'slug',
            'tags'
        )})
        return fieldsets
           
admin.site.register(Entry, EntryAdmin)

