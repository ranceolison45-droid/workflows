# How to Get Your Google Maps API Key

## Step-by-Step Instructions

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2. Create or Select a Project
- Click on the project dropdown at the top
- Click **"New Project"**
- Enter project name: `StormBuster` (or your preferred name)
- Click **"Create"**

### 3. Enable the Maps API
1. Go to: https://console.cloud.google.com/apis/library
2. Search for **"Maps JavaScript API"**
3. Click on it and press **"Enable"**
4. Also enable:
   - **Geocoding API** (for address lookups)
   - **Maps Static API** (for static map images)
   - **Places API** (if you need location searches)

### 4. Create API Key
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"API key"**
4. Your API key will be generated

### 5. Restrict Your API Key (IMPORTANT for Security)
1. Click **"Restrict Key"** in the dialog
2. Or go back to credentials and click the API key name
3. Under **"Application restrictions"**:
   - Select **"HTTP referrers (web sites)"**
   - Add your domains:
     - `https://stormgods.us/*`
     - `https://*.stormgods.us/*`
     - For development: `http://localhost:5000/*`
     - For development: `http://127.0.0.1:5000/*`
4. Under **"API restrictions"**:
   - Select **"Restrict key"**
   - Select only the APIs you enabled:
     - Maps JavaScript API
     - Geocoding API
     - Maps Static API
     - Places API (if enabled)
5. Click **"Save"**

### 6. Add to Your Environment Variables

**For Netlify:**
- Variable name: `GOOGLE_API_KEY`
- Variable value: `your_api_key_here`

**For Local Development:**
Add to your `.env` file:
```bash
GOOGLE_API_KEY=your_api_key_here
```

---

## Quick API Key URLs

- **Create Credentials**: https://console.cloud.google.com/apis/credentials
- **Enable APIs**: https://console.cloud.google.com/apis/library
- **Billing**: https://console.cloud.google.com/billing

---

## Important Notes

### Free Tier Limits
Google Maps API has a free tier that includes:
- $200 credit per month (free)
- After that, pay-as-you-go pricing

### Setup Billing (Required)
⚠️ **You MUST enable billing to use the API:**
1. Go to: https://console.cloud.google.com/billing
2. Link a billing account
3. Google gives you $200/month free credit

### Security Tips
- ✅ Always restrict your API key to specific domains
- ✅ Enable only the APIs you need
- ✅ Set up quota limits in Cloud Console
- ✅ Monitor usage in Google Cloud Console

---

## Testing Your API Key

Once you have your key, you can test it:

```bash
# Test in browser console or Python
import requests

api_key = "YOUR_API_KEY"
url = f"https://maps.googleapis.com/maps/api/geocode/json?address=Dallas,TX&key={api_key}"
response = requests.get(url)
print(response.json())
```

---

## Your API Key Format
Google Maps API keys typically look like:
```
AIzaSyD...
```

Copy the full key (it's long, about 39+ characters).

---

## Need Help?
- Google Maps Documentation: https://developers.google.com/maps
- API Restrictions Guide: https://developers.google.com/maps/api-security-best-practices
- Support: https://console.cloud.google.com/support


