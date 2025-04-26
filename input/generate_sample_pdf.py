from fpdf import FPDF


class SamplePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Sample PDF for Markdown Extraction", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(4)

    def add_code_block(self, code):
        self.set_font("Courier", "", 10)
        self.multi_cell(0, 5, code)
        self.ln()

    def add_table(self, data):
        self.set_font("Arial", "", 10)
        col_width = self.w / 5
        for row in data:
            for item in row:
                self.cell(col_width, 10, item, border=1)
            self.ln()

    def add_link_text(self, text, link):
        self.set_font("Arial", "U", 12)
        self.set_text_color(0, 0, 255)
        self.cell(0, 10, text, ln=True, link=link)
        self.set_text_color(0, 0, 0)



pdf = SamplePDF()
pdf.add_page()

# Body text
pdf.chapter_title("1. Body Text")
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, "This is a sample body paragraph that will be used to test the OCR capabilities of the DocTR model. It simulates printed document text.")

# Document Layout
pdf.chapter_title("2. Document Layout")
pdf.multi_cell(0, 10, "Each section here should represent a distinct layout element including title, paragraphs, tables, and figures.")

# Code Block
pdf.chapter_title("3. Code Block")
code = """def greet(name):\n    print(f"Hello, {name}!")\n\ngreet('World')"""
pdf.add_code_block(code)

# Table
pdf.chapter_title("4. Table")
table_data = [["Name", "Age", "City"], ["Alice", "30", "New York"], ["Bob", "25", "Los Angeles"], ["Charlie", "35", "Chicago"]]
pdf.add_table(table_data)

# Hyperlink
pdf.chapter_title("5. Link")
pdf.add_link_text("Click here to visit OpenAI", "https://www.openai.com")

# Image
pdf.chapter_title("6. Figure")
pdf.set_font("Arial", "I", 12)
pdf.cell(0, 10, "Below is a placeholder for an image that a figure detection model should recognize.", ln=True)
pdf.image("https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png", x=10, y=pdf.get_y()+10, w=60)

# Save the PDF
pdf.output("input/example.pdf")
print("✅ PDF generated: example.pdf")