from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO


class Command(BaseCommand):
    help = 'Dump all fixtures to its file'
    # Use Ctrl+A then Ctrl+Alt+L To Format json files in PyCharm

    def handle(self, *args, **options):
        self.wright_fixture('fixtures/app_user.json', 'app_user')
        self.wright_fixture('fixtures/project.json', 'project')

    @staticmethod
    def wright_fixture(file_name, app_name):
        buf = StringIO()
        call_command('dumpdata', app_name, stdout=buf)
        buf.seek(0)
        with open(file_name, 'w') as f:
            f.write(buf.read())
