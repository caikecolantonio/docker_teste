"""
Rode esse arquivo da forma como rodaria qualquer arquivo python:
python nome_do_arquivo.py


se quiser que ele fique rodando, mas não fique preso ao seu terminal, se estiver no linux rode:
nohup python nome_do_arquivo.py &
Existem inúmeras  de executar um serviços automaticamente, e faço startar automaticamente caso ele caia.
procure WATCHDOG no Google
"""
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import time
from license.models import License
from license.models import Client

class Command(BaseCommand):
    help = 'Email sender'

    def handle(self, *args, **kwargs):

        while True:
            try:
                """  Logic for 1 week expire or already expired and is_send=false  """

                client = Client.objects.all()
                licenses = License.objects.all()
                licenses_id = []
                
                for obj_license in licenses:
                    if (timezone.now() - timedelta(days=7)) >= obj_license.expiration_datetime and obj_license.is_send is False:
                        lista = []
                        lista.append(obj_license.id)
                        lista.append(obj_license.client)
                        licenses_id.append(lista)
                        self.stdout.write(self.style.SUCCESS(obj_license.id))
                        license_instance = License.objects.get(pk=obj_license.pk)
                        license_instance.is_send = True
                        license_instance.save()
                        
                """ Logic for exactly 4 months """

                for obj_license in licenses:
                    if (timezone.now() + timedelta(days=120) ) == obj_license.expiration_datetime  and obj_license.is_send is False:
                        licenses_id.append(obj_license.id)
                        license_instance = License.objects.get(pk=obj_license.pk)
                        license_instance.is_send = True
                        license_instance.save()

                """ Logic for within a month and if today is monday"""

                today = timezone.now()
                today = today.weekday()
                todays = timezone.now()
                for obj_license in licenses:
                    if today == 0:
                        if todays <= obj_license.expiration_datetime and obj_license.is_send is False:
                            licenses_id.append(obj_license.id)
                            license_instance = License.objects.get(pk=obj_license.pk)
                            license_instance.is_send = True
                            license_instance.save()

            
                for name in licenses_id:
                    if name[1] in client:
                        owner = Client.objects.get(client_name=name[1])
                        license_owner = License.objects.get(id=name[0])
                        template = render_to_string('html/email_template.html', {'owner':owner, 'license_owner':license_owner})
                        email = EmailMessage(
                            'The cliente license met one of the criteria',
                            template,
                            settings.EMAIL_HOST_USER,
                            [owner.poc_contact_email],
                        )
                        email.fail_silently=False
                        email.send()
                        self.stdout.write(self.style.SUCCESS('Success Email Sended.'))
            except ValueError:
                self.stdout.write(self.style.ERROR('None of the clients meets the criteria'))

        time.sleep(30)
