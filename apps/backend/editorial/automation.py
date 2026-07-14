from contextlib import contextmanager

from audit.models import AutomationRun
from django.utils import timezone


@contextmanager
def tracked_run(job_name):
    run = AutomationRun.objects.create(job_name=job_name)
    try:
        yield run
    except Exception as exc:  # noqa: BLE001
        run.state = "failed"
        run.error_message = str(exc)[:2000]
        run.finished_at = timezone.now()
        run.save(update_fields=["state", "error_message", "finished_at"])
        raise
    else:
        run.state = "completed"
        run.finished_at = timezone.now()
        run.save(update_fields=["state", "finished_at", "items_created", "metadata"])
