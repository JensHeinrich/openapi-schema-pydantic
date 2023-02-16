from typing import Optional, Union

from pydantic import AnyUrl, BaseModel, Extra, Field

from ._config import DefaultConfig
from .oauth_flows import OAuthFlows


class SecurityScheme(BaseModel):
    """
    Defines a security scheme that can be used by the operations.

    Supported schemes are HTTP authentication,
    an API key (either as a header, a cookie parameter or as a query parameter),
    mutual TLS (use of a client certificate),
    OAuth2's common flows (implicit, password, client credentials and authorization code)
    as defined in [RFC6749](https://tools.ietf.org/html/rfc6749),
    and [OpenID Connect Discovery](https://tools.ietf.org/html/draft-ietf-oauth-discovery-06).

    Please note that as of 2020, the implicit flow is about to be deprecated by
    [OAuth 2.0 Security Best Current Practice](https://tools.ietf.org/html/draft-ietf-oauth-security-topics).
    Recommended for most use case is Authorization Code Grant flow with PKCE.
    """

    type: str = ...
    """
    **REQUIRED**. The type of the security scheme.
    Valid values are `"apiKey"`, `"http"`, "mutualTLS", `"oauth2"`, `"openIdConnect"`.
    """

    description: Optional[str] = None
    """
    A description for security scheme.
    [CommonMark syntax](https://spec.commonmark.org/) MAY be used for rich text representation.
    """

    name: Optional[str] = None
    """
    **REQUIRED** for `apiKey`. The name of the header, query or cookie parameter to be used.
    """

    security_scheme_in: Optional[str] = Field(alias="in", default=None)
    """
    **REQUIRED** for `apiKey`. The location of the API key. Valid values are `"query"`, `"header"` or `"cookie"`.
    """

    scheme: Optional[str] = None
    """
    **REQUIRED** for `http`. The name of the HTTP Authorization scheme to be used in the
    [Authorization header as defined in RFC7235](https://tools.ietf.org/html/rfc7235#section-5.1).
    
    The values used SHOULD be registered in the
    [IANA Authentication Scheme registry](https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml).
    """

    bearerFormat: Optional[str] = None
    """
    A hint to the client to identify how the bearer token is formatted.
    
    Bearer tokens are usually generated by an authorization server,
    so this information is primarily for documentation purposes.
    """

    flows: Optional[OAuthFlows] = None
    """
    **REQUIRED** for `oauth2`. An object containing configuration information for the flow types supported.
    """

    openIdConnectUrl: Optional[Union[AnyUrl, str]] = None
    """
    **REQUIRED** for `openIdConnect`. OpenId Connect URL to discover OAuth2 configuration values.
    This MUST be in the form of a URL. The OpenID Connect standard requires the use of TLS.
    """

    class Config(DefaultConfig):
        allow_population_by_field_name = True
        schema_extra = {
            "examples": [
                {"type": "http", "scheme": "basic"},
                {"type": "apiKey", "name": "api_key", "in": "header"},
                {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                {
                    "type": "oauth2",
                    "flows": {
                        "implicit": {
                            "authorizationUrl": "https://example.com/api/oauth/dialog",
                            "scopes": {"write:pets": "modify pets in your account", "read:pets": "read your pets"},
                        }
                    },
                },
                {"type": "openIdConnect", "openIdConnectUrl": "https://example.com/openIdConnect"},
                {"type": "openIdConnect", "openIdConnectUrl": "openIdConnect"},  # issue #5: allow relative path
            ]
        }
