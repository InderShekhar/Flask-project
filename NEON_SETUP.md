# Neon PostgreSQL Configuration Guide for Vercel

## ✅ What We've Done

1. **Added PostgreSQL dependencies** to `requirements.txt`:
   - `psycopg2-binary` - PostgreSQL database adapter
   - `python-dotenv` - Environment variable management

2. **Updated `app.py`** to use environment variables:
   - Uses `DATABASE_URL` from environment (Vercel sets this automatically)
   - Falls back to SQLite for local development

3. **Created `.env`** file for local development
4. **Created `.gitignore`** to protect sensitive data

## 🔧 Next Steps: Get Your Neon Database URL

### Option 1: From Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your Flask project
3. Click on **Storage** tab
4. Find your Neon database
5. Click **Show Secret** to reveal the connection string
6. Copy the `DATABASE_URL` (it looks like: `postgresql://username:password@host/database`)

### Option 2: From Neon Dashboard
1. Go to [Neon Console](https://console.neon.tech/)
2. Select your project
3. Go to **Dashboard** > **Connection Details**
4. Copy the connection string

## 📝 Configure Local Development

1. Open the `.env` file in your project
2. Replace the placeholder with your actual Neon database URL:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## 🚀 Deploy to Vercel

### The DATABASE_URL is already set in Vercel!
When you created the Neon database in Vercel, it automatically added the `DATABASE_URL` environment variable to your project. You don't need to manually configure it in Vercel.

### Just push your code:
```bash
git add .
git commit -m "Configure Neon PostgreSQL database"
git push origin main
```

Vercel will automatically:
- Detect the changes
- Install the new dependencies (psycopg2-binary)
- Use the DATABASE_URL environment variable
- Create the database tables on first run

## 🧪 Test Locally (Optional)

If you want to test with Neon locally:

1. Update `.env` with your Neon database URL
2. Restart your Flask app:
   ```bash
   python app.py
   ```

If you want to use SQLite locally (easier for development):
- Just comment out or remove the DATABASE_URL line in `.env`
- The app will automatically use SQLite

## ⚠️ Important Notes

- **Never commit `.env` file** - It's already in `.gitignore`
- **Vercel automatically sets DATABASE_URL** - No manual configuration needed in Vercel dashboard
- **Database tables are created automatically** - The `db.create_all()` in app.py handles this
- **SSL is required** - Neon requires `?sslmode=require` in the connection string

## 🔍 Troubleshooting

### If you get connection errors on Vercel:
1. Check that the Neon database is active in Vercel Storage
2. Verify the DATABASE_URL environment variable exists in Vercel project settings
3. Check Vercel deployment logs for specific error messages

### If tables aren't created:
- The app automatically creates tables on startup with `db.create_all()`
- Check Vercel logs to ensure no errors during initialization

## 📚 What Changed in the Code

**app.py:**
- Added `import os` and `from dotenv import load_dotenv`
- Changed database URI to: `os.getenv('DATABASE_URL', 'sqlite:///todo.db')`
- This reads from environment variable, falls back to SQLite if not found

**requirements.txt:**
- Added `psycopg2-binary==2.9.9` for PostgreSQL support
- Added `python-dotenv==1.0.0` for environment variable loading

## ✨ You're All Set!

Your Flask app is now configured to work with Neon PostgreSQL on Vercel! 🎉
