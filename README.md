# BudsPilot website

Static site for BudsPilot, served by GitHub Pages from `main` (root).
Live at https://rizwanahmad8311.github.io/budspilot-site/

## Edit

All page content lives in `build.py`. The `.html` files in the repo root are generated: do not edit them by hand.

```bash
python3 build.py     # rebuilds every page, sitemap.xml, robots.txt, site.webmanifest
```

Commit the generated files together with `build.py`.

- `assets/style.css`, `assets/app.js`: design and the small amount of script (menu, scroll reveal)
- `assets/img/`: phone images cropped from the Play screenshots in the app repo (`brand/play/screenshots`)
- `assets/fonts/`: Inter and Plus Jakarta Sans (SIL Open Font License), subset to Latin

## Privacy policy

`privacy.html` must keep its URL (Play Console links to it). To update it: in the app repo run
`python3 brand/make_privacy_html.py`, copy `brand/privacy-policy.html` over `privacy.html` here,
then run `python3 build.py`, which keeps the policy text and date and wraps them in the site layout.

## When the app is public on Google Play

In `build.py` change `cta_buttons()` and `band()` from the "coming soon" email link to
`https://play.google.com/store/apps/details?id=com.budspilot.app`, add `'installUrl'` and
`'downloadUrl'` to `APP_LD`, and rebuild.

## Moving to another address

Change `SITE` in `build.py` (for example to `https://budspilot.com/`) and rebuild; canonical URLs,
the sitemap and structured data follow. For a custom domain also add a `CNAME` file.
