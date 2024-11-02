# **Site Plan Analyzer**

This tool will be designed to automate the reading of architectural drawings and contextually analyse it. One major hindarance to automating is the lack of standardisation in the creation of architectural drawings. Every firm / architect creates it differently - this includes the depiction of elements, the variation in labelling and so on. We aim to solve for this subjectivity by training multiple OCR models, enabling easy green building verification. 


## **Modules Overview**  
The **Site Plan Analyzer** is divided into several **modules** to simplify the analysis process. Each module focuses on specific aspects of the site plan, ensuring that all critical parameters are covered.

| **Module**                     | **Purpose**                                      | **Sub-Components**                                     | **AI Tasks**                                          |
|---------------------------------|--------------------------------------------------|-------------------------------------------------------|------------------------------------------------------|
| **Boundaries and Site Layout**  | Define property limits and building layout.      | - Site Boundary Lines <br> - Building Footprint <br> - Setbacks | Identify perimeter lines, footprints, and setbacks. |
| **Dimensions and Measurements** | Ensure accuracy of size and layout.              | - Dimension Lines <br> - Scale                        | Extract numerical measurements and interpret scales. |
| **Structural Elements**         | Identify access points and building structure.  | - Doors <br> - Windows <br> - Walls                   | Detect arcs and lines representing openings and walls. |
| **Landscape & Environmental Features** | Monitor green infrastructure and elevation. | - Trees <br> - Vegetation <br> - Contours <br> - Paved Areas | Identify trees, contours, and paved surfaces. |
| **Utility and Service Lines**   | Verify placement of essential utilities.        | - Water Supply <br> - Electrical Lines                | Recognize utility lines and poles with labels. |
| **Annotations and Labels**      | Extract relevant information from plans.        | - Text Labels <br> - North Arrow                      | Use OCR to detect annotations and plan orientation. |
| **Non-Motorized Transport (NMT)** | Ensure sustainable transport infrastructure. | - Bicycle Parking <br> - Footpaths <br> - EV Charging Infrastructure | Identify symbols and spaces for NMT facilities. |
| **Environmental Monitoring**    | Track and assess environmental parameters over time. | - Solar Capacity <br> - Wind Flow <br> - Air/Soil Pollution | Monitor trends using IoT devices and environmental data. |

## **Use Cases**  
- **Architectural Planning:** Validate building layouts and dimensions.
- **Sustainable Certification:** Verify compliance with green building frameworks like **GRIHA**.
- **Municipal Verification:** Ensure public infrastructure requirements are met.
- **Environmental Assessment:** Track pollution and energy efficiency parameters using IoT.

## Contribution
This is a work in process and the team is in the process of building it out. We would welcome contributions from the community to do this. You can pick up any of the modules mentioned above to solve its detection in architectural drawings. 

To contribute to this project, please follow the guidelines outlined in [CONTRIBUTING.md](./CONTRIBUTING.md). Please reach out to **[meghana@peopleplus.ai](mailto:meghana@peopleplus.ai)** or **[vishnu@peopleplus.ai](mailto:vishnu@peopleplus.ai)** if you are interested in taking on any of these parts. 

## Setup

