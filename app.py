import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import hashlib

# Load environment variables
load_dotenv()

# Configure Tesseract OCR path (update for your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def is_pdf_image_based(pdf_path: str, check_pages: int = 3) -> bool:
    """
    Determine if a PDF is image-based by checking text content.
    
    Args:
        pdf_path: Path to the PDF file
        check_pages: Number of pages to check before determining
        
    Returns:
        bool: True if image-based, False if text-based
    """
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        for doc in docs[:check_pages]:
            if len(doc.page_content.strip()) > 50:  # At least 50 characters of text
                return False
        return True
    except Exception as e:
        print(f"Warning: Could not analyze {pdf_path}. Assuming image-based. Error: {str(e)}")
        return True

def extract_text_from_image_pdf(pdf_path: str) -> str:
    """
    Extract text from image-based PDF using OCR.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text or None if OCR fails
    """
    try:
        images = convert_from_path(pdf_path, dpi=300)
        full_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            full_text += f"Page {i+1}:\n{text}\n\n"
        return full_text.strip() if full_text.strip() else None
    except Exception as e:
        print(f"OCR failed for {pdf_path}: {str(e)}")
        return None

def get_content_hash(folder_path: str) -> str:
    """
    Generate a hash of all file contents in a folder to detect changes.
    
    Args:
        folder_path: Path to the folder containing documents
        
    Returns:
        str: MD5 hash of all file contents
    """
    hasher = hashlib.md5()
    for file_path in Path(folder_path).glob("*.*"):
        if file_path.is_file():
            hasher.update(file_path.name.encode())
            # Add file content to hash calculation
            try:
                with open(file_path, 'rb') as f:
                    # Read in chunks to handle large files
                    for chunk in iter(lambda: f.read(4096), b''):
                        hasher.update(chunk)
            except Exception as e:
                print(f"Warning: Could not read file {file_path}: {str(e)}")
    return hasher.hexdigest()

def load_subject_documents(subject_path: str) -> list[Document]:
    """
    Load and process all documents for a subject.
    
    Args:
        subject_path: Path to the subject folder
        
    Returns:
        list: List of processed Document objects
    """
    documents = []
    
    # Process PDF files
    for pdf_file in glob.glob(os.path.join(subject_path, "*.pdf")):
        filename = os.path.basename(pdf_file)
        try:
            if is_pdf_image_based(pdf_file):
                print(f"Processing image-based PDF: {filename}")
                ocr_text = extract_text_from_image_pdf(pdf_file)
                if ocr_text:
                    documents.append(Document(
                        page_content=ocr_text,
                        metadata={"source": pdf_file, "type": "ocr_pdf"}
                    ))
                else:
                    print(f"Failed to extract text from: {filename}")
            else:
                print(f"Processing text-based PDF: {filename}")
                loader = PyPDFLoader(pdf_file)
                docs = loader.load_and_split()
                documents.extend(docs)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Process PowerPoint files
    for ppt_file in glob.glob(os.path.join(subject_path, "*.ppt*")):
        try:
            print(f"Processing PowerPoint: {os.path.basename(ppt_file)}")
            loader = UnstructuredPowerPointLoader(ppt_file)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"Error processing PowerPoint {ppt_file}: {str(e)}")
    
    return documents

def process_subjects(base_folder: str):
    """
    Main function to process all subjects in the base folder.
    
    Args:
        base_folder: Root directory containing subject folders
    """
    # Initialize text splitter and embedding model
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create output directory if it doesn't exist
    os.makedirs("faiss_index", exist_ok=True)
    
    # Process each subject folder
    for subject in os.listdir(base_folder):
        subject_path = os.path.join(base_folder, subject)
        if not os.path.isdir(subject_path):
            continue
            
        print(f"\n{'='*40}")
        print(f"Processing subject: {subject}")
        print(f"{'='*40}")
        
        # Get content hash to detect changes
        content_hash = get_content_hash(subject_path)
        index_path = f"faiss_index/{subject}_v{content_hash}"
        
        # Skip if index already exists
        if os.path.exists(f"{index_path}.index"):
            print(f"Index already exists for {subject}. Skipping...")
            continue
            
        # Load and process documents
        documents = load_subject_documents(subject_path)
        if not documents:
            print(f"No valid documents found in {subject}")
            continue
            
        # Split documents into chunks
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} text chunks")
        
        # Create and save FAISS index
        try:
            vector_db = FAISS.from_documents(chunks, embedding_model)
            vector_db.save_local(index_path)
            print(f"Saved FAISS index to {index_path}")
            
            # Create symlink to latest version
            latest_path = f"faiss_index/{subject}_latest"
            if os.path.exists(latest_path):
                os.remove(latest_path)
            os.symlink(f"{index_path}.index", f"{latest_path}.index")
            os.symlink(f"{index_path}.pkl", f"{latest_path}.pkl")
            print(f"Created symlink: {latest_path}")
        except Exception as e:
            print(f"Error creating FAISS index: {str(e)}")

if __name__ == "__main__":
    print("Starting PDF processing pipeline...")
    PDF_BASE_PATH = r"C:\programming\resume_projects\specific_domain_chatbot\data_base_pdf"
    process_subjects(PDF_BASE_PATH)
    print("Processing complete! FAISS indices saved in 'faiss_index' folder.")