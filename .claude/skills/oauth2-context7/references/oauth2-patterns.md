# OAuth 2.0 Common Patterns

Quick reference for common OAuth 2.0 and OpenID Connect patterns across languages.

## Table of Contents

1. [Authorization Code + PKCE (Python/authlib)](#authorization-code--pkce-pythonauthlib)
2. [Client Credentials (Python/authlib)](#client-credentials-pythonauthlib)
3. [JWT / JWK Validation](#jwt--jwk-validation)
4. [OpenID Connect](#openid-connect)
5. [Authorization Code + PKCE (JavaScript/oauth4webapi)](#authorization-code--pkce-javascriptoauth4webapi)
6. [Go oauth2](#go-oauth2)
7. [Flask/FastAPI Resource Server](#flaskfastapi-resource-server)
8. [Security Best Practices](#security-best-practices)

---

## Authorization Code + PKCE (Python/authlib)

### Flask Integration

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id='...',
    client_secret='...',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    token = github.authorize_access_token()
    user = github.get('user').json()
    return jsonify(user)
```

### httpx / requests (PKCE manual)

```python
import hashlib, base64, secrets
from authlib.integrations.httpx_client import OAuth2Client

# Generate PKCE
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

client = OAuth2Client(
    client_id='your-client-id',
    redirect_uri='https://yourapp.com/callback',
    code_challenge_method='S256',
)
uri, state = client.create_authorization_url(
    'https://provider.com/auth',
    code_challenge=code_challenge,
)
# Redirect user to `uri`

# After callback:
token = client.fetch_token(
    'https://provider.com/token',
    authorization_response=callback_url,
    code_verifier=code_verifier,
)
```

---

## Client Credentials (Python/authlib)

```python
from authlib.integrations.httpx_client import OAuth2Client

client = OAuth2Client(
    client_id='your-client-id',
    client_secret='your-client-secret',
)

token = client.fetch_token(
    'https://provider.com/token',
    grant_type='client_credentials',
    scope='read:data',
)

# Client automatically attaches Bearer token
resp = client.get('https://api.provider.com/data')
```

---

## JWT / JWK Validation

### Decode and Verify JWT (authlib)

```python
from authlib.jose import jwt, JsonWebKey

# Fetch JWKS from provider
import httpx
jwks = httpx.get('https://provider.com/.well-known/jwks.json').json()
key_set = JsonWebKey.import_key_set(jwks)

# Verify JWT
claims = jwt.decode(token, key_set)
claims.validate()  # validates exp, iat, nbf automatically

print(claims['sub'])  # user identifier
print(claims['email'])
```

### Create JWT (authlib)

```python
from authlib.jose import jwt
import time

header = {'alg': 'RS256'}
payload = {
    'sub': 'user-id-123',
    'iss': 'https://yourapp.com',
    'aud': 'https://api.yourapp.com',
    'exp': int(time.time()) + 3600,
    'iat': int(time.time()),
}

# Sign with private key
with open('private.pem', 'rb') as f:
    key = f.read()

token = jwt.encode(header, payload, key)
```

---

## OpenID Connect

### OIDC Discovery (authlib)

```python
from authlib.integrations.httpx_client import OAuth2Client
from authlib.oidc.discovery import get_well_known_url

# Auto-discover provider config
provider_url = 'https://accounts.google.com'
client = OAuth2Client(
    client_id='your-client-id',
    client_secret='your-client-secret',
    scope='openid email profile',
)

# Fetch OIDC metadata
metadata = httpx.get(get_well_known_url(provider_url)).json()
token_endpoint = metadata['token_endpoint']
authorization_endpoint = metadata['authorization_endpoint']
jwks_uri = metadata['jwks_uri']
```

### Validate ID Token (OIDC)

```python
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt

# After receiving id_token in token response
claims = jwt.decode(
    id_token,
    key_set,
    claims_cls=CodeIDToken,
)
claims.validate(
    nonce='the-nonce-you-sent',  # prevent replay attacks
)

user_id = claims['sub']
email = claims.get('email')
```

---

## Authorization Code + PKCE (JavaScript/oauth4webapi)

```typescript
import * as oauth from 'oauth4webapi'

const issuer = new URL('https://accounts.google.com')
const as = await oauth
  .discoveryRequest(issuer)
  .then((r) => oauth.processDiscoveryResponse(issuer, r))

const client: oauth.Client = { client_id: 'your-client-id' }

// Generate PKCE
const codeVerifier = oauth.generateRandomCodeVerifier()
const codeChallenge = await oauth.calculatePKCECodeChallenge(codeVerifier)
const state = oauth.generateRandomState()

// Build authorization URL
const authUrl = new URL(as.authorization_endpoint!)
authUrl.searchParams.set('client_id', client.client_id)
authUrl.searchParams.set('redirect_uri', 'https://yourapp.com/callback')
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('scope', 'openid email')
authUrl.searchParams.set('code_challenge', codeChallenge)
authUrl.searchParams.set('code_challenge_method', 'S256')
authUrl.searchParams.set('state', state)
// Redirect user to authUrl.href

// After callback:
const currentUrl = new URL(window.location.href)
const params = oauth.validateAuthResponse(as, client, currentUrl, state)

const response = await oauth.authorizationCodeGrantRequest(
  as, client, params,
  'https://yourapp.com/callback',
  codeVerifier,
)
const result = await oauth.processAuthorizationCodeResponse(as, client, response)
console.log(result.access_token)

// Validate ID token
const claims = oauth.getValidatedIdTokenClaims(result)
console.log(claims.sub)
```

### Refresh Token (oauth4webapi)

```typescript
const response = await oauth.refreshTokenGrantRequest(
  as, client, refreshToken,
  { clientSecret: 'your-secret' },
)
const result = await oauth.processRefreshTokenResponse(as, client, response)
console.log(result.access_token)
```

---

## Go oauth2

### Authorization Code Flow

```go
import "golang.org/x/oauth2"

conf := &oauth2.Config{
    ClientID:     "your-client-id",
    ClientSecret: "your-client-secret",
    Scopes:       []string{"openid", "email"},
    Endpoint: oauth2.Endpoint{
        AuthURL:  "https://provider.com/auth",
        TokenURL: "https://provider.com/token",
    },
    RedirectURL: "https://yourapp.com/callback",
}

// Generate state for CSRF protection
state := generateRandomState()

// Redirect user
url := conf.AuthCodeURL(state, oauth2.AccessTypeOffline)

// After callback - exchange code
token, err := conf.Exchange(ctx, code)
if err != nil {
    log.Fatal(err)
}

// Use token
client := conf.Client(ctx, token)
resp, err := client.Get("https://api.provider.com/userinfo")
```

### Client Credentials (Go)

```go
import "golang.org/x/oauth2/clientcredentials"

config := &clientcredentials.Config{
    ClientID:     "your-client-id",
    ClientSecret: "your-client-secret",
    TokenURL:     "https://provider.com/token",
    Scopes:       []string{"api:read"},
}

client := config.Client(ctx)
resp, err := client.Get("https://api.provider.com/data")
```

---

## Flask/FastAPI Resource Server

### FastAPI Bearer Token Validation

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.jose import jwt, JsonWebKey
import httpx

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://provider.com/auth",
    tokenUrl="https://provider.com/token",
)

async def get_jwks():
    r = await httpx.AsyncClient().get("https://provider.com/.well-known/jwks.json")
    return JsonWebKey.import_key_set(r.json())

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        jwks = await get_jwks()
        claims = jwt.decode(token, jwks)
        claims.validate()
        return claims
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/protected")
async def protected(user=Depends(get_current_user)):
    return {"user": user["sub"]}
```

---

## Security Best Practices

1. **Always use PKCE** for public clients (SPAs, mobile apps) - RFC 7636
2. **Validate state parameter** to prevent CSRF attacks
3. **Validate nonce** in ID tokens to prevent replay attacks
4. **Check token expiry** (`exp` claim) before using tokens
5. **Validate `iss` and `aud` claims** in JWT validation
6. **Use short-lived access tokens** (15min-1hr) + refresh tokens
7. **Rotate refresh tokens** on each use (RFC 6819)
8. **Store tokens securely** - never in localStorage for sensitive apps
9. **Use HTTPS only** for all OAuth endpoints
10. **Validate redirect_uri** strictly on the authorization server
