# Paris Apartment Listing Map

A browser-based map of real apartments for sale in Paris arrondissements 1–9.

- Filters: arrondissement (1er–9e), asking price, floor space (m²), price per m², rooms, elevator, source (listing site or newspaper) and how precisely the location is known.
- Opens on: 6th arrondissement, up to €2,000,000, up to 150 m², elevator = Yes.
- Click a pin or a list row to see two listing photos, the asking price, €/m², floor, elevator, where the apartment is (or is estimated to be), the source, a link to the listing, and the seller with a link to their website.
- Location precision on the map:
  - **Exact address** (green): the seller published the position or the full address.
  - **Street** (brass): a street named in the listing text, or worked out from the photos, checked against the approximate position.
  - **Approximate area** (purple): the circle published by Bien'ici (50 m – 1 km).
  - **District only** (dashed): only the arrondissement is known.

## Run

Double-click `Paris Apartment Listing Map` (the shortcut) or open `index.html` in a web browser. It needs an internet connection for the map, fonts and photos.

## Data

- `listings-bienici.js`: 239 listings from [Bien'ici](https://www.bienici.com), fetched 25 Sep 2026 (20 newest per arrondissement, 80 for the 6th). Life-annuity sales (*viager*) are left out; notary online auctions are labelled because their price is a starting bid.
- `listings-newspaper.js`: listings from newspaper property sections, marked "Newspaper" in the app. Empty for now.
- `districts.js`: arrondissement boundaries from [Paris Open Data](https://opendata.paris.fr/explore/dataset/arrondissements/).
- Photos are loaded from Bien'ici when you open a listing; they belong to the listing agencies and are not stored in this repository.

Sites that block automated access (SeLoger, PAP, Leboncoin, Logic-Immo, Le Parisien) are not used.

### Refresh the listings

```
python tools/build_bienici.py --refresh
```

Without `--refresh` it rebuilds from the downloads cached in `tools/cache` (not committed). Photo-based location findings are kept in `PHOTO_NOTES` inside the script.

Map tiles: Esri Light/Dark Gray Canvas. Map library: Leaflet 1.9.4. Street lookups: api-adresse.data.gouv.fr.
