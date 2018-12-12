import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from buyer.models import Orders_Buying
from collegemart.settings import MEDIA_ROOT

def create_invoice(profile, order):
    os.environ["INVOICE_LANG"] = "en"

    client_address = "Boys Hostel, Indian Institute of Information Technology Sri City, " + ',<br/>' + "Sri City, Satyavedu Mandal, AP"
    client_zip_code = "517646"
    client_phone = str(profile.phone)
    client_email = profile.user.email

    provider_address = 'Sahara Star, Juhu ' + ',<br/>' + 'Mumbai, Near Airport'
    provider_zip_code = '400049'
    provider_phone = '022-46541799'
    provider_email = 'collegemart@gmail.com'
    payment_method = order.get_payment_type_display()

    client = Client(summary=profile.fname+" "+profile.lname, address=client_address, zip_code=client_zip_code, phone=client_phone,
                    email=client_email,)
    provider = Provider(summary='CollegeMart', address=provider_address, zip_code=provider_zip_code, phone=provider_phone,
                        email=provider_email, payment_method=payment_method,
                        )
    creator = Creator('CM')

    invoice = Invoice(client, provider, creator, str(order.id))
    invoice.currency_locale = 'en.UTF-8'
    items = Orders_Buying.objects.filter(id = order.id)
    for item in items:
        invoice.add_item(Item(item.products_selling.stock, item.products_selling.price, description=item.products_selling.pname))

    pdf = SimpleInvoice(invoice)
    pdf.gen(MEDIA_ROOT+'/orders/'+str(order.id)+".pdf", generate_qr_code=False)
