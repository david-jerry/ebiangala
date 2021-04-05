from celery import task
from django.core.mail import send_mail
from angalabiri.shop.models.ordermodels import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = "Order nr. {}".format(order.id)
    message = "Dear {},\n\nYou have successfully placed an order.\n\nYour order id is {}.".format(
        order.first_name, order.id
    )
    mail_sent = send_mail(subject, message, "admin@ebiangala.ng", [order.email])
    return mail_sent
