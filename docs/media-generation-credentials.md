# media-generation credential checklist

Runtime secrets must never be committed to Git or stored as plaintext in Supabase.

## Generation
- Gemini API credential for Gemini/Veo generation.
- Supabase URL.
- Supabase service-role credential for backend-only DB/storage operations.
- Supabase storage bucket configuration.

## YouTube Shorts
- Google Cloud OAuth client ID.
- Google Cloud OAuth client secret.
- YouTube channel authorization with the required YouTube Data API scope.
- OAuth refresh token stored only in the runtime secret mechanism; DB stores a secret reference.

Suggested environment variables:

GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
MEDIA_STORAGE_BUCKET=media-assets
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN_SECRET_REF=

GitHub Actions/GHCR and GitOps promotion credentials must remain in GitHub secrets/variables or the existing platform mechanism, never source.