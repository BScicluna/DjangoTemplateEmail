import datetime
import traceback
from django.core.mail.backends.smtp import EmailBackend
from email_config import email_address, email_password
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

company_data = {
    "companyId": "c074feca-fd03-4620-88b4-efedc1235ad1",
    "name": "Byson Group",
    "phone": "(03) 9052 4527",
    "email": "build@byson.com.au",
    "companyAbn": "27 629 050 326",
    "addressL1": "",
    "addressL2": "",
    "addressCity": "Mulgrave",
    "addressPostCode": "3170",
    "addressState": "VIC",
    "addressCountry": "",
    "logo": "https://firebasestorage.googleapis.com/v0/b/doxle-build-98566.appspot.com/o/"
            "company%2Fbyson%2Fstorage%2Flogo_1632874290638.png?alt=media&token=27d1a49d-"
            "1eca-447e-9026-cbcc3f360c29", "owner": "6c46322b-405f-41c1-b406-2bf6f9b558c7"
}
bill_data = {
    "bill_id": "1b5fd9ea-74b4-4053-88a1-b4d60aa8dc94",
    "cost_code": "027afcf0-f47a-407a-89d5-422f0e546989",
    "number": "RIDDL2.17.002",
    "startDate": "2022-11-27",
    "endDate": "2022-10-27",
    "damages": "550.00",
    "damages_period": "Week",
    "payment_terms": 30,
    "payment_terms_suffix": "Days",
    "issueDate": "2022-04-12",
    "emailSent": True,
    "supplier": "Driptech Plumbing & Drainage",
    "abSupplier": "dd180c6c-0ad8-4d11-a082-0b14d4305fe2",
    "accepted": None,
    "sub_total": "20000.00",
    "tax": "2000.00",
    "reference": "Drainage Works",
    "total": "22000.00",
    "internalNotes": "",
    "special_conditions": "Please Let Maju Know 1 Day Before",
    "status": "D",
    "lines": [
        {
            "bill_line_id": "593eaeac-47d9-4c16-be5f-e8f1e276c269",
            "index": 0,
            "description": "Supply And Install Stormwater Drains As Per Plans",
            "item_cost": "5000.0000",
            "item_formula": "",
            "line_cost": "5000.0000",
            "quantity": "1.0000",
            "quantity_formula": "",
            "ticked": False,
            "unit": "Ea"
        },
        {
            "bill_line_id": "593eaeac-47d9-4c16-be5f-e8f1e276c269",
            "index": 1,
            "description": "Supply And Install Stormwater Drains As Per Plans",
            "item_cost": "5000.0000",
            "item_formula": "",
            "line_cost": "5000.0000",
            "quantity": "1.0000",
            "quantity_formula": "",
            "ticked": False,
            "unit": "Ea"
        },
        {
            "bill_line_id": "593eaeac-47d9-4c16-be5f-e8f1e276c269",
            "index": 2,
            "description": "Supply And Install Stormwater Drains As Per Plans",
            "item_cost": "5000.0000",
            "item_formula": "",
            "line_cost": "5000.0000",
            "quantity": "1.0000",
            "quantity_formula": "",
            "ticked": False,
            "unit": "Ea"
        },
        {
            "bill_line_id": "593eaeac-47d9-4c16-be5f-e8f1e276c269",
            "index": 3,
            "description": "Supply And Install Stormwater Drains As Per Plans",
            "item_cost": "5000.0000",
            "item_formula": "",
            "line_cost": "5000.0000",
            "quantity": "1.0000",
            "quantity_formula": "",
            "ticked": False,
            "unit": "Ea"
        }
    ],
    "history": [
        {
            "index": 0,
            "shortText": "Bill created",
            "longText": "System generated from firestore",
            "timeStamp": "2022-04-12T04:46:24.949262Z",
            "user": None
        }
    ],
    "signedOff": None,
    "approved": True,
    "approvedBy": "Ben Scicluna <ben@byson.com.au>",
    "emailAddresses": "ben@byson.com.au"
}


def send_po_email():
    to_emails = [email_address]
    email_subject = 'Test Purchase Order'
    email_body = 'MELBOURNE ENERGY RATING PTY LTD,\n\nPlease find attached purchase order: GEEL1.01.01,' \
                 ' The total value of the purchase order is $858.00.\n\nKind Regards,\n\nBen Scicluna'

    try:

        backend = EmailBackend(
            host='smtp.gmail.com',
            port=587,
            username=email_address,
            password=email_password,
            use_tls=True,
            fail_silently=False
        )

        for recipient in to_emails:
            context = {
                'body_lines': email_body.split('\n'),
                'bill_data': bill_data,
                'site_address': "Test Site Address",
                'company_data': company_data,
                'supplier_abn': "00 123 456 789",
                'accept_url': f'http://3.104.202.139:8000/po/1b5fd9ea-74b4-4053-88a1-b4d60aa8dc94/1/'
                              f'58636fc1-4ad7-4b82-a8b6-59b1520aa355/{email_address}/',
                'deny_url': f'http://3.104.202.139:8000/po/1b5fd9ea-74b4-4053-88a1-b4d60aa8dc94/0/'
                            f'58636fc1-4ad7-4b82-a8b6-59b1520aa355/{email_address}/',
                'include_buttons': True
            }

            html_message = render_to_string('email_template/po_template.html', context)
            email = EmailMultiAlternatives(
                subject=email_subject,
                body=email_body,
                to=[recipient],
                cc=[],
                bcc=[],
                from_email=email_address,
                reply_to=[email_address],
                connection=backend,
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

        return True
    except Exception as e:
        print(str(datetime.datetime.now()) + ': ' + str(e) + '\n' + traceback.format_exc())
        return False


def send_po_cancelled_email():
    try:
        to_emails = [email_address]
        backend = EmailBackend(
            host='smtp.gmail.com',
            port=587,
            username=email_address,
            password=email_password,
            use_tls=True,
            fail_silently=False
        )
        context = {
            'body': f"This is an automated method to inform you that:"
                    f"\nPurchase Order RIDDL2.17.002 has been cancelled"
                    f"\n\nIf you have any questions please Byson Group them for further information",
            'company_data': company_data,
            'bill_data': bill_data
        }
        html_message = render_to_string('email_template/po_cancel_template.html', context)
        email = EmailMultiAlternatives(
            subject=f"Purchase Order RIDDL2.17.002 Cancelled by Byson Group",
            body=f"This is an automated method to inform you that:\n"
                 f"Purchase Order RIDDL2.17.002 has been cancelled"
                 f"\n\n"
                 f"If you have any questions please Byson Group them for further information"
            ,
            to=to_emails,
            cc=[],
            bcc=[],
            from_email=email_address,
            reply_to=[email_address],
            connection=backend,
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True

    except Exception as e:
        print(str(datetime.datetime.now()) + ': ' + str(e) + '\n' + traceback.format_exc())
        return False
