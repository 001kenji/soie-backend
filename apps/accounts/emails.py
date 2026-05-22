# apps/accounts/emails.py
from djoser.email import PasswordResetEmail as BasePasswordResetEmail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class PasswordResetEmail(BasePasswordResetEmail):
    
    def get_context_data(self):
        context = super().get_context_data()
        
        # Override with your frontend URL
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        # Parse frontend_url to get protocol and domain
        from urllib.parse import urlparse
        parsed = urlparse(frontend_url)
        
        context['protocol'] = parsed.scheme or 'http'
        context['domain'] = parsed.netloc or 'empty'
        
        # Build the full reset URL manually
        uid = context.get('uid', '')
        token = context.get('token', '')
        context['url'] = f"{frontend_url}/reset-password?uid={uid}&token={token}"
        
        return context
    
    def send(self, to, *args, **kwargs):
        context = self.get_context_data()
        
        html_content = render_to_string('emails/password_reset.html', context)
        
        text_content = f"""
SOIE — Password Reset

Reset your password here:
{context['url']}

This link expires in 24 hours.
        """.strip()
        
        subject = "Reset Your SOIE Password"
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@soie.com')
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()