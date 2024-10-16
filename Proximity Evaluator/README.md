# **Proximity Score Calculator**  
The **Proximity Score Calculator** is a **web-based tool** designed to assess the accessibility of key services and amenities based on a user-defined location. It follows the principles of the **Green Rating for Integrated Habitat Assessment (GRIHA)**, which promotes sustainable and well-planned urban development. 

Using the **Google Maps API**, the tool evaluates proximity to essential amenities, allowing users to make informed decisions about residential, commercial, or business locations based on convenience, accessibility, and sustainability.

## **Features**  
The tool calculates the distance from the user’s location to the nearest essential services, including:

- **Medical Facilities:**  
  - Hospitals  
  - Pharmacies  
  - Doctors, Physiotherapists, and Veterinary Care  

- **Transport & Connectivity:**  
  - Train Stations  
  - Subway Stations  
  - Taxi Stands  

- **Entertainment & Leisure:**  
  - Shopping Malls  
  - Movie Theatres  
  - Art Galleries  
  - Parks & Gyms  

- **Public Services:**  
  - Police Stations, Fire Stations, Post Offices, and City Halls  

- **Education & Finance:**  
  - Schools and Universities  
  - Banks and ATMs  

- **Religious & Dining Spaces:**  
  - Religious Places  
  - Restaurants and Cafes  


## **How It Works**  
The **Proximity Score Calculator** leverages the **Google Maps API** to:  
1. Take a **user-defined location** as input (coordinates or address).  
2. Compute the distance from that location to the nearest essential services.  
3. Display proximity scores, providing insights for sustainable and convenient living or business location selection.  

[Video Walkthrough]()

## **Getting Started**

### **Prerequisites**
- **Google Maps API Key:** You will need an active **Google Maps API key** to use the tool. 

### **Setup Instructions**  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/PeoplePlusAI/GreenTrack.git
   cd GreenTrack
   cd ProximityScoreCalculator
   ```
2. **Replace the API Key:**  
   - **Edit** the following files to replace the placeholder with your **API key**:  
     - **`script.js`** (Line 7)  
     - **`proxeval.html`** (Line 26)  
   ```javascript
   const apiKey = 'YOUR_API_KEY_HERE';  // script.js: Line 7
   ```
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE"></script>  <!-- proxeval.html: Line 26 -->
   ```

3. **Open the Application Locally:**  
   - Open **`proxeval.html`** in your web browser to start using the tool.
