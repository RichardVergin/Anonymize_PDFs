# Anonymize_PDFs

Repository that contains logic to anonymize .pdf files and keep the original structure as granular as possible.

Steps to do so:
- load .pdf file
- extract text and layout utilizing Azure document Intelligence
- anonymize text in layout utilizing regex and NER (gliner from Huggingface)
- create anonymized .pdf file utilizing open source python packages as well as layout and anonymized text.
Result file will contain original structure as well as anonymized text hinting to detected entity. E.g. richard.vergin@icloud.com would becomm emailemailemailemailemail. Text length is matched to avoid overlaps and messed up structure.
