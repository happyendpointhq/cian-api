# Cian API and Scraper

The Cian API returns Russian real estate data from cian.ru as JSON: flats, rooms, houses,
land and commercial property for sale and for rent, with price, area, rooms, floor, metro
stations and walking times, full listing records, asking-price history, Cian's own market
estimate for a flat with its six-month trend, past listings in the same building, new-build
complexes with layouts, price trends and construction progress, daily rentals with
availability, and the reference data searches need: regions, metro stations, districts and
developers. It is a REST API, so you get Cian data into your own code without building and
maintaining a Cian scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/cian-api?utm_source=github&utm_medium=readme&utm_campaign=cian-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/cian-ru
- Product page: https://happyendpoint.com/library/cian-api?utm_source=github&utm_medium=readme&utm_campaign=cian-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://cian-ru.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 39, all `GET` |
| Coverage | Russia, by `region_id` (Moscow `1`, Saint Petersburg `2`, Moscow Oblast `4593`, Kazan `4777`) |
| Listing types | Sale and long-term or daily rent: flats, rooms, beds, shares, houses, land, commercial; new-build complexes |
| Page size | Fixed at 28 listings; at most 1,500 listings per search |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}`; prices in RUB as numbers |

---

## What data you get

**Search**
- Listings for sale or rent with more than a hundred filters (rooms, area, floor, price, price per square metre, metro and walking time, district, street, new build or resale, seller type) and ten sort orders
- Map pins for a search, and a search run from a pasted cian.ru results URL

**Listings**
- The full listing card by id or URL, its dated asking-price history, similar listings, and other listings in the same building or nearby
- Cian's market estimate for a flat, for sale or for rent, with a low to high band and six months of monthly values

**New builds**
- Residential complexes by region with price, area, floor, completion year and class filters
- One complex's houses and deadlines, flat layouts and the flats behind each, monthly price trend, construction photo reports, state-register reliability check, reviews and buyer questions

**Daily rentals and reference data**
- Short-term rentals with nightly prices, an availability calendar with a price quote, guest reviews and house rules
- Regions, cities, address geocoding, metro stations, districts, highways, suburban railway stations, cottage villages and developers

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/cian-ru). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

```bash
curl "https://cian-ru.p.rapidapi.com/search?deal=sale&property_type=flat&rooms=1&building_stage=resale&region_id=1&sort=newest" \
  -H "x-rapidapi-host: cian-ru.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py 1
```

```python
from client import get

page = get("/search", deal="sale", property_type="flat", rooms=1, region_id=1, sort="newest")
for row in page["items"]:
    print(row["offer_id"], row["price"], row["total_area_m2"], row["address"])

