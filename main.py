import json
import os
import sys
from region import SearchableRegion
from places_api import PlacesApiLeadsGenerator
from data_exporter import DataExporter

def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)

def main():
    config = load_config()

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("No API Key found. Please set the GOOGLE_MAPS_KEY environment variable.")
        sys.exit(1)

    leads_generator = PlacesApiLeadsGenerator(
        key=api_key, 
        enterprise_plan=config['enterprise_plan'], 
        budget=config['budget']
    )
    exporter = DataExporter(output_dir=config['output_directory'])

    try:
        search_region = SearchableRegion(coordinates=config['coordinates'])
        search_term = config['search_term']
        print(f"Starting search for '{search_term}' across {len(search_region.sections)} sections...")

        total = len(search_region.sections)
        for i, target_section in enumerate(search_region.sections):
            progress = ((i + 1) / total) * 100
            print(f"[{progress:.1f}%] Processing section {i+1} of {total}...")
            
            leads = leads_generator.recursive_search(search_term, target_section['coordinates'])
            exporter.save(section_id=i, query=search_term, leads=leads)
        
        print("\nSearch complete. Consolidating results...")
        exporter.consolidate(search_term)
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except KeyboardInterrupt:
        print("\nSearch cancelled by user. Saving progress...")

if __name__ == "__main__":
    main()
