from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("audit", "0001_initial")]
    operations = [migrations.CreateModel(name="AutomationRun", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("job_name", models.CharField(max_length=100)), ("state", models.CharField(choices=[("running", "Running"), ("completed", "Completed"), ("failed", "Failed")], default="running", max_length=20)), ("started_at", models.DateTimeField(auto_now_add=True)), ("finished_at", models.DateTimeField(blank=True, null=True)), ("items_created", models.PositiveIntegerField(default=0)), ("error_message", models.TextField(blank=True)), ("metadata", models.JSONField(blank=True, default=dict))], options={"ordering": ["-started_at"]})]
