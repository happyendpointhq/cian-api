"""Asking price against Cian's own market estimate, for the newest flats in a search.

    python valuation_gap.py              # 3 newest one-room resale flats in Moscow
    python valuation_gap.py 2 5          # Saint Petersburg, 5 flats

For each flat: the asking price, Cian's sale estimate with its low to high band, the gap
between the two, whether the asking price sits inside the band, and the estimate's change
over six months. One /search call plus one /offer-valuation call per flat.
"""

import sys

from client import get, rub, to_date

region = sys.argv[1] if len(sys.argv) > 1 else "1"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 3

rows = get(
    "/search",
    deal="sale",
    property_type="flat",
    rooms=1,
    building_stage="resale",
    region_id=region,
    sort="newest",
)["items"]

gaps = []
for row in rows[:count]:
    value = get("/offer-valuation", offer_id=row["offer_id"], deal="sale")
    estimate = value.get("sale_estimate")
    print(f"\n{row['offer_id']}  {row['total_area_m2']} m2  {row['address']}")
    if not value.get("is_supported") or not estimate:
        print("  no estimate for this listing")
        continue
    asking = value["asking_price_rub"]
    gap = asking / estimate["estimate_rub"] - 1
    inside = estimate["lower_rub"] <= asking <= estimate["upper_rub"]
    gaps.append(gap)
    history = estimate.get("history") or []
    since = to_date(history[0]["date"]) if history else None
    print(f"  asking   {rub(asking):>16}   Cian label: {value.get('price_tag') or '-'}")
    print(f"  estimate {rub(estimate['estimate_rub']):>16}   band {rub(estimate['lower_rub'])} to {rub(estimate['upper_rub'])}")
    print(f"  gap {gap:+.1%}, {'inside' if inside else 'outside'} the band; estimate "
          f"{estimate['change_6m_pct']:+}% over 6 months (monthly history from {since})")

if gaps:
    print(f"\n{len(gaps)} flats valued, average gap to estimate {sum(gaps) / len(gaps):+.1%}")
