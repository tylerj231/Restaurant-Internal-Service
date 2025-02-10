from django.contrib import admin

from app.models import (
    Vote,
    Restaurant,
    DailyMenu,
    MenuItem,
)

admin.site.register(Vote)
admin.site.register(Restaurant)
admin.site.register(DailyMenu)
admin.site.register(MenuItem)
