import pymongo
import os
import io
import datetime

from application import MONGO_DB
from application.utils.constants import VOUCHERS_GENERAL_DIR

from bson.objectid import ObjectId
from werkzeug.datastructures import FileStorage
from PyPDF2 import PdfMerger, PdfWriter, PdfReader

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

DEFAULT_PROJECTION_FIELDS = {
    '_id': {"$toString": "$_id"},
    'owner_email': 1,
    'credits': 1,
    'period': 1,
    'kind': 1,
    'description': 1,
    'status': 1,
    'reviewer': 1,
    'createdTime': 1,
    'updatedTime': 1,
    'voucher': 1
}


class Activity:

    @staticmethod
    def register(owner_email: str, voucher: FileStorage, period: str, kind: str, description: str, status: str):
        try:
            user_dir = owner_email.split("@")[0]
            final_path = f'{user_dir}/{voucher.filename}'

            if not os.path.exists(f'{VOUCHERS_GENERAL_DIR}/{user_dir}'):
                os.makedirs(f'{VOUCHERS_GENERAL_DIR}/{user_dir}')

            activity = {
                'owner_email': owner_email,
                'description': description,
                'voucher': final_path,
                'period': period,
                'status': status,
                'kind': kind,
                'justify': None,
                'credits': None,
                'reviewer': None,
                'createdTime': datetime.datetime.utcnow(),
                'updatedTime': datetime.datetime.utcnow(),
            }

            MONGO_DB.activity.insert_one(activity)

            if not os.path.exists(f'{VOUCHERS_GENERAL_DIR}/{final_path}'):
                voucher.save(f'{VOUCHERS_GENERAL_DIR}/{final_path}')

        except ValueError as e:
            raise (e)

    @staticmethod
    def find(query: dict, page: int, size: int, sort: str, order: str):
        projection = DEFAULT_PROJECTION_FIELDS
        activity = MONGO_DB.activity.find(query, projection)

        if (sort and order):
            direction = pymongo.ASCENDING if order == 'asc' else pymongo.DESCENDING
            activity = activity.sort(sort, direction)
        if (page and size):
            activity = activity.limit(size).skip(page * size)

        return activity

    @staticmethod
    def find_one(query: dict):
        projection = DEFAULT_PROJECTION_FIELDS
        activity = MONGO_DB.activity.find_one(query, projection)
        return activity

    @staticmethod
    def find_one_by_id(activity_id: str):
        projection = DEFAULT_PROJECTION_FIELDS
        activity = MONGO_DB.activity.find_one(
            {'_id': ObjectId(activity_id)}, projection)
        return activity

    @staticmethod
    def update(activity_id: str, update_fields: str):
        query = {'_id': ObjectId(activity_id)}
        update_doc = {"$set": update_fields}
        activity = MONGO_DB.activity.find_one_and_update(
            query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
        return activity

    @staticmethod
    def count(query: dict):
        return MONGO_DB.activity.count_documents(query)

    @staticmethod
    def get_process_data(activities: list):
        voucher_paths = list()
        reviewers = list()
        data = [['<b>Tipo de Atividade</b>', '<b>Descrição Atividade</b>',
                 '<b>Período</b>', '<b>Créditos</b>', '<b>Comprovação</b>']]

        for index, activity in enumerate(activities):
            voucher_paths.append(activity['voucher'])
            reviewers.append(activity['reviewer'])
            data.append([
                activity['kind'],
                activity['description'],
                activity['period'],
                str(activity['credits']),
                f'Página {index+2}'
            ])

        return data, voucher_paths, reviewers

    @staticmethod
    def generate_table_of_contents(owner_email: str, owner_name: str, owner_enroll: str, data: list):
        user_dir = owner_email.split("@")[0]
        doc = SimpleDocTemplate(f"{VOUCHERS_GENERAL_DIR}/{user_dir}/table_of_contents.pdf", pagesize=letter)

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

        vounchers = [f"{user_dir}/table_of_contents.pdf"]
        vounchers.extend(voucher_paths)

        merger = PdfMerger()
        for path in vounchers:
            merger.append(f"{VOUCHERS_GENERAL_DIR}/{path}")

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
