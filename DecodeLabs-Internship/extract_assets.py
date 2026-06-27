import os
import fitz  # PyMuPDF

# This ensures the folder is created right where the script is being executed
output_dir = "docs/images"
os.makedirs(output_dir, exist_ok=True)

# File mapping configurations
extraction_map = [
    ("Project_1_Data_Cleaning.pdf", 0, "project1_dirty_data.png"),
    ("Project_2_EDA.pdf", 1, "project2_statistical_distribution.png"),
    ("Project_4_Dashboard.pdf", 0, "pbi_overview_layer.png"),
    ("Project_4_Dashboard.pdf", 0, "dashboard_banner.png"), 
    ("Project_4_Dashboard.pdf", 0, "project4_bi_architecture.png"), 
    ("Project_4_Dashboard.pdf", 1, "pbi_leakage_layer.png"),
    ("Project_4_Dashboard.pdf", 2, "pbi_channels_layer.png"),
]

print("🔍 Scanning your entire directory structure to find the project PDFs...")

# Walk through all directories recursively to find the files
file_pool = {}
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".pdf"):
            file_pool[file.lower()] = os.path.join(root, file)

print(f"🎯 Found {len(file_pool)} PDF target files in your workspace workspace.")

for base_pdf_name, page_idx, target_name in extraction_map:
    look_up_key = base_pdf_name.lower()
    
    if look_up_key in file_pool:
        resolved_path = file_pool[look_up_key]
        doc = fitz.open(resolved_path)
        
        if page_idx < len(doc):
            page = doc[page_idx]
            zoom = 2  # High resolution zoom
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Save using web-safe forward slash directory paths
            final_destination = f"{output_dir}/{target_name}"
            pix.save(final_destination)
            print(f"✅ SUCCESS: Extracted '{base_pdf_name}' -> Saved to '{final_destination}'")
        else:
            print(f"⚠️ WARNING: Page {page_idx+1} does not exist inside '{base_pdf_name}'")
        doc.close()
    else:
        print(f"❌ ERROR: Could not locate '{base_pdf_name}' anywhere in this directory tree.")

print("\n🎉 Process finished!")