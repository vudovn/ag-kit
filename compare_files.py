import csv
import os
import json

def load_csv(path, base_path):
    files = {}
    # PowerShell Export-Csv with -NoTypeInformation on Windows usually results in UTF8 or Unicode
    # We'll try common encodings
    for encoding in ['utf-8-sig', 'utf-16', 'latin-1']:
        try:
            with open(path, mode='r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    full_path = row['FullName']
                    # Normalize base path case-insensitively
                    if full_path.lower().startswith(base_path.lower()):
                        rel_path = full_path[len(base_path):].lstrip('\\')
                    else:
                        rel_path = full_path
                    
                    # Store information
                    files[rel_path.lower()] = {
                        'rel_path': rel_path,
                        'full_path': full_path,
                        'length': row['Length'],
                        'last_write': row['LastWriteTime']
                    }
                return files
        except UnicodeDecodeError:
            continue
    return None

source_base = "C:\\repos\\antigravity-kit"
dest_base = "c:\\repos_pn\\antigravity-kit"

source = load_csv('source_files.csv', source_base)
dest = load_csv('dest_files_post.csv', dest_base)

if source is None or dest is None:
    print("Error: Could not load CSV files.")
    exit(1)

new_files = []
modified_files = []

for rel_path_lower, info in source.items():
    # If length is empty, it's a directory, skip for sync (we only care about files)
    if not info['length']:
        continue
        
    if rel_path_lower not in dest:
        new_files.append(info['rel_path'])
    else:
        # Compare length as primary check
        s_len = info['length']
        d_len = dest[rel_path_lower]['length']
        
        if s_len != d_len:
            modified_files.append(info['rel_path'])

# Save results to JSON for easier processing
diffs = {
    'new': new_files,
    'modified': modified_files
}

with open('file_diffs.json', 'w') as f:
    json.dump(diffs, f, indent=2)

print(f"Comparison complete. Found {len(new_files)} new files and {len(modified_files)} modified files.")
