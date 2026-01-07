import csv
import os

class DataExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, section_id, query, leads):
        """Saves section leads as CSV file."""
        if not leads:
            print(f"No leads found for section {section_id}. Skipping export.")
            return

        tag = f"{section_id}_{query.replace(' ', '_')}"
        file_path = os.path.join(self.output_dir, f"{tag}_output.csv")

        print(f"Saving {len(leads)} items to {file_path}")
        with open(file_path, "w", newline="", encoding="utf-8") as f:  
            title = leads[0].keys()
            cw = csv.DictWriter(f, title, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            cw.writeheader()
            cw.writerows(leads)

    def consolidate(self, query):
        """Merges all individual section CSVs into one master file."""
        tag = query.replace(' ', '_')
        master_file = os.path.join(self.output_dir, f"MASTER_{tag}.csv")
        all_leads = []
        seen_ids = set()

        # 1. Read all files in the output directory
        for filename in os.listdir(self.output_dir):
            if filename.endswith("_output.csv") and tag in filename:
                with open(os.path.join(self.output_dir, filename), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # 2. Final Deduplication (just in case)
                        if row['id'] not in seen_ids:
                            all_leads.append(row)
                            seen_ids.add(row['id'])

        # 3. Write the Master File
        if all_leads:
            with open(master_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=all_leads[0].keys())
                writer.writeheader()
                writer.writerows(all_leads)
            print(f"\n✨ Success! Consolidated {len(all_leads)} unique leads into {master_file}")
