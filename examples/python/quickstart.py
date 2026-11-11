"""Newest one-room resale flats for sale in Moscow, then one listing's price history.

    python quickstart.py            # Moscow (region_id 1)
    python quickstart.py 2          # Saint Petersburg
"""

import sys

from client import get, rub, to_date

region = sys.argv[1] if len(sys.argv) > 1 else "1"

# 1. Search. Pages hold 28 listings, and at most 1,500 listings of a search can be read.
page = get(
    "/search",
    deal="sale",
    property_type="flat",
    rooms=1,
    building_stage="resale",
    region_id=region,
    sort="newest",
)
print(f"{page['total']:,} listings match, {page['retrievable_total']:,} can be paged, {page['returned']} on this page\n")
for row in page["items"][:10]:
    per_m2 = row["price"] / row["total_area_m2"] if row.get("total_area_m2") else None
    label = (row.get("price_details") or {}).get("price_label") or ""
    print(
        f"{rub(row['price']):>16}  {row['total_area_m2'] or '?':>5} m2  {rub(per_m2):>12}/m2  "
        f"floor {row['floor_text'] or '?':<11} {label}"
    )

if not page["items"]:
    raise SystemExit("No listings on this page.")

# 2. The asking-price history of the first listing. Dates here are Unix seconds.
offer_id = page["items"][0]["offer_id"]
history = get("/offer-price-history", offer_id=offer_id)
summary = history["summary"]
print(f"\nOffer {offer_id}: first price {rub(summary['first_price'])}, now {rub(summary['current_price'])}, "
      f"{summary['changes_count']} changes in {summary['days_listed']} days")
for event in history["history"]:
    print(f"  {to_date(event['date'])}  {rub(event['price'])}")
