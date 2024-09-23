from django.db import models
from traitlets import default

from goods.models import Products
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    """Описание самого заказа."""
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.SET_DEFAULT,
        default=None
    )
    created_timestamp = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20
    )
    requires_delivery = models.BooleanField(
        verbose_name='Требуется доставка',
        default=False
    )
    delivery_address = models.TextField(
        verbose_name='Адрес доставки',
        null=True,
        blank=True
    )
    payment_on_get = models.BooleanField(
        verbose_name='Оплата при получении',
        default=False
    )
    is_paid = models.BooleanField(
        verbose_name='Оплачено',
        default=False
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        default='В обработке',
        max_length=50
    )

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('id', )

    def __str__(self) -> str:
        return (f'Заказ № {self.pk} | '
                f'Покупатель {self.user.first_name} {self.user.last_name}')
    

class OrderItem(models.Model):
    """Товаров, которые заказал пользователь."""
    order = models.ForeignKey(
        to=Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Products,
        verbose_name='Продукт',
        on_delete=models.SET_DEFAULT,
        null=True, default=None
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=150
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=7,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )
    created_timestamp = models.DateTimeField(
        verbose_name='Дата продажи', 
        auto_now_add=True
    )

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'
        ordering = ('id', )

    objects = OrderitemQueryset.as_manager()

    def product_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self) -> str:
        return f'Товар {self.name} | Заказ № {self.order.pk}'