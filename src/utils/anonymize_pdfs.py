import copy
from src.utils.doc_intelligence import extract_layout
import src.utils.anonymization as anonymize
from src.utils.pdf_rendering import draw_anonymized_pdf
 
 
def main(directory, filename, filename_output, endpoint, key, model, add_black_bars=True):
    """conduct ocr that maintains layout"""
    layout = extract_layout(
        file_name=filename,
        directory_path=directory,
        endpoint=endpoint,
        key=key
    )
   
    """anonymize text within layout"""
    layout_anonymized = copy.deepcopy(layout)
 
    # extract text in each page
    for i, page in enumerate(layout):
        for j, line in enumerate(page['lines']):
                line_anonymized = anonymize.main(
                    x=line['content'],
                    model=model
                )
                # replace anonymized text in layout
                layout_anonymized[i]['lines'][j]['content'] = line_anonymized
 
    """create pdf and store it"""
    print(f'storing anonymized pdf: {filename_output}')
    draw_anonymized_pdf(
        layout_anonymized=layout_anonymized,
        output_path=str(directory / filename_output),
        add_black_bars=add_black_bars
    )
    return None
