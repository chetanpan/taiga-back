# Copyright (C) 2015 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2015 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2015 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from rest_framework.serializers import ValidationError

from taiga.base.serializers import ModelSerializer
from taiga.base.serializers import JsonField

from . import models


######################################################
# Custom Attribute Serializer
#######################################################

class BaseCustomAttributeSerializer(ModelSerializer):
    def validate(self, data):
        """
        Check the name is not duplicated in the project. Check when:
          - create a new one
          - update the name
          - update the project (move to another project)
        """
        data_name = data.get("name", None)
        data_project = data.get("project", None)
        if self.object:
            data_name = data_name or self.object.name
            data_project = data_project or self.object.project

        model = self.Meta.model
        qs = model.objects.filter(project=data_project, name=data_name)
        if qs.exists():
            raise ValidationError(_("There is a custom field with the same name in this project."))

        return data


class UserStoryCustomAttributeSerializer(BaseCustomAttributeSerializer):
    class Meta:
        model = models.UserStoryCustomAttribute


class TaskCustomAttributeSerializer(BaseCustomAttributeSerializer):
    class Meta:
        model = models.TaskCustomAttribute


class IssueCustomAttributeSerializer(BaseCustomAttributeSerializer):
    class Meta:
        model = models.IssueCustomAttribute


######################################################
# Custom Attribute Serializer
#######################################################


class BaseCustomAttributesValuesSerializer:
    values = JsonField(source="values", label="values", required=True)

    def validate_values(self, attrs, source):
        data_values = attrs.get("values", None)
        data_project = attrs.get("project", None)

        if self.object:
            if self.object.values:
                data_values = (data_values or self.object.values)
            data_project = data_project or self.object.project_id

        if type(data_values) is not dict:
            raise ValidationError(_("Invalid content. It must be {\"key\": \"value\",...}"))

        values_ids = list(data_values.keys())
        qs = self._custom_attribute_model.objects.filter(project=data_project,
                                                         id__in=values_ids)
        if qs.count() != len(values_ids):
            raise ValidationError(_("It contain invalid custom fields."))

        return attrs

    def validate(self, attrs):
        attrs = super().validate(attrs)

        data_container = attrs.get(self._container_field, None)
        data_project = attrs.get("project", None)

        if data_container:
            data_container = data_container.id

        if data_project:
            data_project = data_project.id

        if self.object:
            data_container = data_container or getattr(self.object, "{}_id".format(self._container_field))
            data_project = data_project or self.object.project_id

        model = apps.get_model(self._container_model)
        if not model.objects.filter(project=data_project, id=data_container).exists():
            raise ValidationError(_("Different project value between the custom field values object and "
                                    "the container object."))

        return attrs


class UserStoryCustomAttributesValuesSerializer(BaseCustomAttributesValuesSerializer, ModelSerializer):
    _custom_attribute_model = models.UserStoryCustomAttribute
    _container_model = "userstories.UserStory"
    _container_field = "user_story"

    class Meta:
        model = models.UserStoryCustomAttributesValues


class TaskCustomAttributesValuesSerializer(BaseCustomAttributesValuesSerializer, ModelSerializer):
    _custom_attribute_model = models.TaskCustomAttribute
    _container_model = "tasks.Task"
    _container_field = "task"

    class Meta:
        model = models.TaskCustomAttributesValues


class IssueCustomAttributesValuesSerializer(BaseCustomAttributesValuesSerializer, ModelSerializer):
    _custom_attribute_model = models.IssueCustomAttribute
    _container_model = "issues.Issue"
    _container_field = "issue"

    class Meta:
        model = models.IssueCustomAttributesValues
