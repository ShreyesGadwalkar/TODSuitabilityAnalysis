# Transit-Oriented Development (TOD) Suitability Analysis

## Overview
This project aims to conduct a Transit-Oriented Development (TOD) suitability analysis in San Francisco using geospatial data. The goal is to identify parcels of land that are most suitable for TOD based on their proximity to parks, schools, and bus stops.

## Requirements
- Python 3.x
- Pandas
- GeoPandas
- Matplotlib
- Certifi (for SSL certificate verification)
- Jupyter Notebook or any Python environment

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/transit-oriented-development.git
   ```
2. Install the required Python packages:
   ```bash
   pip install pandas geopandas matplotlib certifi
   ```

## Usage
1. Ensure all required dependencies are installed.
2. Run the `main.py` script:
   ```bash
   python main.py
   ```
3. The script will perform the following tasks:
   - Download geospatial datasets for parcels, parks, schools, and bus stops in San Francisco.
   - Calculate the distance from each parcel to the nearest park, school, and bus stop.
   - Score each parcel based on its proximity to these amenities.
   - Visualize the results on a map.
   - Save the results as a Shapefile.

## Data Sources
- Parcel Data: [San Francisco Assessor-Recorder Office](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Parcels-Active-and-Retired/acdm-wktn)
- Park Data: [San Francisco Recreation & Parks Department](https://data.sfgov.org/Parks-and-Recreation/Recreation-and-Park-Department-Park-Properties/k6ts-qzbu)
- School Data: [California Department of Education](https://data.sfgov.org/Economy-and-Community/Registered-Business-Locations-San-Francisco/gtr9-ntp6)
- Bus Stop Data: [San Francisco Municipal Transportation Agency (SFMTA)](https://data.sfgov.org/Transportation/SFMTA-Stop-Information-Map/2z2v-wy2b)
