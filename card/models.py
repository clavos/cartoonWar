from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


class Card(models.Model):
    card_name = models.CharField(max_length=255)
    card_cout = models.IntegerField(default=0)
    card_ptattaque = models.IntegerField(default=0)
    card_ptvie = models.IntegerField(default=0)
    card_image = models.ImageField(blank=True, null=True, upload_to="covers/card/")
    collection = models.ForeignKey("Collection", blank=True, null=True, on_delete=models.DO_NOTHING)
    card_owners = models.ManyToManyField(User, related_name="cards", through="Collec")
    #cout_achat = models.IntegerField(default=0)
    #cout_vente = models.IntegerField(default=0)
    UNKNOWN = '-'
    MONSTRE = 'Monstre'
    SORT = 'Sort'
    TYPE_CARD_CHOICES = (
        (UNKNOWN, '-'),
        (MONSTRE, 'Monstre'),
        (SORT, 'Sort'),
    )
    card_type = models.CharField(max_length=10, choices=TYPE_CARD_CHOICES, default=UNKNOWN)

    def __str__(self):
        return self.card_name


class Collection(models.Model):
    collection_name = models.CharField(max_length=255)

    # collection_image =

    def __str__(self):
        return self.collection_name


class Collec(models.Model):
    current_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Deck(models.Model):
    deck_name = models.CharField(max_length=255)
    cards = models.ManyToManyField("Card", blank=True)
    gamer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='deck_owner')

    def __str__(self):
        return self.deck_name

    @classmethod
    def make_card(cls, current_deck, current_user, new_card):
        deck, created = cls.objects.get_or_create(
            gamer=current_user,
            deck_name=current_deck.deck_name
        )
        deck.cards.add(new_card)

    @classmethod
    def lose_card(cls, current_deck, current_user, new_card):
        deck, created = cls.objects.get_or_create(
            gamer=current_user,
            deck_name=current_deck.deck_name
        )
        deck.cards.remove(new_card)


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='', blank=True, null=True)
    # city = models.CharField(max_length=100, default='London', blank=True, null=True)
    phone = models.CharField(max_length=10,default='', blank=True, null=True)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    money = models.IntegerField(default=200)

    # london = UserProfileManager()

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        deck = Deck.objects.create(deck_name='Base', gamer=kwargs['instance'])
        #cards_list = list()
        for i in range (1,31):
            collection = Collec.objects.create(current_user=kwargs['instance'], quantity=1, cards=Card.objects.get(pk=i))
            deck.cards.add(Card.objects.get(pk=i))
        deck.save()




post_save.connect(create_profile, sender=User)
