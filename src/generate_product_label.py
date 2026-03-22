import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit

# ================= CONFIG =================
CSV_FILE = "data/my_barcode_product.csv"
OUTPUT_PDF = "my_barcode_product.pdf"

COLS = 4
ROWS = 12


PAGE_WIDTH, PAGE_HEIGHT = A4

print(PAGE_WIDTH, PAGE_HEIGHT)

LEFT_MARGIN = 10 * mm
TOP_MARGIN = 5 * mm

LABEL_WIDTH = PAGE_WIDTH / COLS
LABEL_HEIGHT = (PAGE_HEIGHT - 50)/ ROWS


NAME_FONT = "Helvetica-Bold"
NAME_FONT_SIZE = 10

BARCODE_FONT_SIZE = 8
BARCODE_HEIGHT = 4.5 * mm
BARCODE_BAR_WIDTH = 0.8
# =========================================


def read_products(csv_file):
    products = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                "name": row["name"].strip(),
                "barcode": row["barcode"].strip()
            })
    return products


def generate_pdf(products, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)

    labels_per_page = COLS * ROWS

    for idx, product in enumerate(products):
        pos = idx % labels_per_page

        if pos == 0 and idx > 0:
            c.showPage()

        col = pos % COLS
        row = pos // COLS


        # #%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
        x = col * LABEL_WIDTH + LEFT_MARGIN
        y = PAGE_HEIGHT - ((row + 1) * LABEL_HEIGHT) + TOP_MARGIN

        # ---- Draw label border ----
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(
            x - 15,
            y - 25,
            LABEL_WIDTH - LEFT_MARGIN , #(LEFT_MARGIN * 2),
            LABEL_HEIGHT - TOP_MARGIN,
            stroke=1,
            fill=0
        )

        # #%%%%%%%%%%%%%%%%%%%%%%%%%%%%5

        if col == 0:
            used_left_margin = LEFT_MARGIN
        else:
            used_left_margin = LEFT_MARGIN/2

        x = col * LABEL_WIDTH + used_left_margin
        y = (row+1) * LABEL_HEIGHT #+ TOP_MARGIN #PAGE_HEIGHT - ((row + 1) * LABEL_HEIGHT) + TOP_MARGIN

        # updated fornt logic
        c.setFont(NAME_FONT, NAME_FONT_SIZE)

        max_text_width = LABEL_WIDTH - (used_left_margin * 2)
        text_lines = simpleSplit(
            product["name"],
            NAME_FONT,
            NAME_FONT_SIZE,
            max_text_width
        )

        line_height = NAME_FONT_SIZE + 2
        start_y = y + BARCODE_HEIGHT - 12#+ LABEL_HEIGHT - 12

        # Limit lines to avoid barcode collision (optional safety)
        max_lines = 2
        text_lines = text_lines[:max_lines]

        for i, line in enumerate(text_lines):
            c.drawCentredString(
                x + (LABEL_WIDTH / 2) - used_left_margin,
                start_y - (i * line_height) + BARCODE_HEIGHT,
                line
            )

        # ---------- Product Name ----------
        # c.setFont(NAME_FONT, NAME_FONT_SIZE)
        # c.drawCentredString(
        #     x + (LABEL_WIDTH / 2) - LEFT_MARGIN,
        #     y + BARCODE_HEIGHT , #+ 12,#+ LABEL_HEIGHT, #+ LABEL_HEIGHT - 12,
        #     product["name"]
        # )

        # ---------- Barcode ----------
        barcode = code128.Code128(
            product["barcode"],
            barHeight=BARCODE_HEIGHT,
            barWidth=BARCODE_BAR_WIDTH
        )

        barcode_x = x + (LABEL_WIDTH - barcode.width) / 2 - used_left_margin
        barcode_y = y - 16

        barcode.drawOn(c, barcode_x, barcode_y)

        # ---------- Barcode Text ----------
        c.setFont("Helvetica", BARCODE_FONT_SIZE)
        c.drawCentredString(
            x + (LABEL_WIDTH / 2) - used_left_margin,
            barcode_y - ( BARCODE_HEIGHT / 2 )- 1 ,
            product["barcode"]
        )

    c.save()


if __name__ == "__main__":
    products = read_products(CSV_FILE)
    generate_pdf(products, OUTPUT_PDF)
    print("PDF generated successfully:", OUTPUT_PDF)
