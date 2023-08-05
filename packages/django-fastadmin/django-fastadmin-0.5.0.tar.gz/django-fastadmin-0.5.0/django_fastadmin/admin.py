import uuid
import copy
import json
from functools import update_wrapper


from fastutils import listutils
from fastutils import funcutils
from magic_import import import_from_string

from django.db import models
from django import forms
from django.forms import Textarea
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.options import unquote
from django.contrib import messages

from django_middleware_global_request.middleware import get_request

from .utils import jquery_plugins


class UuidFieldSearchableAdmin(admin.ModelAdmin):
    """Enable search by uuid string with dashes.
    """
    def get_search_results(self, request, queryset, search_term):
        try:
            search_term_new = search_term
            if isinstance(search_term_new, str):
                search_term_new = search_term_new.strip()
            search_term_new = uuid.UUID(search_term_new).hex
        except ValueError:
            search_term_new = search_term
        result = super().get_search_results(request, queryset, search_term_new)
        return result



class InlineBooleanFieldsAllowOnlyOneCheckedMixin(InlineModelAdmin):
    """Admin inline formset has a boolean field, so that there are many checkboxes of that field, make sure that only one checkbox is checked.
    """

    special_class_name = "inline-boolean-fields-allow-only-one-checked-mixin"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/inline-boolean-fields-allow-only-one-checked-mixin/inline-boolean-fields-allow-only-one-checked-mixin.js",
        ])


class InlineUniqueChoiceFieldsMixin(InlineModelAdmin):
    """ @todo
    """
    special_class_name = "with-inline-unique-choice-fields"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/with-inline-unique-choice-fields.js",
        ])





class DisableInlineEditingInAddingMixin(BaseModelAdmin):
    """Disable inline editing in main object adding step.
    """
    def get_inline_instances(self, request, obj=None):
        if not obj or not obj.pk:
            return []
        else:
            return super().get_inline_instances(request, obj)


class InlineEditingHideOriginalMixin(BaseModelAdmin):
    """Hide original part in inline editing.
    """
    class Media:
        css = {
            "all": [
                "fastadmin/admins/inline-editing-hide-original-mixin/inline-editing-hide-original-mixin.css",
            ]
        }


class DisableDeleteActionMixin(BaseModelAdmin):
    """Disable delete action for all user.
    """
    DELETE_ACTION_ENABLE_FOR_SUPERUSER = False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user and request.user.is_superuser and self.DELETE_ACTION_ENABLE_FOR_SUPERUSER:
            pass
        else:
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions



class DisableAddPermissionMixin(BaseModelAdmin):
    ADD_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_add_permission(self, request):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.ADD_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True

class DisableDeletePermissionMixin(BaseModelAdmin):
    DELETE_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_delete_permission(self, request, obj=None):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.DELETE_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True

class DisableChangePermissionMixin(BaseModelAdmin):
    CHANGE_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_change_permission(self, request, obj=None):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.CHANGE_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True


class MarkPermissionsMixin(BaseModelAdmin):

    def get_changing_object(self, request, object_id):
        if not object_id:
            return None
        else:
            to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
            obj = self.get_object(request, unquote(object_id), to_field)
            return obj

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        obj = self.get_changing_object(request, object_id)
        extra_context = extra_context or {}
        has_add_permission = self.has_add_permission(request)
        has_view_permssion = self.has_view_permission(request, obj)
        has_change_permission = self.has_change_permission(request, obj)
        has_delete_permission = self.has_delete_permission(request, obj)
        setattr(request, "has_add_permission", has_add_permission)
        setattr(request, "has_view_permssion", has_view_permssion)
        setattr(request, "has_change_permission", has_change_permission)
        setattr(request, "has_delete_permission", has_delete_permission)
        extra_context.update({
            "has_add_permission": has_add_permission,
            "has_view_permssion": has_view_permssion,
            "has_change_permission": has_change_permission,
            "has_delete_permission": has_delete_permission,
        })
        return super().changeform_view(request, object_id, form_url, extra_context)


class TextFieldAutoHeightMixin(BaseModelAdmin):
    class Media:
        js = jquery_plugins([
            "fastadmin/admins/text-field-auto-height-mixin/text-field-auto-height-mixin.js",
        ])

class TextFieldSetRowColumnMixin(BaseModelAdmin):
    TEXT_AREA_ROW = 1
    TEXT_AREA_COLS = 80

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if models.TextField in self.formfield_overrides:
            self.formfield_overrides[models.TextField]["widget"] = Textarea(attrs={'rows': self.TEXT_AREA_ROW, 'cols': self.TEXT_AREA_COLS})




