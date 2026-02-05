# PM Analytics - Private Markets Data Platform

A comprehensive data platform for the private markets industry, providing transparency and insights for General Partners (GPs) and Limited Partners (LPs).

## 🚀 Live Demo

Visit the live application: [PM Analytics on GitHub Pages](https://marcushudson.github.io/PM-Analytics/)

## 📋 Features

- **Real-time Dashboards**: Monitor key metrics across private markets funds
- **Data Visualization**: Interactive charts for AUM distribution and vintage year analysis
- **Fund Database**: Comprehensive searchable database of private equity, infrastructure, real estate, and credit funds
- **High Data Quality**: Only displaying funds with ≥95% confidence scores
- **Responsive Design**: Optimized for desktop and mobile devices

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: GitHub Pages
- **CI/CD**: GitHub Actions

## 🏃‍♂️ Running Locally

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📦 Building for Production

```bash
npm run build
```

This creates a static export in the `out` directory, ready for GitHub Pages deployment.

## 🚢 Deployment

The application automatically deploys to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

### Manual Deployment

1. Ensure GitHub Pages is enabled in repository settings
2. Set source to "GitHub Actions"
3. Push changes to `main` branch
4. GitHub Actions will build and deploy automatically

## 📊 Data Sources

Data is sourced from:
- SEC filings (Form D, Form ADV, 10-K reports)
- Authoritative regulatory filings
- Public disclosures from institutional investors
- Verified private markets data providers

## 📄 License

Copyright © 2026 PM Analytics. All rights reserved.

## 🤝 Contact

For questions or feedback, please open an issue on GitHub.
