from django.db import models

class Bike(models.Model):
    class Category(models.TextChoices):
        ROAD = "road", "Шоссейный"
        MTB = "mtb", "Горный"
        CITY = "city", "Городской"
        ELECTRIC = "electric", "Электровелосипед"

    class Colour(models.TextChoices):
        RED = "red", "Красный"
        BLUE = "blue", "Синий"
        BLACK = "black", "Чёрный"
        WHITE = "white", "Белый"
        GREEN = "green", "Зелёный"

    class Brand(models.TextChoices):
        TREK = "trek", "Trek"
        GIANT = "giant", "Giant"
        SPECIALIZED = "specialized", "Specialized"
        CUBE = "cube", "Cube"
        AUTHOR = "author", "Author"

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        blank=True,
        null=True,
        verbose_name="Category",
    )

    brand = models.CharField(
        max_length=50,
        choices=Brand.choices,
        verbose_name="Bike Brand"
    )

    colour = models.CharField(
        max_length=20,
        choices=Colour.choices,
        verbose_name="Colour",
        default='black',
    )

    name = models.CharField(max_length=1024, blank=True, null=True)
    electricity = models.BooleanField(default=False, help_text="Есть ли у него педали")
    available = models.BooleanField(default=True)
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bike History",
        help_text="Тут мы храним всю историю о велосипеде и его обслуживании",
    )
    preview = models.FileField(upload_to="bike/preview", blank=True, null=True)
    station = models.ForeignKey(
        "bike.Station",
        on_delete=models.PROTECT,
        related_name="bikes"
    )

    class Meta:
        verbose_name = "Bicycle"
        verbose_name_plural = "Bicycles"

    def __str__(self):
        return f"Bike name {self.name or 'No name'}"

    def get_category_display(self):
        if not self.category:
            return "Не указана"
        return self.Category(self.category).label

    def get_brand_display(self):
        if not self.brand:
            return "Не указана"
        return self.Brand(self.brand).label

    def get_colour_display(self):
        if not self.colour:
            return "Не указан"
        return self.Colour(self.colour).label


class Station(models.Model):
    name = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    capacity = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'

    def __str__(self):
        return f"Station {self.name} - ({self.address})"