let map;
let backgroundMap;
let autocomplete;
let userMarker;
let markersArray = [];

const apiKey = "YOUR_API_KEY_HERE"; 

function initMap() {
    const bounds = new google.maps.LatLngBounds();
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 55.53, lng: 9.4 },
        zoom: 10,
        disableDefaultUI: true,
    });
    backgroundMap = new google.maps.Map(document.getElementById("backgroundMap"), {
        center: { lat: 55.53, lng: 9.4 },
        zoom: 10,
        disableDefaultUI: false,
    });

    function updateBackgroundMap(location) {
        map.setCenter(location);
    }

    function updateBackgroundMap(location) {
        const backgroundBounds = new google.maps.LatLngBounds(location);
        backgroundMap.fitBounds(backgroundBounds);
    }

    function geocodeAddress(geocoder, address, callback) {
        geocoder.geocode({ address: address }, (results, status) => {
            if (status === "OK" && results[0]) {
                const location = {
                    lat: results[0].geometry.location.lat(),
                    lng: results[0].geometry.location.lng(),
                };
                callback(location);
                updateBackgroundMap(location);
            } else {
                callback(null);
            }
        });
    }

    const geocoder = new google.maps.Geocoder();
    const service = new google.maps.DistanceMatrixService();

    const input = document.getElementById("address");
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo("bounds", map);

    document.getElementById("getProximityGrading").addEventListener("click", () => {
        const address = input.value;
        geocodeAddress(geocoder, address, (location) => {
            if (location) {
                userMarker = new google.maps.Marker({
                    position: location,
                    map: backgroundMap,
                    title: "Your Location"
                });

                calculateGrihaScore(location);
            } else {
                document.getElementById("griha-score").innerText = "Address not found. Please enter a valid address.";
            }
        });
    });
}

const grihaPlaces = [
    { name: "Pharmacy", types: ["pharmacy", "drugstore"] },
    { name: "Hospitals", types: ["doctor", "hospital"] },
    { name: "Other Medical Facilities", types: ["physiotherapist", "dentist", "veterinary_care"] },
    { name: "Primary School", types: ["primary_school"] },
    { name: "Secondary School", types: ["secondary_school"] },
    { name: "University", types: ["university", "school"] },
    { name: "Community Centre", types: ["community_center"] },
    { name: "Art Gallery", types: ["art_gallery"] },
    { name: "Movie Theatre", types: ["movie_theater"] },
    { name: "Convenience Store", types: ["convenience_store", "supermarket", "store"] },
    { name: "Gas Station", types: ["gas_station"] },
    { name: "Restaurant", types: ["restaurant", "cafe"] },
    { name: "Gym", types: ["gym"] },
    { name: "Park", types: ["park"] },
    { name: "Bus Station", types: ["bus_station"] },
    { name: "Subway Station", types: ["subway_station", "light_rail_station"] },
    { name: "Transit Station", types: ["transit_station", "train_station"] },
    { name: "ATM", types: ["atm"] },
    { name: "Bank", types: ["bank"] },
    { name: "Church", types: ["church"] },
    { name: "Mosque", types: ["mosque"] },
    { name: "Hindu Temple", types: ["hindu_temple"] },
    { name: "Synagogue", types: ["synagogue"] },
    { name: "Government Building", types: ["city_hall", "courthouse", "fire_station", "police", "post_office", "local_government_office", "embassy"] },
];

function calculateGrihaScore(location) {
    const service = new google.maps.places.PlacesService(map);
    let grihaScore = 0;
    let scoreBreakdown = "";
    let counts = {
        lessThan375m: 0,
        between375mAnd400m: 0,
    };
    const closestPlaces = {};
    const exclusionThreshold = 0.05; // 50 meters, to exclude user location from results

    // Define priority services
    const priorityServices = {
        healthcare: ["pharmacy", "doctor", "hospital", "drugstore"],
        education: ["primary_school", "secondary_school", "university", "school"],
        distribution: ["convenience_store", "supermarket", "store", "gas_station"],
        publicTransit: ["bus_station", "subway_station", "transit_station", "train_station"],
        publicServiceOffice: ["city_hall", "courthouse", "fire_station", "police", "post_office", "local_government_office", "embassy"],
        sportsAndRecreation: ["gym", "park"],
        socioCultural: ["community_center", "art_gallery", "movie_theater"],
        religiousFacilities: ["church", "mosque", "hindu_temple", "synagogue"],
        bankingFacilities: ["atm", "bank"],
    };

    function getCategoryName(types) {
        for (const [category, serviceTypes] of Object.entries(priorityServices)) {
            if (types.some(type => serviceTypes.includes(type))) {
                return category;
            }
        }
        return null;
    }

    function formatCategoryName(name) {
        return name.replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .replace(/_/g, ' ');
    }

    grihaPlaces.forEach((place) => {
        const request = {
            location,
            rankBy: google.maps.places.RankBy.DISTANCE,
            types: place.types,
        };

        service.nearbySearch(request, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
                const closestPlace = results[0];
                const distance = calculateDistance(location, closestPlace.geometry.location);

                // Exclude results that are too close to the original location (e.g., user location)
                if (distance > exclusionThreshold) {
                    const categoryName = getCategoryName(place.types);
                    if (categoryName) {
                        if (!closestPlaces[categoryName] || closestPlaces[categoryName].distance > distance) {
                            closestPlaces[categoryName] = {
                                name: closestPlace.name,
                                distance: distance,
                            };
                        }

                        if (distance < 0.375) {
                            counts.lessThan375m++;
                        } else if (distance <= 0.4) {
                            counts.between375mAnd400m++;
                        }
                    }
                }

                if (counts.lessThan375m >= 5) {
                    grihaScore = 2;
                } else if (counts.between375mAnd400m >= 5) {
                    grihaScore = 1;
                }

                scoreBreakdown = Object.entries(closestPlaces).map(([category, data]) => {
                    return `${formatCategoryName(category)}: ${data.name}\nDistance: ${data.distance.toFixed(2)} km\n`;
                }).join("\n");

                document.getElementById("griha-score").innerText =
                    `Total GRIHA Score: ${grihaScore}\n\nClosest Places:\n\n${scoreBreakdown}`;
            }
        });
    });
}

function calculateDistance(userLocation, location) {
    const rad = Math.PI / 180;
    const lat1 = userLocation.lat;
    const lon1 = userLocation.lng;
    const lat2 = location.lat();
    const lon2 = location.lng();

    const earthRadius = 6371;
    const dLat = rad * (lat2 - lat1);
    const dLon = rad * (lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(rad * lat1) * Math.cos(rad * lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadius * c;

    return distance;
}

window.initMap = initMap;
