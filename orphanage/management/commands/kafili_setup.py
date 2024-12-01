import logging

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
        This command sets up the project
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-perms",
            action="store_true",
            help="If this argument is set, all permissions will be removed and recreated (This action is irreversible!!).",
        )

    def handle(self, *args, **options):
        admins_group, _created = Group.objects.get_or_create(name="ADMINS")

        # Add all available permissions to group ADMINS
        admins_group.permissions.add(
            *Permission.objects.all().values_list("id", flat=True)
        )
        try:
            superadmin = User.objects.get(username="superadmin")
            logging.warning("superuser superadmin already exists!")
        except User.DoesNotExist:
            superadmin = User(
                username="superadmin",
                email="admin@jadesystems.com",
                first_name="Super",
                last_name="User",
                is_staff=True,
                is_superuser=True,
            )
            superadmin.set_password("superadmin_pass")
            superadmin.save()
            superadmin.groups.set([admins_group])
            logging.info("superadmin was created successfully!")

        try:
            admin = User.objects.get(username="admin")
            admin.groups.add(admins_group)
            logging.warning("admin user admin already exists!")
        except User.DoesNotExist:
            admin = User(
                username="admin",
                email="admin@jadesystems.com",
                first_name="Jade",
                last_name="Administrator",
                is_staff=True,
            )
            admin.set_password("admin_1234")
            admin.save()
            admin.groups.set([admins_group])
            logging.info("admin was created successfully!")
