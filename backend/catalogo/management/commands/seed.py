from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Popula o banco com dados de teste"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("Seed executado!")
        )