from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import random
import string


def rand_slug():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(3)])


class Category(models.Model):
    name = models.CharField('Категория', max_length=250, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category-list', args=[str(self.slug)])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название', max_length=250)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField('Изображение', upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[str(self.slug)])


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset for the ProductManager.

        Returns:
            QuerySet: The filtered queryset for available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()
    
    class Meta:
        proxy = True