# Sample responses

Real `200` responses for three Cian API endpoints, taken on 4 November 2026. Search rows
are cut to five and photo lists to three, and each row's seller block (name, phones,
avatar) and seller ids are removed. Field names and values are otherwise unchanged. File
names follow the endpoint path.

Privacy review (4 Nov 2026): building numbers are removed from each search row's `address` and `full_address` (street and district are kept), and listing coordinates are rounded to three decimals (about 100 m).

| File | Request |
|---|---|
| `search.json` | `GET /search?deal=sale&property_type=flat&rooms=1&building_stage=resale&region_id=1&sort=newest` |
| `offer-price-history.json` | `GET /offer-price-history?offer_id=335713104` |
| `offer-valuation.json` | `GET /offer-valuation?offer_id=335713104&deal=sale` |

Offer 335713104 is the fifth search row. Live data changes daily, so do not hard-code these
values.
