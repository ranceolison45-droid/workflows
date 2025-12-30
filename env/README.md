# Environment Variables

This folder contains environment variable configurations for different deployment environments.

## Files

- `.env.production` - Production environment variables for live deployment
- `.env.development` - Development environment variables for local development
- `.env.example` - Template for creating your own environment files

## Usage

### For Local Development

1. Copy the example file:
   ```bash
   cp env/.env.example .env
   ```

2. Edit `.env` with your actual credentials

3. Python will automatically load `.env` when using `python-dotenv`

### For Netlify Deployment

1. Go to your Netlify dashboard
2. Navigate to: **Site settings** → **Build & deploy** → **Environment**
3. Add environment variables from `.env.production`
4. Replace placeholder values with your actual credentials

### Important Security Notes

⚠️ **NEVER commit `.env` files to git!**

- All `.env` files are automatically ignored by `.gitignore`
- Only commit `.env.example` files
- Keep sensitive credentials secure
- Use different keys for development and production

## Environment Variables Reference

### Required Variables

- `SECRET_KEY` - Flask secret key for session management
- `DATABASE_URL` - Database connection string

### Optional but Recommended

- `OPENAI_API_KEY` - For AI chat features
- `ANTHROPIC_API_KEY` - For Claude AI features
- `GOOGLE_API_KEY` - For Google AI features
- `STRIPE_SECRET_KEY` - For payment processing
- `TWILIO_*` - For SMS messaging
- `SMTP_*` - For email notifications

## Generate a Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as your `SECRET_KEY`.
