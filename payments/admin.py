from django.contrib import admin
from .models import Payment, SubscriptionPlan, AlgerianCardPayment, EdahabiaPayment

# (hadi l'admin ta3 les paiements)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'formatted_amount', 'payment_method', 'status', 'payment_date')  # (li yban fi liste)
    list_filter = ('status', 'payment_method', 'payment_date')  # (bach t9dar tfiltri l’admin)
    search_fields = ('user__username', 'course__title', 'transaction_id')  # (t9dar tchercher b username, titre, transaction)
    readonly_fields = ('payment_date',)  # (date makach t9der tbdelha men admin)

    def formatted_amount(self, obj):  # (hadi taffichi l’montant formaté)
        return obj.formatted_amount()
    formatted_amount.short_description = 'Montant'  # (titre li ybda fi admin)

# (admin ta3 les paiements par carte dziriya)
@admin.register(AlgerianCardPayment)
class AlgerianCardPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'card_type', 'card_holder', 'expiry_date')  # (chouf chkon daba w ash men carte)
    list_filter = ('card_type',)  # (filter 3la type de carte)

# (admin ta3 les paiements Edahabia)
@admin.register(EdahabiaPayment)
class EdahabiaPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'phone_number', 'transaction_code')  # (chouf numéro w code transaction)
    search_fields = ('phone_number', 'transaction_code')  # (tqder tchercher par numéro ou code)
