import os
from gliner import GLiNER
from src.config import repo_dir
from src.utils.anonymize_pdfs import main
 
 
# example pdf file
directory = repo_dir / 'path_to_your_directory'
filename = 'your_filename.pdf'
filename_output = 'output.pdf'
 
# azure setup
endpoint = os.getenv('ENDPOINT_DOCUMENT_INTELLIGENCE'),
key = os.getenv('KEY_DOCUMENT_INTELLIGENCE')
 
# anonymization setup
model = GLiNER.from_pretrained(
    'urchade/gliner_multi_pii-v1'
)
 
 
if __name__ == '__main__':
    main(
        directory=directory,
        filename=filename,
        filename_output=filename_output,
        endpoint=endpoint,
        key=key,
        model=model,
        add_black_bars=True
    )
