from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Source", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=300)), ("url", models.URLField()), ("publisher", models.CharField(max_length=200)), ("author", models.CharField(blank=True, max_length=200)), ("published_at", models.DateField(blank=True, null=True)), ("consulted_at", models.DateField(auto_now_add=True)), ("source_type", models.CharField(choices=[("official", "Official"), ("documentation", "Documentation"), ("research", "Research"), ("news", "News"), ("analysis", "Analysis"), ("community", "Community"), ("social", "Social")], max_length=32)), ("confidence_note", models.TextField(blank=True)), ("usage_note", models.TextField(blank=True))], options={"ordering": ["-consulted_at", "title"]})]
