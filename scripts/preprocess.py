#!/usr/bin/env python3
"""CLI script to preprocess all educational PDFs and build FAISS indices."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.preprocessing import preprocess_all_subjects

if __name__ == "__main__":
    print("Starting preprocessing of all subjects...")
    preprocess_all_subjects("../educational_pdf")
    print("Preprocessing completed.")
