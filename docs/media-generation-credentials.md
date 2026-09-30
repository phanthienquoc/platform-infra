# media-generation credential checklist

Runtime secrets must never be committed to Git or stored as plaintext in Supabase.

## Generation
- Gemini API credential for Gemini/Veo generation.
- Supabase URL.
- Supabase service-role credential for backend-only DB/storage operations.
- Supabase storage bucket configuration. The production runtime uses `media-generation`.

## YouTube Shorts
- Google Cloud OAuth client ID.
- Google Cloud OAuth client secret.
- YouTube channel authorization with the required YouTube Data API scope.
- OAuth refresh token stored only in the runtime secret mechanism; DB stores a secret reference.

Suggested environment variables:

```text
GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
MEDIA_STORAGE_BUCKET=media-generation
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN_SECRET_REF=
```

The current media-generation runtime only requires the Generation credentials above. YouTube credentials are optional until the Shorts publishing integration is enabled.

GitHub Actions/GHCR and GitOps promotion credentials must remain in GitHub secrets/variables or the existing platform mechanism, never source.
