def check_active_sidebar_links(request):
    try:
        current_url = request.resolver_match.url_name
    except Exception:
        current_url = "dashboard"

    print(current_url)

    services_urls_status = False
    # skills_urls_status = False
    # clients_urls_status = False
    # workers_url_status = False
    # jobs_url_status = False
    # queries_url_status = False

    context = {
        'current_url': current_url,
    }
    return context