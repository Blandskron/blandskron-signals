from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Site", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120)), ("domain", models.CharField(max_length=255, unique=True)), ("slug", models.SlugField(unique=True)), ("is_active", models.BooleanField(default=True)), ("editorial_language", models.CharField(default="es", max_length=10)), ("timezone", models.CharField(default="America/Santiago", max_length=64))], options={"ordering": ["name"]})]
