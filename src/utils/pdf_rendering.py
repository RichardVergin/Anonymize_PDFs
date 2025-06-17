from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.units import inch
import string
 
 
def draw_anonymized_pdf(layout_anonymized, output_path, add_black_bars=True):
    c = canvas.Canvas(output_path, pagesize=letter)
 
    for page in layout_anonymized:
        page_width = page['width'] * inch
        page_height = page['height'] * inch
 
        for line in page['lines']:
            text = line['content']
            x = line['polygon'][0] * inch
            y = page_height - (line['polygon'][1] * inch)  # Convert to PDF coordinate system
            font_size = 10  # You can adjust this based on polygon height if needed
            c.setFont("Helvetica", font_size)
            c.drawString(x, y, text)
       
            # Optional: draw black bars over anonymized tokens
            if add_black_bars:
                current_x = x  # Track current x position for each word
                for word in text.split():
                    # Clean word for width measurement
                    clean_word = word.strip(string.punctuation)
                    word_width = c.stringWidth(clean_word, "Helvetica", font_size)
   
                    if word.startswith("anonymized_"):
                        # Adjust bar position and size
                        bar_height = font_size * 0.9
                        bar_y_offset = font_size * 0.2
                        padding = 1  # Optional: small padding for better coverage
   
                        c.setFillColor(black)
                        c.rect(current_x - padding, y - bar_y_offset, word_width + 2 * padding, bar_height, fill=1)
                        c.setFillColorRGB(0, 0, 0)
   
                    # Move x to the next word position
                    current_x += word_width + c.stringWidth(" ", "Helvetica", font_size)
            else:
                pass        
        c.showPage()
 
    c.save()
    return None
