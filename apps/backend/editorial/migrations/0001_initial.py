from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("sites", "0001_initial")]
    operations = [migrations.CreateModel(name="EditorialGuideline", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("tone", models.TextField(default="Claro, profesional y accesible.")), ("audience", models.TextField(blank=True)), ("allowed_topics", models.JSONField(blank=True, default=list)), ("restricted_topics", models.JSONField(blank=True, default=list)), ("seo_requirements", models.JSONField(blank=True, default=list)), ("agent_instructions", models.TextField(blank=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("site", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="guidelines", to="sites.site"))])]
