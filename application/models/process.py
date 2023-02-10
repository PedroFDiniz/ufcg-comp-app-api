import io
import hashlib

from PyPDF2 import PdfMerger, PdfWriter, PdfReader

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from application.utils.constants import VOUCHERS_GENERAL_DIR
from application.database.psql_database import get_db_connection
from werkzeug.datastructures import FileStorage

class Process:

    @staticmethod
    def save_process(process_path: str, user_email: str):
        with open(process_path, 'rb') as file:
            process = file.read()
            checksum = hashlib.md5(process).hexdigest()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO process (owner_email, checksum , path) VALUES (%s, %s, %s)', (user_email, checksum, process_path))
        conn.commit()
        cur.close()
        conn.close()

        return checksum

    @staticmethod
    def get_process_data(activities: list):
        voucher_paths = list()
        reviewers = list()
        data = [['<b>Tipo de Atividade</b>', '<b>Descrição Atividade</b>',
                 '<b>Período</b>', '<b>Créditos</b>', '<b>Comprovação</b>']]

        for index, activity in enumerate(activities):
            voucher_paths.append(activity[9])
            reviewers.append(activity[2])
            data.append([
                activity[3], # kind
                activity[8], # description
                f"{activity[5]} ", # workload + workload_unity
                str(activity[10]), # computed_credits
                f'Página {index+2}'
            ])

        return data, voucher_paths, reviewers
    @staticmethod
    def generate_table_of_contents(owner_email: str, owner_name: str, owner_enroll: str, data: list):
        user_dir = owner_email.split("@")[0]
        doc = SimpleDocTemplate(
            f"{VOUCHERS_GENERAL_DIR}/{user_dir}/table_of_contents.pdf", pagesize=letter)

        styles = getSampleStyleSheet()
        styleN = styles["Normal"]

        header_style = ParagraphStyle(name="header", fontSize=12, leading=16)
        header_name = Paragraph(f"Nome: {owner_name}", header_style)
        header_email = Paragraph(f"Email: {owner_email}", header_style)
        header_enroll = Paragraph(f"Matricula: {owner_enroll}", header_style)

        t = Table(
            [[Paragraph(cell, styleN) for cell in row] for row in data],
            colWidths=[2*inch, 2*inch, 0.9*inch, 0.8*inch, 1.2*inch]
        )

        ts = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                         ('TEXTCOLOR', (1, 1), (-2, -2), (0, 0, 0)),
                         ('VALIGN', (0, 0), (0, -1), 'TOP'),
                         ('TEXTCOLOR', (0, 0), (0, -1), (0, 0, 0)),
                         ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                         ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                         ('TEXTCOLOR', (0, -1), (-1, -1), (0, 0, 0)),
                         ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
                         ('BOX', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
                         ])

        t.setStyle(ts)

        spacer = Spacer(0, 0.5*inch)

        story = [header_name, header_email, header_enroll, spacer, t]
        doc.build(story)

    @staticmethod
    def merge_vouchers(owner_email: str, voucher_paths: str):
        user_dir = owner_email.split("@")[0]
        process_path = f"{VOUCHERS_GENERAL_DIR}/{user_dir}/process.pdf"

        vounchers = [f"{VOUCHERS_GENERAL_DIR}/{user_dir}/table_of_contents.pdf"]
        vounchers.extend(voucher_paths)

        merger = PdfMerger()
        for path in vounchers:
            merger.append(path)

        with open(process_path, 'wb') as fout:
            merger.write(fout)

        return process_path

    @staticmethod
    def generate_final_process(process_path: str, reviewers: list):
        with open(process_path, 'rb') as file:
            input_pdf = PdfReader(file)
            output_pdf = PdfWriter()

            for i in range(len(input_pdf.pages)):
                packet = io.BytesIO()
                page = input_pdf.pages[i]

                can = canvas.Canvas(packet)
                if i != 0:
                    can.drawString(50, 20, f'Validador: {reviewers[i-1]}.')

                can.drawString(500, 20, f'{i+1}')
                can.save()

                packet.seek(0)
                new_pdf = PdfReader(packet)
                page.merge_page(new_pdf.pages[0])

                output_pdf.add_page(page)

            with open(process_path, 'wb') as output:
                output_pdf.write(output)

        return process_path

    @staticmethod
    def check_process(voucher: FileStorage, user_email: str):
        print(user_email, flush=True)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"SELECT checksum FROM process WHERE owner_email = '{user_email}'")
        checksumDB = cur.fetchone()[0]

        cur.close()
        conn.close()

        checksum = hashlib.md5(voucher.read()).hexdigest()
        return checksum == checksumDB
