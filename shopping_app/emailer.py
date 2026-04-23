from __future__ import annotations

import smtplib
from email.message import EmailMessage

from shopping_app.config import get_settings
from shopping_app.models import ProductCandidate


def send_recommendation_email(items: list[ProductCandidate]) -> bool:
    settings = get_settings()
    if not settings.smtp_username or not settings.smtp_app_password:
        return False

    message = EmailMessage()
    message["Subject"] = "Your shopping cart recommendations are ready"
    message["From"] = settings.email_from or settings.smtp_username
    message["To"] = settings.email_to
    lines = [
        "The shopping cart website has added the top recommended items to your cart.",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"Platform: {item.platform.value}",
                f"Title: {item.title}",
                f"Price: ${item.item_price:.2f}",
                f"Shipping: ${item.shipping_cost:.2f}",
                f"Total: ${item.total_cost:.2f}",
                f"URL: {item.url}",
                "",
            ]
        )
    message.set_content("\n".join(lines))

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as client:
        client.login(settings.smtp_username, settings.smtp_app_password)
        client.send_message(message)
    return True