value = get("/offer-valuation", offer_id=page["items"][0]["offer_id"], deal="sale")
print(value["asking_price_rub"], value["sale_estimate"]["estimate_rub"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs 1
```

---

## Example response

`GET /offer-valuation?offer_id=335713104&deal=sale`, with the monthly history cut to two
values. More responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "offer_id": 335713104,
    "category": "flatSale",
    "deal": "sale",
    "is_supported": true,
    "asking_price_rub": 13150000,
    "asking_price_period": "total",
    "sale_estimate": {
      "estimate_rub": 13400000,
      "lower_rub": 12100000,
      "upper_rub": 14800000,
      "change_6m_pct": -6.6,
      "change_6m_text": "6,6%",
      "change_6m_direction": "decrease",
      "history": [
        { "date": 1777593600000, "price_rub": 14385950 },
        { "date": 1793491200000, "price_rub": 13440969 }
      ]
    },
    "rent_estimate": null,
    "price_tag": "Хорошая цена"
  }
}
```

---

## Endpoints

Base URL: `https://cian-ru.p.rapidapi.com`

### Search

| Endpoint | Returns |
|---|---|
| `GET /search` | Listings for sale or rent, with filters, ten sort orders and 28 full cards a page |
| `GET /map-clusters` | Map pins for a search in a map view, with listing count and price label |
| `GET /search-by-url` | A search run from a cian.ru results URL |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /offer` | The full card of one listing by `offer_id` |
| `GET /offer-by-url` | The same card from a cian.ru listing URL |
| `GET /offer-price-history` | The dated asking-price history of a listing, with a change summary |
| `GET /similar-offers` | Listings Cian ranks as alternatives |
| `GET /house-offer-history` | Past and current listings in the same building, or nearby comparable ones |
| `GET /offer-valuation` | Cian's market estimate of a flat for sale or rent, with its band and six-month trend |

### New builds

| Endpoint | Returns |
|---|---|
| `GET /newbuildings` | Residential complexes in a region, with price, area, floor, completion and class filters |
| `GET /newbuilding` | One complex: houses and deadlines, prices and per-room tables, promotions and specs |
| `GET /newbuilding-layouts` | Every flat layout in a complex, with area, price range and flats per layout |
| `GET /newbuilding-layout-offers` | The flats for sale behind one layout, with price, floor and discount |
| `GET /newbuilding-construction-progress` | Dated construction photo reports |
| `GET /newbuilding-reliability` | The state-register check: deadlines, deadline shifts, escrow and permits |
| `GET /newbuilding-reviews` | Buyer and resident reviews with ratings |
| `GET /newbuilding-review-answers` | The reply thread of one review |
| `GET /newbuilding-questions` | Buyer questions about a complex |
| `GET /newbuilding-question-answers` | The answers to one question |
| `GET /newbuilding-price-trend` | Monthly average price and price per square metre by room count, with sales volume |
| `GET /developer` | A developer's track record, reliability check and rating |

### Daily rent

| Endpoint | Returns |
|---|---|
| `GET /dailyrent-search` | Short-term rentals with nightly prices, deposits and ratings |
| `GET /dailyrent-availability` | The availability calendar and a price quote for dates and guests |
| `GET /dailyrent-reviews` | Guest reviews with scores |
| `GET /dailyrent-listing` | Deposit, house rules and rating scores of a daily rental |

### Agents

| Endpoint | Returns |
|---|---|
| `GET /agent` | The public profile of an agent, agency or developer |
| `GET /agent-reviews` | Reviews of an agent, agency or developer |
| `GET /agent-listings` | Every live listing of one agent, agency or developer |

### Reference

| Endpoint | Returns |
|---|---|
| `GET /regions` | Every region of Russia with its `region_id` |
| `GET /locations` | City and region name autocomplete |
| `GET /geocode` | An address parsed into region, location, street and house ids |
| `GET /place-suggestions` | Districts, metro stations, complexes, highways, villages and developers by name |
| `GET /metro-stations` | A city's metro stations and lines |
| `GET /districts` | A city's districts |
| `GET /highways` | Highways out of Moscow and Saint Petersburg |
| `GET /railway-stations` | Suburban railway stations of a region |
| `GET /cottage-villages` | Cottage villages of an area |
| `GET /developers` | Developers with complexes in an area |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples against the API on 4 November 2026. They are the
mistakes that produce wrong numbers rather than errors.

- **A search stops at 1,500 listings.** One-room resale flats in Moscow matched 7,461
  (`total`), but `retrievable_total` was 1,500 and `is_truncated` true. Split a large
  search by district, metro station or price band to read all of it. Pages hold a fixed 28.
- **"Хорошая цена" is not a verdict on the estimate.** Cian's "good price" label sat on a
  listing asking 6.9% more than Cian's own estimate. In `valuation_gap.py`, three new
  Moscow listings ranged from 3.7% below to 12.2% above the estimate, and one was outside
  the estimate's band.
- **Two timestamp units.** Price history dates are Unix seconds (`1793720263`), valuation
  history dates Unix milliseconds (`1777593600000`), and `created_at` is an ISO string.
  `client.to_date()` handles all three.
- **One deal per valuation call.** `deal=sale` fills `sale_estimate` and leaves
  `rent_estimate` null; ask again with `deal=rent` for the rent estimate.
- **The sign is already in `change_6m_pct`.** It reads `-6.6` with
  `change_6m_direction: "decrease"`, and can be a whole number (`12`). Do not apply the
  direction twice.
- **New listings have one history point.** The newest listings were all created the day
  before, with `changes_count: 0` and `days_listed: 0`. Price-cut analysis needs older
  listings (`sort=oldest`, or the listings of `/house-offer-history`).
- **Resale flats can carry a `newbuilding` block.** A resale flat in a finished complex has
  `is_new_building: false` and still names its complex in `newbuilding`. Filter on
  `building_stage` in the search, not on that block.
- **Display text is Russian, numbers are plain.** `price_formatted` (`"10 500 000 ₽"`,
  with non-breaking spaces between the digit groups), `price_per_m2_formatted` and
  `floor_text` (`"2/16 этаж"`) are for display; use `price`, `total_area_m2`, `floor` and
  `floors_total`.
- **Search rows include the seller block.** It holds names and phone numbers; leave it out
  of anything you store or show. The samples here have it removed.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Newest one-room resale flats in a region with price per square metre, then one listing's price history |
| [`examples/python/valuation_gap.py`](examples/python/valuation_gap.py) | Asking price against Cian's market estimate and band for the newest flats in a search |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The search in Node 18+, no dependencies |
| [`samples/`](samples/) | Real responses for three endpoints |

Output of `valuation_gap.py` on 4 November 2026 (Moscow, three newest listings):

```
335747347  38.3 m2  Митинская улица, 44, Москва
  asking     17 100 000 RUB   Cian label: Хорошая цена
  estimate   16 000 000 RUB   band 14 400 000 RUB to 17 600 000 RUB
  gap +6.9%, inside the band; estimate +12% over 6 months (monthly history from 2026-05-01)

335738951  36.2 m2  улица Омская, 5, Внуковское поселение, Москва
  asking     10 500 000 RUB   Cian label: Хорошая цена
  estimate   10 900 000 RUB   band 9 800 000 RUB to 11 900 000 RUB
  gap -3.7%, inside the band; estimate +8.9% over 6 months (monthly history from 2026-05-01)

335735980  32.5 m2  Борисовский проезд, 22К1, Москва
  asking     15 600 000 RUB   Cian label: -
  estimate   13 900 000 RUB   band 12 500 000 RUB to 15 200 000 RUB
  gap +12.2%, outside the band; estimate +14% over 6 months (monthly history from 2026-05-01)

3 flats valued, average gap to estimate +5.1%
```

---

## API or your own Cian scraper

A homemade Cian scraper has to keep up with the site's layouts and anti-bot rules and breaks
when they change. This API returns the same listings, price histories and estimates as
documented JSON with a stable contract, so your work goes into the analysis. If you need a
one-off file or a recurring export rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=cian-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Cian without
code:

```json
{
  "mcpServers": {
    "cian": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: cian-ru.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Cian API?

Cian does not offer a public developer API for its listings. This API, built and maintained
by Happy Endpoint and independent of Cian, returns cian.ru listings, price histories,
estimates and new-build data as REST and JSON.

### Can I get Moscow flat prices from Cian?

Yes. `/search` with `region_id=1` returns Moscow listings with price, area and price per square
metre, and `/offer-valuation` Cian's estimate for any flat listing.
[`valuation_gap.py`](examples/python/valuation_gap.py) compares the two.

### Can I track price changes on a listing?

Yes. `/offer-price-history` returns every dated asking price of a listing with a summary of
increases and decreases, and `/house-offer-history` the past listings in the same building.

### Does it cover new builds?

Yes. `/newbuildings` lists residential complexes, and the `/newbuilding-*` endpoints return
layouts, prices, monthly price trends, construction progress and the state-register reliability
check for one complex.

### Is there a free Cian API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/cian-ru), where every endpoint can
also be tested in the browser.

### Where is the documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the endpoint
tables above summarise them. Real example responses are in [`samples/`](samples/).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [yad2-api](https://github.com/happyendpointhq/yad2-api) - Israel listings with registered sale prices
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spanish rentals and homes for sale
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
