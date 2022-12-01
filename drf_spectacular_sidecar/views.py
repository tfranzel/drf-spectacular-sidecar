from django.templatetags.static import static
from django.views.generic import RedirectView


class SwaggerOauthRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return static("drf_spectacular_sidecar/swagger-ui-dist/oauth2-redirect.html") + f"?{self.request.GET.urlencode()}"
