from django.contrib import admin

from card.models import Card, Collection, Deck, Collec, UserProfile


class CardAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


class CollecAdmin(admin.ModelAdmin):
    pass


class DeckAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Card, CardAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Collec, CollecAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(UserProfile, UserProfileAdmin)