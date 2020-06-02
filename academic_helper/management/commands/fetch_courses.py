import json
import random

from django.core.management import BaseCommand

from academic_helper.logic.shnaton_parser import ShnatonParser
from academic_helper.models import Course
from academic_helper.utils.logger import log

LIMIT = 50
SKIP_EXISTING = True
SHUFFLE = True


# TODO: Add arguments: src file, limit
class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("courses_2020.json", encoding="utf8") as file:
            courses = json.load(file)
        if SHUFFLE:
            random.shuffle(courses)
        fail_count = 0
        for i, course in enumerate(courses):
            if i > LIMIT:
                break
            course_number = course["id"]
            if SKIP_EXISTING:
                if Course.objects.filter(course_number=course_number).exists():
                    continue
            try:
                ShnatonParser.fetch_course(course_number)
            except Exception as e:
                log.error(f"Could'nt fetch course {course_number}: {e}")
                fail_count += 1
        print(f"Fail count:", fail_count)