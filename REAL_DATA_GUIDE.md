# 🌐 Real Football Data Integration Guide

This guide shows you how to replace the simulated data with **real football match data** from live APIs.

---

## 📊 Available Data Sources

### 1. **Football-Data.org** (Recommended - FREE)

✅ **Best for beginners**
- ✅ Free tier available (10 requests/minute)
- ✅ Covers major European leagues
- ✅ Historical data available
- ✅ Easy to use API
- ✅ No credit card required

**Get Started:**
1. Visit: https://www.football-data.org/client/register
2. Register for FREE
3. Verify your email
4. Copy your API key from the dashboard

**Leagues Available:**
- Premier League (England)
- La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)
- And more...

---

### 2. **API-Football** (RapidAPI)

⚡ **Most comprehensive**
- ✅ 100+ leagues worldwide
- ✅ Live scores
- ✅ Detailed statistics
- ✅ Player data
- ❌ Paid (free tier very limited)

**Get Started:**
1. Visit: https://rapidapi.com/api-sports/api/api-football
2. Sign up for RapidAPI
3. Subscribe to API-Football (free tier: 100 requests/day)
4. Copy your RapidAPI key

---

### 3. **TheSportsDB** (Alternative - FREE)

✅ **Good alternative**
- ✅ Completely free
- ✅ No API key needed
- ✅ Multiple sports
- ❌ Less detailed than others

---

## 🚀 Quick Start: Import Real Data

### **Option 1: Using Football-Data.org (Recommended)**

#### Step 1: Install requests library
```bash
pip install requests
```

#### Step 2: Get your FREE API key
1. Go to: https://www.football-data.org/client/register
2. Fill in the registration form
3. Verify your email
4. Login and copy your API key

#### Step 3: Run the import script
```bash
python scripts/import_real_data.py
```

Follow the prompts:
- Choose option **2** (with API key)
- Paste your API key
- Confirm to import

**What happens:**
- Fetches last 30 days + next 30 days of matches
- Imports from all 5 major leagues
- Creates teams automatically
- Updates your database with real data

---

### **Option 2: Without API Key (Limited)**

You can try without an API key, but you'll hit rate limits quickly:

```bash
python scripts/import_real_data.py
```

Choose option **1** (no key)

**Limitations:**
- Only 10 requests per minute
- May not fetch all data
- Slower import process

---

## 📝 Manual Integration (Advanced)

If you want more control, here's how to integrate manually:

### Example: Fetch Premier League Matches

```python
from services.api_service import FootballAPIService

# Initialize with your API key
api = FootballAPIService(api_key="YOUR_API_KEY_HERE")

# Fetch Premier League matches
matches = api.fetch_matches_football_data_org(
    competition_code="PL",
    date_from="2024-01-01",
    date_to="2024-12-31"
)

# Process matches
for match in matches:
    parsed = api.parse_football_data_org_match(match)
    print(f"{parsed['home_team']} vs {parsed['away_team']}")
```

---

## 🔄 Updating Data Regularly

### Option 1: Manual Updates

Run the import script whenever you want fresh data:

```bash
python scripts/import_real_data.py
```

### Option 2: Scheduled Updates (Advanced)

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 6 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `scripts/import_real_data.py`
7. Start in: Your project directory

