# noderow

Comparisons and build guides for agency automation stacks — GoHighLevel, n8n,
Make and Zapier.

## How the site is built

`deploy/` is the Netlify publish root and **is** the site. No framework, no
bundler, no build step on Netlify — the HTML in `deploy/` is committed as
generated.

Regenerate after any content or template change:

```
python3 tools/build.py     # generates deploy/, runs the validation gate
python3 tools/validate.py  # audits what is already in deploy/
```

`build.py` refuses to write anything if a page fails validation, so `deploy/`
never holds a page that would not pass review.

## Where things live

| Path | What it is |
|---|---|
| `content/products.json` | Every platform, its URLs and commission status. The only place a vendor URL is written. |
| `tools/site_config.py` | Site-wide constants: author, nav, footer, disclosure text. |
| `tools/entity.py` | Schema.org graph. One Organization, one Person, referenced by `@id`. |
| `tools/head.py` | The single `<head>` generator. Every page uses it. |
| `tools/components.py` | Header, footer, affiliate links, disclosure, integrity callout. |
| `tools/pages.py` | Page content. |
| `tools/build.py` | Renders `deploy/`, sitemap, RSS, llms.txt, robots.txt. |
| `tools/validate.py` | The publish gate. |
| `tools/affiliate.py` | Swaps a plain vendor URL for a real affiliate link. |
| `deploy/css/site.css` | The one stylesheet. Never create a second. |

## Adding an affiliate link

```
python3 tools/affiliate.py --list
python3 tools/affiliate.py gohighlevel "https://www.gohighlevel.com/?fp_ref=YOURID"
python3 tools/build.py
```

Pages read outbound URLs from `products.json`, so one command updates the link
everywhere. It refuses to set a link on a product marked `monetizable: false`.

## Rules that are enforced by code, not discipline

- Affiliate links get `rel="sponsored nofollow noopener"` automatically.
- Any page carrying an affiliate link must show the inline disclosure — the gate
  fails the build otherwise.
- The "we earn no commission" callout is generated from `monetizable: false`. It
  cannot silently go missing when a page is edited.
- `aggregateRating` is rejected by the gate. It is a spam-policy violation here.
- Links to unwritten pages render as parked `<span>`s, not dead anchors.