class DisplayField(object):

    template_name = None
    css = {}
    js = []

    def __init__(self, field_name, short_description, help_text=None):
        self.field_name = field_name
        self.short_description = short_description
        self.help_text = help_text

    def __call__(self, obj):
        request = get_request()
        templates = self.get_templates(request, obj)
        context = self.get_context(request, obj)
        return render_to_string(templates, context)

    def get_templates(self, request, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        templates = [
            "admin/{}/{}/{}".format(app_label, model_name, self.template_name),
            "admin/{}/{}".format(app_label, self.template_name),
            "admin/{}".format(self.template_name),
        ]
        return templates

    def get_context(self, request, obj=None):
        add = request.path.endswith("/add/")
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        context = {
            "request": request,
            "obj": obj,
            "field_name": self.field_name,
            "short_description": self.short_description,
            "help_text": self.help_text,
            "add": add,
            "has_change_permission": request.has_change_permission,
            "value": getattr(obj, self.field_name),
        }
        return context

class WithDisplayFieldsMixin(MarkPermissionsMixin):

    def get_display_fields_map(self):
        fields_map = {}
        for name in dir(self):
            if name in ["media"]:
                continue
            field = getattr(self, name)
            if isinstance(field, DisplayField):
                fields_map[field.field_name] = name
        return fields_map

    def get_fieldsets(self, request, obj=None):
        fields_map = self.get_display_fields_map()
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = copy.deepcopy(fieldsets)
        if request.method != 'POST':
            for block in fieldsets:
                fields = listutils.replace(block[1]["fields"], fields_map)
                block[1]["fields"] = fields
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        fields_map = self.get_display_fields_map()
        fields = list(super().get_readonly_fields(request, obj))
        fields = copy.deepcopy(fields)
        for field_old, field_new in fields_map.items():
            if not field_new in fields:
                fields.append(field_new)
        return fields

    @property
    def media(self):
        resource = super().media
        fields_map = self.get_display_fields_map()
        for _, display_field_name in fields_map.items():
            field = getattr(self, display_field_name)
            resource += forms.Media(css=field.css, js=field.js)
        return resource
    

class HideShowField(DisplayField):
    template_name = "hide_show_field.html"
    css = {
        "all": [
            "fastadmin/admins/hide-show-field/hide-show-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/hide-show-field/hide-show-field.js",
    ])

class EditablePasswordField(DisplayField):

    template_name = "fastadmin/admins/editable-password-field/editable-password-field.html"
    css = {
        "all": [
            "fastadmin/admins/editable-password-field/editable-password-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/editable-password-field/editable-password-field.js",
    ])


class ResetToRandomPasswordField(object):

    template_name = "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.html"
    css = {
        "all": [
            "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.js",
    ])

    def __init__(self, field_name, get_password_url, short_description, help_text=None, params=None):
        super().__init__(field_name, short_description, help_text)
        self.get_password_url = get_password_url
        self.params = params

    def get_context(self, request, obj=None):
        context = super().get_context(request, obj)
        context.update({
            "get_password_url": reverse(self.get_password_url),
            "params": self.params,
            "params_json": json.dumps(self.params),
        })
        return context

class AddAdminViewHelper(admin.ModelAdmin):
    """With this extenstion, you can add an admin view by following simple code:
    ```
    extra_admin_views = [{
        "name": "admin_view_name_suffix",
        "view": "admin_view_function_name_or_function_itself",
        "url": "<path:object_id>/some-action-name/"
    }]  

    def admin_view_function_name_or_function_itself(self, request, object_id):
        pass
    ```                                                                                                                                                                                                                                                                11111111111111111111                
    """

    admin_site_namespace = "admin"

    def get_urls(self):
        urlpatterns = self.get_extra_admin_views()
        urlpatterns += super().get_urls()
        return urlpatterns

    def get_extra_admin_views(self):
        extra_admin_view_configs = self.get_extra_admin_view_configs()
        urlpatterns = []
        for admin_view_config in extra_admin_view_configs:
            urlpatterns.append(self.make_urlpattern(admin_view_config))
        return urlpatterns

    def get_extra_admin_view_configs(self):
        return getattr(self, "extra_admin_views", [])

    def admin_view_wrap(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        wrapper.model_admin = self
        return update_wrapper(wrapper, view)

    def get_admin_view_name(self, suffix):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return "{app_label}_{model_name}_{suffix}".format(app_label=app_label, model_name=model_name, suffix=suffix)

    def make_urlpattern(self, config):
        from django.urls import path

        name = config.get("name", None)
        view = config["view"]
        url = config["url"]

        if isinstance(view, str):
            view = getattr(self, view, None)
            if view is None:
                view = import_from_string(view)
        
        extra_params = {}
        if name:
            extra_params["name"] = name
        return path(url, self.admin_view_wrap(view), **extra_params)


class ToggleFieldStateAdmin(AddAdminViewHelper, admin.ModelAdmin):
    

    def get_toggle_field_state_view_name(self, field_name):
        return "toggle_" + field_name

    def get_extra_admin_view_configs(self):
        configs = super().get_extra_admin_view_configs()
        for field_name, field_config in self.get_toggle_field_state_configs().items():
            configs.append({
                "name": self.get_admin_view_name(self.get_toggle_field_state_view_name(field_name)),
                "view": self.toggle_field_state,
                "url": "<path:object_id>/toggle-field-state/<path:field_name>/",
            })
        return configs

    def toggle_field_state(self, request, object_id, field_name):
        obj = self.get_object(request, object_id)
        if self.has_toggle_field_state_permission(request, obj, field_name):
            method_name = "toggle_{0}_state".format(field_name)
            if hasattr(obj, method_name):
                getattr(obj, method_name)(request)
                obj.save()
            else:
                if getattr(obj, field_name, None):
                    setattr(obj, field_name, False)
                else:
                    setattr(obj, field_name, True)
                obj.save()
            messages.success(request, _("Toggle state success."))
        else:
            messages.error(request, _("You have NO permission to change the state of the instance."))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def has_toggle_field_state_permission(self, request, obj, field_name):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return request.user.has_perm("{app_label}.change_{model_name}".format(app_label=app_label, model_name=model_name))

    def get_toggle_field_state_configs(self):
        return getattr(self, "toggle_field_state_configs", {})

    def field_state(self, obj, field_name):
        return getattr(obj, field_name, None)

    @staticmethod
    def make_toggle_field_state_button(field_name_config_name):
        def toggle_field_state_button(self, obj):
            field_name = getattr(self, field_name_config_name, field_name_config_name)
            href = reverse("{namespace}:{view_name}".format(
                namespace=self.admin_site_namespace,
                view_name= self.get_admin_view_name(self.get_toggle_field_state_view_name(field_name))),
                args=[obj.pk, field_name],
            )
            button_config = self.get_toggle_field_state_configs()[field_name]
            if self.field_state(obj, field_name):
                icon = button_config.get("toggle_button_icon_state_on", "")
                title = button_config.get("toggle_button_title_turn_off", _("Turn Off"))
            else:
                icon = button_config.get("toggle_button_icon_state_off", "")
                title = button_config.get("toggle_button_title_turn_on", _("Turn On"))
            return {
                "href": href,
                "icon": icon,
                "title": title,
                "help_text": button_config.get("toggle_button_help_text", ""),
            }
        return toggle_field_state_button

class SimplePublishModelAdmin(ToggleFieldStateAdmin, admin.ModelAdmin):

    published_field_name = "published"

    toggle_publish_state_button_title_turn_on = _("Publish")
    toggle_publish_state_button_title_turn_off = _("Unpublish")
    toggle_publish_state_button_icon_state_on = "fa fa-eye"
    toggle_publish_state_button_icon_state_off = "fa fa-eye-slash"
    toggle_publish_state_button_help_text = _("Toggle item publish state.")

    def get_toggle_field_state_configs(self):
        configs = super().get_toggle_field_state_configs()
        configs[self.published_field_name] = {
            "toggle_button_title_turn_on": self.toggle_publish_state_button_title_turn_on,
            "toggle_button_title_turn_off": self.toggle_publish_state_button_title_turn_off,
            "toggle_button_icon_state_on": self.toggle_publish_state_button_icon_state_on,
            "toggle_button_icon_state_off": self.toggle_publish_state_button_icon_state_off,
            "toggle_button_help_text": self.toggle_publish_state_button_help_text,
        }
        return configs

    toggle_publish_state_button = ToggleFieldStateAdmin.make_toggle_field_state_button("published_field_name")


class SetTopModelAdmin(ToggleFieldStateAdmin, admin.ModelAdmin):

    is_top_field_name = "is_top"

    toggle_top_setting_button_title_turn_on = _("Set Top")
    toggle_top_setting_button_title_turn_off = _("Cancel Top")
    toggle_top_setting_button_icon_state_on = "fa fa-compress-arrows-alt"
    toggle_top_setting_button_icon_state_off = "fa fa-arrow-up"
    toggle_top_setting_button_help_text = _("Set item to display top or cancel the top setting.")

    def get_toggle_field_state_configs(self):
        configs = super().get_toggle_field_state_configs()
        configs[self.is_top_field_name] = {
            "toggle_button_title_turn_on": self.toggle_top_setting_button_title_turn_on,
            "toggle_button_title_turn_off": self.toggle_top_setting_button_title_turn_off,
            "toggle_button_icon_state_on": self.toggle_top_setting_button_icon_state_on,
            "toggle_button_icon_state_off": self.toggle_top_setting_button_icon_state_off,
            "toggle_button_help_text": self.toggle_top_setting_button_help_text,
        }
        return configs

    toggle_top_setting_button = ToggleFieldStateAdmin.make_toggle_field_state_button("is_top_field_name")
