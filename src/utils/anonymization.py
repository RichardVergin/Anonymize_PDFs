import sys
import re
import string
 
 
class SlimRegexCleaner:
    def __init__(self) -> None:
        pass
 
    def remove_iban(self, text: str):
        # Find and replace IBANs in the text with 'anonymized iban'
        ibans = re.findall(
            pattern=r"\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9A-Z]{1,4}){5,}\b",
            string=text
        )
        for iban in ibans:
            text = re.sub(pattern=iban, string=text, repl='anonymized_iban')
        return text
 
    def remove_bic(self, text: str):
        # Find and replace BICs in the text with 'anonymized bic'
        bics = re.findall(
            pattern=r"\b[A-Z]{4}[A-Z]{2}[A-Z2-9]{2}(?:[A-Z2-9]{3})?\b",
            string=text
        )
        for bic in bics:
            text = re.sub(pattern=bic, string=text, repl='anonymized_bic')
        return text
   
    def remove_blz(self, text: str):
        words = ['Bankleitzahl', 'BLZ', 'Bankltzahl']
        escaped_words = '|'.join(re.escape(word) for word in words)
       
        # Match one of the words followed by any number of digits/spaces, stopping before a German letter
        pattern = rf'({escaped_words})\s*\d+[\d\s]*(?=[A-Za-zäöüÄÖÜß])'
        text = re.sub(pattern, 'anonymized_bank_information', text, flags=re.IGNORECASE)
 
        return text
 
    def remove_kontonummer(self, text: str):
        words = ['Kontonummer', 'Kontonr.', 'Kontonr']
        escaped_words = '|'.join(re.escape(word) for word in words)
       
        # Match one of the words followed by any number of digits/spaces, stopping before a German letter
        pattern = rf'({escaped_words})\s*\d+[\d\s]*(?=[A-Za-zäöüÄÖÜß])'
        text = re.sub(pattern, 'anonymized_bank_account_number', text, flags=re.IGNORECASE)
 
        return text
 
    def remove_claimnumbers(self, text: str):
        # Prefixes and patterns to remove (extend this list as needed)
        prefixes = [
            "Schd.Nr",
            "Schd.Nr.",
            "VS-Nr",
            "Vers.-Nr",
            "Versicherungsscheinnummer",
            "Schadennummer VU",
            "Kundennummer:",
            "Versicherungsschein-Nummer:",
            "Schaden-Nr.",
            "Schadennummer:"
        ]
        escaped_prefixes = [re.escape(prefix) for prefix in prefixes]
        prefix_pattern = r'(?:' + '|'.join(escaped_prefixes) + r')'
        middle_pattern = r'[\d\s\W]*'
        as_pattern = r'(AS[\w-]*)?'
        combined_pattern = prefix_pattern + middle_pattern + as_pattern
        return re.sub(combined_pattern, ' ', text, flags=re.IGNORECASE)
 
    def remove_claimnumbers_without_prefix(self, text):
        # The pattern 'AS' optionally followed by a hyphen, other punctuation or up to two spaces, then digits
        pattern = r'AS[-\s.,;!?\'"&*(){}[\]=+<>:/\\~@#$%^|`]{0,2}\d+'
        return re.sub(pattern, 'anonymized_insurance_number', text)
   
    def remove_phoneandfax_numbers(self, text: str):
        # catch numbers that have indicator phrase like phone and fax
        # beforehand written --> should ensure to keep other numbers
        # since prhase must be written beforehand
        pattern = r'(?:phone|tel|Telefon|telefon|fax|Telefax|0049|0049/|0049:)\b[\s:.]*\+?[\s\-()/.]*\d(?:[\s\-()/.]*\d)*'  # noqa
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
 
    def remove_subsequent_special_chars(self, text: str):
        special_chars = string.punctuation
        pattern = re.compile(
            r'([' + re.escape(special_chars) + '])' + r'(?:\s*[' + re.escape(special_chars) + '])*'
        )
        return re.sub(pattern, r'\1', text)
   
    def transform(self, text):
        try:
            text_cleaned = self.remove_iban(
                text=text
            )
            text_cleaned = self.remove_bic(
                text=text_cleaned
            )
            text_cleaned = self.remove_blz(
                text=text_cleaned
            )
            text_cleaned = self.remove_kontonummer(
                text=text_cleaned
            )
            text_cleaned = self.remove_claimnumbers(
                text_cleaned
            )
            text_cleaned = self.remove_claimnumbers_without_prefix(
                text_cleaned
            )
            text_cleaned = self.remove_phoneandfax_numbers(
                text=text_cleaned
            )
            text_cleaned = self.remove_subsequent_special_chars(
                text=text_cleaned
            )
            text_cleaned = text_cleaned.strip(string.punctuation + string.whitespace)
        except TypeError:  # probably empty cell due to not working ocr
            return None
        return text_cleaned
 
def remove_entities(text, model):
    labels = [
        "person",
        "phone number",
        "address",
        "passport number",
        "email",
        "credit card number",
        "date of birth",
        "mobile phone number",
        "bank account number",
        "tax identification number",
        "identity card number",
        "national id number",
        "email address",
        "iban",
        "health insurance number",
        "insurance number",
        "landline phone number",
        "postal code",
        "passport_number",
        "fax number",
        "visa number"
    ]
   
    ents = model.predict_entities(text, labels)
    # print(ents)
 
    # filter to treshold
    ents = [ent for ent in ents if ent['score'] > 0.50]
 
    # extract label of entity and text that contains this entity
    # replace each entity with label and anonymized
    for ent in ents:
        phrase = 'anonymized_' + ent['label']
        phrase_to_remove = ent['text']
        text = text.replace(phrase_to_remove, phrase)
       
    return text
 
 
def main(x, model):
    regexcleaner = SlimRegexCleaner()
    text_cleaned = remove_entities(x, model)
    text_cleaned = regexcleaner.transform(text_cleaned)
 
    # print(text_cleaned)
    return text_cleaned
 
 
if __name__ == '__main__':
    document = sys.argv[1]
    model = sys.argv[2]
    main(
        x=document,
        model=model
    )
 
