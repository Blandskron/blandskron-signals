from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Trend", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=160)), ("slug", models.SlugField(unique=True)), ("category", models.CharField(choices=[("artificial_intelligence", "Artificial Intelligence"), ("development", "Development"), ("automation", "Automation"), ("infrastructure", "Infrastructure"), ("cybersecurity", "Cybersecurity"), ("business", "Business"), ("open_source", "Open Source"), ("user_experience", "User Experience")], max_length=32)), ("description", models.TextField()), ("state", models.CharField(choices=[("detected", "Detected"), ("emerging", "Emerging"), ("growing", "Growing"), ("mainstream", "Mainstream"), ("declining", "Declining"), ("watching", "Watching")], default="detected", max_length=20)), ("impact_level", models.PositiveSmallIntegerField(default=0)), ("maturity_level", models.PositiveSmallIntegerField(default=0)), ("detected_at", models.DateField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True))])]
