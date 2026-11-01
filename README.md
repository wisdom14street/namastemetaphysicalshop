# namastemetaphysicalshop.com
Ritual, altar and metaphysical supply shop for Namaste Bookshop (Wealth Edge Ventures Inc.). Static site on GitHub Pages, rebuilt daily from the namastebookshop.com public catalog by `.github/workflows/deploy.yml`. Checkout uses Shopify cart permalinks on namastebookshop.com with `attributes[Storefront]=Namaste Metaphysical Shop`.
- `site/sitecopy.py`: drawers, product selection and all copy. `site/p2site.py`: visit/pickup copy. `site/theme.css`: look.
- Build locally: `python3 scripts/fetch.py && python3 scripts/build.py --preview`
