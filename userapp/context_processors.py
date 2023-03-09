from userapp.models import Service


def get_services(request):
    services = Service.objects.all()
    return {'services': services}


def check_active_navitem(request):
    try:
        current_url = request.resolver_match.url_name
    except Exception:
        current_url = "index"

    print(current_url)