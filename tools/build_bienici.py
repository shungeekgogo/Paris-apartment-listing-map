"""Build listings-bienici.js from Bien'ici search results.

Usage (from the project folder):
    python tools/build_bienici.py            # build, reusing downloads cached in tools/cache
    python tools/build_bienici.py --refresh  # download fresh listings first

Data comes from Bien'ici's public listing endpoints (the same ones its website uses).
Location precision:
    exact    – Bien'ici shows the exact position
    street   – a street named in the description, checked against the approximate
               position with the French government address service (api-adresse.data.gouv.fr)
    area     – Bien'ici's approximate circle (50 m – 1 km)
    district – only the arrondissement is known
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
OUT = os.path.join(HERE, "..", "listings-bienici.js")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
PER_DISTRICT = {n: 20 for n in range(1, 10)} | {6: 80}  # more for the 6th, the default view
ZONES = {1: "-20727", 2: "-9542", 3: "-20742", 4: "-9597", 5: "-20873",
         6: "-9527", 7: "-9521", 8: "-20872", 9: "-9537"}
REFRESH = "--refresh" in sys.argv


def get_json(url, cache_name):
    path = os.path.join(CACHE, cache_name)
    if os.path.exists(path) and (not REFRESH or cache_name.startswith("geo_")):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    time.sleep(0.7)
    return data


def search(n):
    filters = {"size": PER_DISTRICT[n], "from": 0, "filterType": "buy", "propertyType": ["flat"],
               "page": 1, "sortBy": "publicationDate", "sortOrder": "desc", "onTheMarket": [True],
               "zoneIdsByTypes": {"zoneIds": [ZONES[n]]}}
    url = "https://www.bienici.com/realEstateAds.json?filters=" + urllib.parse.quote(json.dumps(filters))
    return get_json(url, f"search_{n}.json")["realEstateAds"]


def detail(ad_id):
    return get_json(f"https://www.bienici.com/realEstateAd.json?id={ad_id}", f"ad_{ad_id}.json")


def dist_m(a, b):
    dy = (a[0] - b[0]) * 111320
    dx = (a[1] - b[1]) * 111320 * math.cos(math.radians(a[0]))
    return math.hypot(dx, dy)


STREET_RE = re.compile(
    r"\b(rue|avenue|boulevard|bd|place|quai|square|passage|impasse|cour|allée|villa|cité)\s+"
    r"((?:de la |de l['’]|des |du |de |d['’]|la |le |saint[- ]|sainte[- ])*"
    r"[A-ZÉÈÀÂÎÔÛÇ][\w'’\-éèêàâîôûçëïü]+(?:[ \-](?:de |du |des |la |le |l['’]|d['’])?[A-ZÉÈÀÂÎÔÛÇ][\w'’\-éèêàâîôûçëïü]+)*)",
    re.IGNORECASE)


def find_street(text, postcode, centre, radius):
    """Return (street name, why) if the description names a street near the approximate position."""
    seen = set()
    for m in STREET_RE.finditer(text or ""):
        kind, name = m.group(1), m.group(2)
        before = (text[max(0, m.start() - 45):m.start()]).lower()
        if re.search(r"proche|près|proximité|pas d|pas de|minutes|entre|non loin|face|vue|donnant|depuis|jusqu|métro|et la|et le", before):
            continue  # a nearby landmark, not the address
        if not name[:1].isupper() and not name.lower().startswith(("de ", "du ", "des ", "d'", "d’", "la ", "le ", "saint")):
            continue
        q = f"{kind} {name}".strip()
        if q.lower() in seen:
            continue
        seen.add(q.lower())
        key = re.sub(r"[^a-z0-9]+", "_", q.lower())[:60]
        url = ("https://api-adresse.data.gouv.fr/search/?" +
               urllib.parse.urlencode({"q": q, "postcode": postcode, "type": "street", "limit": 1}))
        try:
            g = get_json(url, f"geo_{postcode}_{key}.json")
        except Exception:
            continue
        if not g or not g.get("features"):
            continue
        f = g["features"][0]
        p = f["properties"]
        if p.get("score", 0) < 0.6:
            continue
        lon, lat = f["geometry"]["coordinates"]
        # the street's reference point must be reasonably close to the approximate position
        if dist_m((lat, lon), centre) <= radius + 700:
            return p["name"], f"Street named in the listing text (“{q}”) and consistent with the approximate area shown by Bien'ici."
    return None, None


# Findings from looking through each listing's photos (Bien'ici id -> overrides).
# "street"/"lat"/"lng" are set only when the photos clearly place the flat.
PHOTO_NOTES = {
    "laforet-immo-facile-52930746": {
        "street": "Rue Saint-Sulpice", "lat": 48.8516, "lng": 2.3348,
        "clue": "Estimated from photos: a window looks straight across the street at the north side of Saint-Sulpice church (rose window, statues), with the towers to the right. That places it on Rue Saint-Sulpice."},
    "citya-1-705-TAPP705-971495": {
        "street": "Rue de Rennes",
        "clue": "Estimated from photos: the balcony view runs down a long straight Haussmann street ending at the Tour Montparnasse, which matches Rue de Rennes. Bien'ici's approximate area is on Rue de Rennes too."},
    "ag755942-551390453": {
        "clue_extra": "Photos: the corner windows overlook a wide boulevard with the Tour Montparnasse close by."},
    "ag755440-551233988": {
        "clue_extra": "Photos: the roof window frames the two towers of Saint-Sulpice church, which fits the approximate area."},
    "ag752476-550753523": {
        "clue_extra": "Photos: high-floor view west over the rooftops to the Eiffel Tower."},
    "iad-france-1011090": {
        "clue_extra": "Photos: rooftop terrace with the Tour Montparnasse close by to the south-west."},
    "hektor-ulys-303": {
        "clue_extra": "Photos include Place Saint-Sulpice and the Luxembourg Garden, but these are neighbourhood shots, not views from the flat."},
    "netty-dumarest-appt-2612": {
        "clue_extra": "Photos: a cobbled inner courtyard with a statue; no landmark that pins down the street."},
}

def geocode_address(text):
    key = re.sub(r"[^a-z0-9]+", "_", text.lower())[:70]
    url = "https://api-adresse.data.gouv.fr/search/?" + urllib.parse.urlencode({"q": text, "type": "housenumber", "limit": 1})
    try:
        g = get_json(url, f"geo_addr_{key}.json")
    except Exception:
        return None
    if not g or not g.get("features") or g["features"][0]["properties"].get("score", 0) < 0.7:
        return None
    f = g["features"][0]
    lon, lat = f["geometry"]["coordinates"]
    return lat, lon, f["properties"].get("street") or f["properties"].get("name")


PLATFORM_HOSTS = ("immo-facile.com", "apimo.pro", "netty.immo", "notaires.fr", "adaptimmo.com",
                  "digitregroup.io", "drive.google.com", "amazonaws.com", "googleusercontent.com")
HOST_MAP = {"bareme.iadfrance.fr": "https://www.iadfrance.fr/", "media.kwfrance.com": "https://www.kwfrance.com/"}


def seller_site(ad, agency):
    u = ad.get("agencyFeeUrl") or ""
    host = urllib.parse.urlparse(u).netloc
    if host in HOST_MAP:
        return HOST_MAP[host], False
    if host and not any(host.endswith(h) for h in PLATFORM_HOSTS):
        return f"https://{host}/", False
    if agency:
        return "https://www.google.com/search?" + urllib.parse.urlencode({"q": f"{agency} agence immobilière Paris"}), True
    return None, False


def elevator(ad):
    if ad.get("hasElevator") is not None:
        return bool(ad["hasElevator"])
    d = (ad.get("description") or "").lower()
    if re.search(r"sans ascenseur|pas d['’]ascenseur", d):
        return False
    if "ascenseur" in d:
        return True
    return None


def floor_text(ad):
    f, q = ad.get("floor"), ad.get("floorQuantity")
    if f is None:
        return ""
    s = "Ground floor" if f == 0 else f"Floor {f}"
    return s + (f" of {q}" if q else "")


def build():
    os.makedirs(CACHE, exist_ok=True)
    out = []
    for n in range(1, 10):
        for summary in search(n):
            ad = detail(summary["id"]) or summary
            if not ad.get("price") or not ad.get("surfaceArea"):
                continue
            desc = ad.get("description") or ""
            if re.search(r"\bviager\b", desc, re.IGNORECASE):
                continue  # life-annuity sale: the price is only a down payment and the flat stays occupied
            auction = "immo-interactif" in desc.lower() or "immo interactif" in desc.lower()
            c = ad.get("contactRelativeData") or {}
            agency = c.get("agencyNameToDisplay") or c.get("contactNameToDisplay") or ""
            blur = ad.get("blurInfo") or {}
            pos = blur.get("position") or blur.get("centroid")
            radius = blur.get("radius")
            quarter = (ad.get("district") or {}).get("libelle") or ""
            postcode = ad.get("postalCode") or f"7500{n}"

            street, why = None, None
            addr = re.search(r"Adresse du bien\s*:\s*(\d+[^\n]*?750\d\d)", desc)
            exact_pt = geocode_address(addr.group(1)) if addr else None
            if exact_pt:
                pos = {"lat": exact_pt[0], "lon": exact_pt[1]}
                street = exact_pt[2]
                precision, why = "exact", f"Full address given in the listing: {addr.group(1).strip()}."
            elif blur.get("type") == "exact" and pos:
                precision, why = "exact", "Exact position published by the seller on Bien'ici."
            elif pos and radius:
                street, why = find_street(ad.get("description"), postcode, (pos["lat"], pos["lon"]), radius)
                precision = "street" if street else "area"
                if not street:
                    why = f"Approximate position from Bien'ici (within about {radius} m). No street is named in the listing."
            else:
                precision, why = "district", "Only the arrondissement is published."

            note = PHOTO_NOTES.get(ad["id"])
            photo_checked = (n == 6 and precision in ("area", "district")  # the ones reviewed by hand
                             and ad["price"] <= 2_000_000 and ad["surfaceArea"] <= 150)
            if note:
                photo_checked = True
                if note.get("street"):
                    street, precision, why = note["street"], "street", note["clue"]
                    if note.get("lat"):
                        pos = {"lat": note["lat"], "lon": note["lng"]}
                elif note.get("clue_extra"):
                    why = f"{why} {note['clue_extra']}"
            elif photo_checked:
                why = f"{why} Photos checked: no landmark that pins down the street."

            site, is_search = seller_site(ad, agency)
            photos = [p["url"] + "?width=900" for p in (ad.get("photos") or [])[:2] if p.get("url")]
            rooms = ad.get("roomsQuantity") or 1
            out.append({
                "id": "bi-" + ad["id"],
                "source": "Bien'ici",
                "sourceType": "listing site",
                "url": f"https://www.bienici.com/annonce/{ad['id']}",
                "seller": agency,
                "sellerUrl": site,
                "sellerUrlIsSearch": is_search,
                "district": n,
                "price": ad["price"],
                "surface": round(ad["surfaceArea"], 1),
                "rooms": rooms,
                "bedrooms": ad.get("bedroomsQuantity"),
                "floor": floor_text(ad),
                "elevator": elevator(ad),
                "year": ad.get("yearOfConstruction"),
                "title": f"{'Studio' if rooms == 1 else f'{rooms}-room'} · {round(ad['surfaceArea'])} m²" + (f" · {quarter}" if quarter else ""),
                "quarter": quarter,
                "precision": precision,
                "street": street or "",
                "lat": pos["lat"] if pos else None,
                "lng": pos["lon"] if pos else None,
                "radius": radius if precision in ("area", "street") else None,
                "clue": why,
                "saleType": "Notary online auction (Immo-interactif): the price is the starting bid" if auction else "",
                "photoChecked": photo_checked,
                "published": (ad.get("publicationDate") or "")[:10],
                "photos": photos,
                "description": (ad.get("description") or "")[:600],
            })
    header = (f"// Generated by tools/build_bienici.py on {date.today().isoformat()}.\n"
              "// Source: Bien'ici (www.bienici.com). Photos are loaded from Bien'ici and belong to the listing agencies.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header + "window.LISTINGS_BIENICI = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n")
    counts = {p: sum(1 for l in out if l["precision"] == p) for p in ("exact", "street", "area", "district")}
    print(f"{len(out)} listings written to {os.path.normpath(OUT)}; precision: {counts}")


if __name__ == "__main__":
    build()
