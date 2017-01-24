from probe.models import Settings


def is_first_run():
    if len(list(Settings.objects.all())) == 0:
        return True
    return False


def use_prtg():
    k = Settings.objects.first()
    if k and k.prtg_url and k.prtg_token:
        return True
    return False
