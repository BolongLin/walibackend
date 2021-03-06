def _get_pusher():
    from django.conf import settings
    from django.utils.module_loading import import_string
    pusher_loader_dict = settings.PUSHER
    pusher_clz = pusher_loader_dict["clz"]
    pusher_kwargs = pusher_loader_dict.get("kwargs", {})
    return import_string(pusher_clz)(**pusher_kwargs)


default_pusher = _get_pusher()
