// Cian API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs 1      (1 = Moscow, 2 = Saint Petersburg)

const HOST = 'cian-ru.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Cian API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const rub = (v) => `${Math.round(v).toLocaleString('en-US').replace(/,/g, ' ')} RUB`;

const region = process.argv[2] ?? '1';
const page = await get('/search', {
  deal: 'sale',
  property_type: 'flat',
  rooms: 1,
  building_stage: 'resale',
  region_id: region,
  sort: 'newest',
});
// 28 rows a page; only the first 1,500 listings of a search can be paged.
console.log(`${page.total} listings, ${page.retrievable_total} pageable`);
for (const row of page.items.slice(0, 10)) {
  const perM2 = row.total_area_m2 ? rub(row.price / row.total_area_m2) : '-';
  console.log(`${rub(row.price).padStart(16)}  ${row.total_area_m2} m2  ${perM2}/m2  ${row.address}`);
}