**macOS/Linux (Cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 6 AM)
0 6 * * * cd /path/to/football-prediction && python3 scripts/import_real_data.py
```

---

## 🎯 API Comparison

| Feature | Football-Data.org | API-Football | TheSportsDB |
|---------|------------------|--------------|-------------|
| **Cost** | FREE | Paid (limited free) | FREE |
| **API Key** | Required | Required | Optional |
| **Rate Limit** | 10 req/min | 100 req/day (free) | Unlimited |
| **Leagues** | 10+ major | 100+ | 50+ |
| **Historical Data** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Live Scores** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Statistics** | ✅ Basic | ✅ Detailed | ❌ Limited |
| **Best For** | Beginners | Professionals | Hobbyists |

---

## 📋 League Codes Reference

### Football-Data.org Codes

```python
"PL"   # Premier League (England)
"PD"   # La Liga (Spain)
"BL1"  # Bundesliga (Germany)
"SA"   # Serie A (Italy)
"FL1"  # Ligue 1 (France)
"CL"   # Champions League
"ELC"  # Championship (England)
"PPL"  # Primeira Liga (Portugal)
"DED"  # Eredivisie (Netherlands)
"BSA"  # Série A (Brazil)
```

### API-Football League IDs

```python
39   # Premier League
140  # La Liga
78   # Bundesliga
135  # Serie A
61   # Ligue 1
2    # Champions League
3    # Europa League
```

---

## 🔧 Troubleshooting

### Issue: "Rate limit exceeded"

**Solution:**
- Wait 1 minute between requests
- Use API key for higher limits
- Fetch smaller date ranges

### Issue: "API key invalid"

**Solution:**
- Check you copied the key correctly
- Make sure you verified your email
- Try logging out and back in to get a fresh key

### Issue: "No data returned"

**Solution:**
- Check your date range
- Verify league code is correct
- Some leagues may not have data for certain dates

### Issue: "Connection error"

**Solution:**
- Check your internet connection
- Verify API endpoint is accessible
- Try again in a few minutes

---

## 💡 Tips for Best Results

1. **Start Small**: Import one league first to test
2. **Use Date Ranges**: Don't fetch all data at once
3. **Check Rate Limits**: Respect API rate limits
4. **Cache Data**: Store fetched data to avoid repeated requests
5. **Update Regularly**: Run imports daily for fresh data
6. **Backup Database**: Before importing, backup your database

---

## 🎓 Example Workflows

### Workflow 1: Fresh Start with Real Data

```bash
# 1. Clear simulated data (optional)
python scripts/seed_database.py  # Answer 'yes' to clear

# 2. Import real data
python scripts/import_real_data.py

# 3. Train models on real data
python scripts/train_all_models.py

# 4. Run app
python run.py
```

### Workflow 2: Add Real Data to Existing

```bash
# Import real data (keeps existing data)
python scripts/import_real_data.py

# Retrain models with combined data
python scripts/train_all_models.py

# Run app
python run.py
```

### Workflow 3: Daily Updates

```bash
# Run this daily to get latest matches
python scripts/import_real_data.py

# Optional: Retrain models weekly
python scripts/train_all_models.py
```

---

## 🌟 Recommended Setup

For the best experience:

1. **Get Football-Data.org API key** (FREE)
   - https://www.football-data.org/client/register

2. **Import last 2 years of data**
   - Modify date range in script
   - Run import script

3. **Set up daily updates**
   - Use Task Scheduler (Windows) or Cron (Mac/Linux)
   - Fetch new matches daily

4. **Retrain models weekly**
   - More data = better predictions
   - Run training script weekly

---

## 📞 Support

### Football-Data.org
- Website: https://www.football-data.org
- Documentation: https://www.football-data.org/documentation/quickstart
- Support: support@football-data.org

### API-Football
- Website: https://www.api-football.com
- Documentation: https://www.api-football.com/documentation-v3
- Support: Via RapidAPI

---

## ⚠️ Important Notes

1. **API Keys**: Never commit API keys to version control
2. **Rate Limits**: Respect API rate limits to avoid being blocked
3. **Terms of Service**: Read and follow each API's terms of service
4. **Commercial Use**: Check if your use case requires a paid plan
5. **Data Accuracy**: APIs are generally accurate but not 100% guaranteed

---

## 🎉 Next Steps

After importing real data:

1. ✅ Check the Matches page to see real fixtures
2. ✅ Generate predictions on real upcoming matches
3. ✅ Compare predictions with actual results
4. ✅ Retrain models with more real data for better accuracy
5. ✅ Set up automated daily imports

---

**Enjoy predicting with REAL data! ⚽📊**



