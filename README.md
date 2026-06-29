# LIQ Invoice

**LIQ Invoice — Beautiful invoices in 60 seconds. No subscriptions.**

A clean, fast desktop app that turns your line items into a polished,
branded PDF invoice — and keeps track of every one you've sent. No
account, no cloud, no monthly fee. Pay once, own it forever.

## What's inside

- Real-time invoice builder with instant totals
- Branded PDF output — your logo, your accent color
- Full Cyrillic support (Russian and Ukrainian render perfectly)
- Built-in invoice history — mark Paid, Unpaid, or Cancelled, search anytime
- Light and Dark themes
- English, Russian and Ukrainian interface
- Runs fully offline — your data stays on your machine (you can make it better)

## Download
Use the signed installer in `public_download/` or publish it from GitHub Releases.

## Screenshots
Replace `docs/images/screenshot-1.png` and `docs/images/screenshot-2.png` with
real screenshots from the app to show the UI in the GitHub Pages site.

## Support
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/liqapps)

## Running from source

```bash
pip install customtkinter reportlab pillow pdf2image
python invoice_app.py
```

## Notes
The app includes full Cyrillic support and uses bundled fonts for correct Russian
and Ukrainian PDF rendering.
