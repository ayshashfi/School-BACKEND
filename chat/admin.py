from django.contrib import admin
from chat.models import Messages,ChatRooms
# Register your models here.
admin.site.register(ChatRooms)
admin.site.register(Messages)