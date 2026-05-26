from apps.core.models.person import Person


class Seller(Person):

    class Meta:
        db_table = "sellers"
        ordering = ["-created_at"]
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
