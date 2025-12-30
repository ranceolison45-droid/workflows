# Free Map API Alternatives

Looking for free mapping services? Here are the best options:

---

## 🗺️ Top Free Map API Services

### 1. **Mapbox** (Highly Recommended)
- **Free Tier**: 50,000 map loads/month
- **API**: Mapbox GL JS, Static Images API
- **Get Key**: https://account.mapbox.com/access-tokens/
- **Documentation**: https://docs.mapbox.com/

**Features:**
- ✅ Beautiful custom styling
- ✅ High-quality satellite imagery
- ✅ Easy to use
- ✅ 50K free loads/month

**Cost after free tier**: $5 per 1,000 additional loads

---

### 2. **Leaflet.js** (100% Free)
- **Free Tier**: Unlimited
- **API**: Open-source JavaScript library
- **Tiles**: OpenStreetMap (free tiles)
- **Get Started**: https://leafletjs.com/

**Features:**
- ✅ Completely free, no API key needed
- ✅ Open source
- ✅ Very lightweight
- ✅ Works with OpenStreetMap data

**Example Usage:**
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

---

### 3. **OpenStreetMap (OSM)** (100% Free)
- **Free Tier**: Unlimited
- **Data**: Community-driven mapping
- **Get Started**: https://www.openstreetmap.org/

**Features:**
- ✅ Completely free and open-source
- ✅ No API key required
- ✅ Good coverage worldwide
- ✅ Free geocoding via Nominatim

**Geocoding API (Free):**
```
https://nominatim.openstreetmap.org/search?q=Dallas,TX&format=json
```

---

### 4. **Here Maps** (Limited Free Tier)
- **Free Tier**: 50,000 transactions/month
- **Get Key**: https://developer.here.com/
- **Documentation**: https://developer.here.com/documentation

**Features:**
- ✅ 50K free transactions
- ✅ Good international coverage
- ✅ Geocoding and routing

---

### 5. **MapQuest** (Limited Free Tier)
- **Free Tier**: 15,000 requests/month
- **Get Key**: https://developer.mapquest.com/plan_purchase/choose_plan/individual
- **Documentation**: https://developer.mapquest.com/documentation/

**Features:**
- ✅ 15K free requests/month
- ✅ Geocoding, routing, static maps

---

### 6. **ArcGIS** (Esri)
- **Free Tier**: Limited free access
- **Get Key**: https://developers.arcgis.com/
- **Documentation**: https://developers.arcgis.com/documentation/

**Features:**
- ✅ Professional-grade mapping
- ✅ Good for specialized use cases
- ⚠️ More complex setup

---

## 📊 Comparison Table

| Service | Free Tier | API Key Needed | Best For |
|---------|-----------|----------------|----------|
| **Leaflet.js** | Unlimited | ❌ No | Simple maps, small projects |
| **OpenStreetMap** | Unlimited | ❌ No | Completely free, open-source |
| **Mapbox** | 50K loads | ✅ Yes | Production apps, quality |
| **Here Maps** | 50K requests | ✅ Yes | International coverage |
| **MapQuest** | 15K requests | ✅ Yes | Basic mapping needs |
| **ArcGIS** | Limited | ✅ Yes | Professional GIS |
| **Google Maps** | $200 credit | ✅ Yes | Most features |

---

## 🎯 Recommendations for Your Project

### **For Development & Testing:**
**Use Leaflet.js** - It's completely free, no API key needed!

```javascript
// Example with Leaflet
var map = L.map('mapid').setView([32.7767, -96.7970], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);
```

### **For Production (Your StormBuster Site):**
**Use Mapbox** - Best balance of quality and free tier

**Benefits for your use case:**
- 50,000 map loads/month free (plenty for starting)
- Beautiful visualizations for hail events
- Great performance
- Easy to style for weather/storm data
- Professional appearance

---

## 🚀 Quick Setup: Leaflet.js (Free Forever)

### 1. Add to your HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map { height: 400px; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([32.7767, -96.7970], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        // Add markers for hail events
        L.marker([32.7767, -96.7970]).addTo(map).bindPopup('Dallas Hail Event');
    </script>
</body>
</html>
```

### 2. No API key needed - it just works! ✨

---

## 🔑 Quick Setup: Mapbox (Best Production Option)

### 1. Get Free API Key:
1. Go to: https://account.mapbox.com/access-tokens/
2. Sign up (free)
3. Copy your access token

### 2. Add to HTML:

```html
<script src='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css' rel='stylesheet' />

<script>
    mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [-96.7970, 32.7767],
        zoom: 10
    });
</script>
```

### 3. Add Token to Environment:
```bash
MAPBOX_TOKEN=your_token_here
```

---

## 🌐 Geocoding (Address to Coordinates) - FREE Options

### OpenStreetMap Nominatim (Free)
```
https://nominatim.openstreetmap.org/search?q=Dallas,TX&format=json&limit=1
```

### Mapbox Geocoding (Free with token)
```
https://api.mapbox.com/geocoding/v5/mapbox.places/Dallas,TX.json?access_token=YOUR_TOKEN
```

---

## 💡 Recommendation for StormBuster

**Start with Leaflet.js** (free, no signup):
- Perfect for development
- No API keys to manage
- Quick to implement
- Switch to Mapbox later if you need more features

**When you need more:**
- Upgrade to **Mapbox** for production
- Still get 50K free loads/month
- More styling options
- Better performance

---

## 📝 Update Your Environment Variables

Add this to your environment files:

**For Leaflet (No API key needed):**
```bash
MAP_PROVIDER=leaflet
```

**For Mapbox:**
```bash
MAP_PROVIDER=mapbox
MAPBOX_TOKEN=your_token_here
```

---

## 🛠️ Need Help?

- **Leaflet.js Docs**: https://leafletjs.com/examples.html
- **Mapbox Docs**: https://docs.mapbox.com/
- **OpenStreetMap**: https://www.openstreetmap.org/

---

**Bottom Line:** Start with Leaflet.js - it's free forever, no signup needed! 🎉


