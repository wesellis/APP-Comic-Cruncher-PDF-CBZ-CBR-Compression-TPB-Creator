# 🌐 GitHub Pages Setup Guide

## 🚀 Quick Setup (2 minutes)

### Step 1: Enable GitHub Pages
1. Go to your repository: `https://github.com/wesellis/CBR-to-CBZ-Converter`
2. Click the **Settings** tab (top navigation)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **"GitHub Actions"**
5. Click **Save**

### Step 2: Trigger Deployment
1. Go to **Actions** tab in your repository
2. Find the **"Deploy to GitHub Pages"** workflow
3. Click **"Re-run jobs"** or push any commit to main branch

### Step 3: Access Your Website
Your website will be live at: `https://wesellis.github.io/CBR-to-CBZ-Converter/`

---

## 🔧 Troubleshooting

### If Pages Can't Be Enabled
**Alternative**: Your website is ready in the `docs/` folder and can be:
- Used locally by opening `docs/index.html` in a browser
- Deployed to other hosting services (Netlify, Vercel, etc.)
- Shared directly with the HTML file

### If Images Don't Show
The workflow automatically fixes image paths, but if needed:
- Images should be in the `assets/` folder at repository root
- Website expects them at `assets/filename.png`

### If Workflow Fails
The workflow includes helpful error messages and will:
- Show setup instructions if Pages isn't enabled
- Continue with alternative deployment options
- Provide clear next steps

---

## 📁 File Structure
```
CBR-to-CBZ-Converter/
├── docs/
│   └── index.html          # Website homepage
├── assets/                 # Screenshots folder
│   ├── ComicCruncher1.png  # Main interface screenshot
│   ├── ComicCombiner1.png  # Combiner mode screenshot
│   └── ComicCombiner2.png  # Batch processing screenshot
├── .github/workflows/
│   └── deploy-pages.yml    # Deployment workflow
└── README.md              # Updated with website link
```

---

## ✅ Success Indicators

**GitHub Pages Enabled**: Green checkmark in Settings → Pages  
**Workflow Success**: Green checkmark in Actions tab  
**Website Live**: Visit your URL and see the Comic Cruncher website  
**Images Working**: Screenshots appear in the gallery section  

---

**Your professional Comic Cruncher website will showcase your dual-mode comic processing application with interactive screenshots and comprehensive documentation!** 🎉
