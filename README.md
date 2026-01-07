# 📍 Google Maps Lead Generator (No-Install)

A.K.A - Simple Google Maps Scraper

A lightweight, professional Python tool designed for startups to extract high-quality B2B leads from dense urban areas.

Get thousands of leads for free using Google Maps! (check disclaimer)

### Why use this?
* **Zero Dependencies:** Runs on standard Python. No `pip install` required.
* **Deep Extraction:** Uses a recursive algorithm to bypass the Google 60-result limit in crowded cities.
* **Budget Friendly:** Built-in budget controls to keep your API costs predictable.
* **Simple:** The tool is designed to be simple and easy to utilise

### 💡 The Value Proposition

#### One of the most cost-effective comprehensive solutions for extracting leads from google maps in densely populated areas.

Unlike traditional scrapers that use expensive proxies or hit the 60-result ceiling, this tool uses an API-first Recursive algorithm. It ensures 100% area coverage while minimizing API costs.

---

## 🚀 Quick Start

1. **Get your API Key:** Grab a **Google Places** api key from the [Google Cloud Console](https://console.cloud.google.com/).
2. **Set your Key:**
   ```bash
   export GOOGLE_MAPS_KEY='your_api_key_here'
   ```
3. **Configure Search:** Open `config.json` set you search term and the coordinates of the region you want to search (search region is a rectangle with low/high set points)
4. **Run:** 
   ```bash
   python3 main.py
   ```
Your leads will appear as CSV files in the `/outputs` folder, ready for your CRM or cold outreach.

---

🛠 How it Works: The "Dense Search" Engine

Most tools miss 70% of leads in cities because Google only returns 60 results at a time. This tool solves that:
1. **Grid Partitioning:** It divides your target area into 1-mile squares.
2. **Recursive Splitting:** If a square is "too full" (60+ leads), the tool automatically splits that square into 4 smaller quadrants and searches again.
3. **Deduplication:** Automatically removes duplicate entries found in overlapping zones.

---

📊 Config

```json
{
    "search_term": "vintage boutique",
    "budget": 1000,
    "enterprise_plan": true,
    "output_directory": "outputs",
    "coordinates": {
        "high": {
            "latitude": 40.7831, 
            "longitude": -73.9439
        },
        "low": {
            "latitude": 40.7019, 
            "longitude": -74.0170
        }
    }
}
```

---

## 🛡 Security & Ethics

- **API Security:** This tool uses environment variables for keys. Never hardcode your key in the script.
- **Usage:** Intended for legitimate B2B lead generation. Please respect Google's Terms of Service.


---

## ⚖️  Disclaimer & Liability

**Important:** This tool interacts with the Google Places API which is a paid service. 

* **Costs:** The developer(s) of this tool is NOT responsible for any costs incurred through your use of the Google Cloud Platform. Always monitor your usage and set billing alerts in the Google Cloud Console.
* **Terms of Service:** You are responsible for ensuring that your use of this data complies with Google's Terms of Service and local data protection laws (e.g., GDPR, CCPA).
* **As-Is:** This software is provided "as is", without warranty of any kind. In no event shall the authors be liable for any claim, damages, or other liability.

