import base64

from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'PUT':
            name = f'{user}.'
        elif self.context['request'].method == 'POST':
            name = f'{user}-{timezone.now()}.'
        else:
            recipe_id = self.context['request'].path.split('/')[-2]
            name = f'{user}-{recipe_id}.'
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=name + file_extension
            )
        return super().to_internal_value(data)
