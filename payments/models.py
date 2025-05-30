from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()  # (rani jibna model mta3 user, li rah ya3mil login)

class Payment(models.Model):
    # (hadi les types de paiement li n9adro ndirou bihoum, wsh carte, edahabia, paypal...)
    PAYMENT_METHODS = [
        ('credit_card', _('Carte de Crédit')),
        ('edahabia', _('Edahabia')),
        ('cib', _('CIB')),
        ('paypal', _('PayPal')),
        ('bank_transfer', _('Virement Bancaire')),
    ]

    # (hadi les états li ykoun fihoum paiement: en attente, complet, échoué, etc.)
    PAYMENT_STATUSES = [
        ('pending', _('En attente')),
        ('completed', _('Complété')),
        ('failed', _('Échoué')),
        ('refunded', _('Remboursé')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # (ila tmas7 user, khaliha null)
        null=True,
        related_name='payments',
        verbose_name=_('utilisateur')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,  # (ki tmas7 course, null aussi)
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('cours')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],  # (makach paiement negatif ya kho)
        verbose_name=_('montant (DZD)')
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='credit_card',  # (par défaut rah carte de crédit)
        verbose_name=_('méthode de paiement')
    )
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUSES,
        default='pending',  # (kif ydir paiement ybda pending)
        verbose_name=_('statut')
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,  # (kul transaction fiha ID unique)
        blank=True,
        verbose_name=_('numéro de transaction')
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,  # (datetime automatiquement ki ydir paiement)
        verbose_name=_('date de paiement')
    )
    receipt_url = models.URLField(
        blank=True,
        verbose_name=_('lien de reçu')  # (lien ta3 reçu si disponible)
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('notes')  # (chwiya espace bach tdir des remarques)
    )

    class Meta:
        ordering = ['-payment_date']  # (trie les paiements men a9dam jdidan)
        verbose_name = _('paiement')
        verbose_name_plural = _('paiements')

    def __str__(self):
        return f"Paiement #{self.id} - {self.amount} DZD par {self.user}"

    def formatted_amount(self):  # (fonction bach ndir montant fi format mzyan)
        return f"{self.amount:,} DZD".replace(",", " ")  # (exemple: 15 000 DZD)

class SubscriptionPlan(models.Model):  # (hadi plans d’abonnement, ya3ni packs)
    PLAN_TYPES = [
        ('monthly', _('Mensuel')),
        ('annual', _('Annuel')),
        ('lifetime', _('À vie')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_('nom')
    )
    description = models.TextField(
        verbose_name=_('description')  # (chrah mta3 plan)
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('prix (DZD)')
    )
    duration_days = models.PositiveIntegerField(
        verbose_name=_('durée (jours)')  # (combien de jours ydoum)
    )
    plan_type = models.CharField(
        max_length=10,
        choices=PLAN_TYPES,
        verbose_name=_('type d\'abonnement')  # (mois, année, ou à vie)
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('actif')  # (ila plan actif wla la)
    )
    features = models.JSONField(
        default=list,
        verbose_name=_('caractéristiques')  # (liste des options li fih)
    )

    class Meta:
        verbose_name = _('plan d\'abonnement')
        verbose_name_plural = _('plans d\'abonnement')

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"

    def formatted_price(self):  # (format prix selon type de plan)
        return f"{self.price:,} DZD/mois".replace(",", " ") if self.plan_type == 'monthly' else f"{self.price:,} DZD".replace(",", " ")

class AlgerianCardPayment(models.Model):  # (paiement avec carte algérienne)
    CARD_TYPES = [
        ('visa', 'VISA'),
        ('mastercard', 'MasterCard'),
        ('cib', 'CIB'),
        ('badr', 'Banque Al Baraka'),
    ]



    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,  # (ila tmas7 paiement, tmas7 les détails aussi)
        related_name='card_details'
    )
    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPES
    )
    card_number = models.CharField(  # (numéro mta3 la carte, optionnel ici)
        max_length=16,
        blank=True
    )
    card_holder = models.CharField(  # (esm mta3 sahib carte)
        max_length=100
    )
    expiry_date = models.CharField(  # (date expiration format MM/YY)
        max_length=5,
        help_text="Format: MM/YY"
    )
    cvv = models.CharField(  # (code CVV mta3 sécurité)
        max_length=3
    )

    class Meta:
        verbose_name = _('paiement par carte algérienne')
        verbose_name_plural = _('paiements par carte algérienne')

    def __str__(self):
        return f"Paiement par carte {self.card_type} pour {self.payment}"

class EdahabiaPayment(models.Model):  # (paiement avec Edahabia, la carte postale)
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='edahabia_details'
    )
    phone_number = models.CharField(
        max_length=10,
        help_text="Numéro de téléphone Algérien (10 chiffres)"  # (ex: 0555xxxxxx)
    )
    transaction_code = models.CharField(
        max_length=100,
        blank=True  # (code li yji baed l'achat)
    )

    class Meta:
        verbose_name = _('paiement Edahabia')
        verbose_name_plural = _('paiements Edahabia')

    def __str__(self):
        return f"Paiement Edahabia ({self.phone_number}) pour {self.payment}"
