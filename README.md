# Paris Apartment Listing Map

A browser-based map of apartments for sale in Paris arrondissements 1–9.

- Filter by arrondissement (1er–9e), asking price, floor space (m²), price per m², rooms, and how precisely the location is known.
- Click a pin or a list row to see 1–2 photos, the asking price, €/m², and where the apartment is (or is estimated to be).
- Location precision is shown on the map:
  - **Exact address**: green pin.
  - **Street, estimated from photos**: brass pin with a dashed circle around the likely street.
  - **District only**: dashed pin, and the whole arrondissement is outlined when selected.

## Run

Open `index.html` in a web browser (double-click it). It needs an internet connection for the map tiles and fonts.

## Data

- `listings.js`: the apartments. **The current entries are sample data for testing, not real listings.** Each field is described at the top of the file. Add up to two photo URLs per listing in `photos`; listings without photos show a drawn illustration.
- `districts.js`: arrondissement 1–9 boundaries from [Paris Open Data](https://opendata.paris.fr/explore/dataset/arrondissements/) (Licence Ouverte / ODbL).

Map tiles: Esri Light/Dark Gray Canvas. Map library: Leaflet 1.9.4.
