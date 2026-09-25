// Apartment listings shown on the map.
//
// THESE ARE SAMPLE LISTINGS for testing the app — not real properties for sale.
// Replace them with real listings (keep the same fields).
//
// Fields:
//   id         unique string
//   district   1–9 (arrondissement)
//   price      asking price in euros
//   surface    living area in m² (loi Carrez)
//   rooms      number of "pièces" (1 = studio)
//   floor      e.g. "3rd floor, elevator"
//   title      short headline
//   precision  "exact"    → address is known
//              "street"   → only the street is known / estimated from photos
//              "district" → only the arrondissement is known
//   street     street name (for "exact" and "street")
//   lat, lng   point on the map (for "district", leave empty: the app places it in the district)
//   clue       how the location was found or estimated (e.g. what the photos show)
//   photos     optional list of 1–2 image URLs; if empty, the app draws an illustration
//   source     optional link to the original listing

window.LISTINGS = [
  { id: "p01", district: 1, price: 1020000, surface: 68, rooms: 3, floor: "4th floor, elevator",
    title: "Bright 3-room near Saint-Honoré", precision: "street", street: "Rue Saint-Honoré",
    lat: 48.8613, lng: 2.3428, clue: "Window photo shows the Saint-Eustache church apse to the north-east.", photos: [] },
  { id: "p02", district: 1, price: 495000, surface: 38, rooms: 2, floor: "2nd floor",
    title: "2-room with beams, Les Halles side", precision: "district", street: "",
    clue: "Interior photos only. No exterior landmarks visible.", photos: [] },

  { id: "p03", district: 2, price: 560000, surface: 45, rooms: 2, floor: "3rd floor",
    title: "Montorgueil 2-room over the market street", precision: "street", street: "Rue Montorgueil",
    lat: 48.8652, lng: 2.3470, clue: "Balcony photo shows a pedestrian market street with the Stohrer bakery sign.", photos: [] },
  { id: "p04", district: 2, price: 1090000, surface: 92, rooms: 4, floor: "5th floor, elevator",
    title: "Family 4-room in Sentier", precision: "district", street: "",
    clue: "Listing text says “Sentier”; photos show only courtyard walls.", photos: [] },
  { id: "p05", district: 2, price: 830000, surface: 70, rooms: 3, floor: "1st floor",
    title: "Near Passage Choiseul", precision: "exact", street: "Rue Saint-Augustin",
    lat: 48.8683, lng: 2.3358, clue: "Address given in listing.", photos: [] },

  { id: "p06", district: 3, price: 790000, surface: 64, rooms: 3, floor: "2nd floor",
    title: "Haut-Marais 3-room", precision: "street", street: "Rue de Bretagne",
    lat: 48.8633, lng: 2.3620, clue: "Street photo shows the Marché des Enfants Rouges entrance.", photos: [] },
  { id: "p07", district: 3, price: 1790000, surface: 128, rooms: 5, floor: "Piano nobile, 1st floor",
    title: "Hôtel particulier floor, Marais", precision: "exact", street: "Rue Vieille-du-Temple",
    lat: 48.8611, lng: 2.3591, clue: "Address given in listing.", photos: [] },
  { id: "p08", district: 3, price: 295000, surface: 24, rooms: 1, floor: "6th floor, no elevator",
    title: "Studio under the roofs", precision: "district", street: "",
    clue: "Only rooftop view; zinc roofs without identifiable landmark.", photos: [] },

  { id: "p09", district: 4, price: 1980000, surface: 110, rooms: 4, floor: "3rd floor, elevator",
    title: "Quai view on Île Saint-Louis", precision: "street", street: "Quai de Bourbon",
    lat: 48.8529, lng: 2.3547, clue: "Window photo shows the Seine and the Hôtel de Ville roofline across the water.", photos: [] },
  { id: "p10", district: 4, price: 575000, surface: 42, rooms: 2, floor: "4th floor",
    title: "2-room in the Pletzl", precision: "street", street: "Rue des Rosiers",
    lat: 48.8572, lng: 2.3589, clue: "Street photo shows narrow pedestrian street with falafel shop signs.", photos: [] },
  { id: "p11", district: 4, price: 2750000, surface: 145, rooms: 5, floor: "2nd floor",
    title: "Under the arcades, Place des Vosges", precision: "exact", street: "Place des Vosges",
    lat: 48.8556, lng: 2.3656, clue: "Address given in listing.", photos: [] },

  { id: "p12", district: 5, price: 480000, surface: 40, rooms: 2, floor: "3rd floor",
    title: "Mouffetard 2-room", precision: "street", street: "Rue Mouffetard",
    lat: 48.8424, lng: 2.3498, clue: "Street photo shows the sloping market street and Saint-Médard church at the end.", photos: [] },
  { id: "p13", district: 5, price: 1250000, surface: 96, rooms: 4, floor: "5th floor, elevator",
    title: "Latin Quarter 4-room with balcony", precision: "exact", street: "Rue des Écoles",
    lat: 48.8490, lng: 2.3487, clue: "Address given in listing.", photos: [] },
  { id: "p14", district: 5, price: 690000, surface: 58, rooms: 3, floor: "1st floor",
    title: "Quiet 3-room on courtyard", precision: "district", street: "",
    clue: "Courtyard photos only.", photos: [] },

  { id: "p15", district: 6, price: 1160000, surface: 75, rooms: 3, floor: "2nd floor",
    title: "Cherche-Midi 3-room", precision: "street", street: "Rue du Cherche-Midi",
    lat: 48.8488, lng: 2.3270, clue: "Façade photo matches the Poilâne storefront across the street.", photos: [] },
  { id: "p16", district: 6, price: 2950000, surface: 180, rooms: 6, floor: "4th floor, elevator",
    title: "Large family flat near Luxembourg", precision: "exact", street: "Rue de Fleurus",
    lat: 48.8466, lng: 2.3316, clue: "Address given in listing.", photos: [] },
  { id: "p17", district: 6, price: 720000, surface: 48, rooms: 2, floor: "5th floor",
    title: "2-room with Saint-Sulpice view", precision: "street", street: "Rue Saint-Sulpice",
    lat: 48.8508, lng: 2.3355, clue: "Window photo frames both Saint-Sulpice towers from the east, at close range.", photos: [] },

  { id: "p18", district: 7, price: 1020000, surface: 72, rooms: 3, floor: "3rd floor, elevator",
    title: "Rue Cler 3-room", precision: "street", street: "Rue Cler",
    lat: 48.8563, lng: 2.3065, clue: "Street photo shows the pedestrian food market street with café terraces.", photos: [] },
  { id: "p19", district: 7, price: 2400000, surface: 160, rooms: 5, floor: "6th floor, elevator",
    title: "Eiffel Tower view", precision: "exact", street: "Avenue de La Bourdonnais",
    lat: 48.8567, lng: 2.2987, clue: "Address given in listing.", photos: [] },
  { id: "p20", district: 7, price: 490000, surface: 35, rooms: 2, floor: "Ground floor",
    title: "Compact 2-room, Saint-Germain side", precision: "district", street: "",
    clue: "Interior photos only.", photos: [] },

  { id: "p21", district: 8, price: 1290000, surface: 105, rooms: 4, floor: "2nd floor, elevator",
    title: "Classic 4-room, Miromesnil", precision: "street", street: "Rue de Miromesnil",
    lat: 48.8752, lng: 2.3157, clue: "Street sign visible in the entrance photo.", photos: [] },
  { id: "p22", district: 8, price: 4100000, surface: 210, rooms: 6, floor: "3rd floor, elevator",
    title: "Golden Triangle apartment", precision: "exact", street: "Avenue Montaigne",
    lat: 48.8664, lng: 2.3046, clue: "Address given in listing.", photos: [] },
  { id: "p23", district: 8, price: 540000, surface: 44, rooms: 2, floor: "6th floor, elevator",
    title: "2-room near Saint-Lazare", precision: "district", street: "",
    clue: "Listing mentions “close to Saint-Lazare”; no photo landmarks.", photos: [] },

  { id: "p24", district: 9, price: 690000, surface: 62, rooms: 3, floor: "4th floor",
    title: "SoPi 3-room", precision: "street", street: "Rue des Martyrs",
    lat: 48.8786, lng: 2.3403, clue: "Street photo shows the sloping shopping street toward Montmartre.", photos: [] },
  { id: "p25", district: 9, price: 420000, surface: 39, rooms: 2, floor: "2nd floor",
    title: "2-room near Notre-Dame-de-Lorette", precision: "district", street: "",
    clue: "Interior photos only.", photos: [] },
  { id: "p26", district: 9, price: 1380000, surface: 120, rooms: 5, floor: "3rd floor, elevator",
    title: "Trudaine family flat", precision: "exact", street: "Avenue Trudaine",
    lat: 48.8820, lng: 2.3442, clue: "Address given in listing.", photos: [] }
];
