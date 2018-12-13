#!/usr/bin/env python
#-*- coding: utf-8 -*-
#########################################################################
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from items.models import Item

class Command(BaseCommand):
    help = 'create dev data'

#    def add_arguments(self, parser):
#        # https://docs.python.org/3/library/argparse.html#nargs
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # create user
        tom , _ = User.objects.get_or_create(
                username='tom',
                email='tom@wanderland.com')
        tom.set_password('pass1234')
        tom.save()
        mary, _ = User.objects.get_or_create(
                username='mary',
                email='mary@wonderland.com')
        mary.set_password('pass1234')
        mary.save()
        mike, _ = User.objects.get_or_create(
                username='mike',
                email='mike@wonderland.com')
        mike.set_password('pass1234')
        mike.save()
        # user create item
        tesla, _ = Item.objects.get_or_create(
                title="Tesla's giant battery saved $40M during its first year, report says'",
                url="https://electrek.co/2018/12/06/tesla-battery-report/",
                creator=tom)
        jira, _ = Item.objects.get_or_create(
                title="JIRA is an antipattern",
                url="https://techcrunch.com/2018/12/09/jira-is-an-antipattern/",
                creator=mary)
        coinbase, _ = Item.objects.get_or_create(
                title="Coinbase Abandons Cautious Approach with Plan to List Up to 30 New Currencies",
                url="https://techcrunch.com/2018/12/07/coinbase-dabbles-in-shitcoins/",
                creator=mike)
        self.stdout.write(self.style.SUCCESS('Successfully created dev data'))
