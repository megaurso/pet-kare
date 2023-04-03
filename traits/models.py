from django.db import models

class Trait(models.Model):
    name = models.CharField(max_length=20)

    pets_Traints = models.ManyToManyField(
        "pets.Pet",
        related_name="traits",
    )
    
    def __repr__(self) -> str:
        return f"<Trait ({self.id} - {self.name})>"
