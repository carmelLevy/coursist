from django.db import models
from django_comments.abstracts import CommentAbstractModel
from star_ratings.models import UserRating

from academic_helper.models import Course
from django.contrib.sites.models import Site


class CourseComment(CommentAbstractModel):
    is_anonymous = models.BooleanField(
        "is anonymous", default=False, help_text="Check this box if we should hide the  user name."
    )

    @property
    def get_user_name_to_show(self):
        """
        :return: The user name to be shown in the comments list - either user name or 'Anonymous'
        """
        return self.user_name if not self.is_anonymous else "Anonymous"

    def get_rating(self, rating_dummy):
        semester_rating = UserRating.objects.filter(user=self.user, rating__object_id=rating_dummy.id)
        if len(semester_rating) == 1:
            return semester_rating[0]
        return None

    @property
    def semester_rating(self):
        course = Course.objects.get(pk=self.object_pk)
        return self.get_rating(course.semester_rating)

    @property
    def finals_rating(self):
        course = Course.objects.get(pk=self.object_pk)
        return self.get_rating(course.finals_rating)

    @property
    def interesting_rating(self):
        course = Course.objects.get(pk=self.object_pk)
        return self.get_rating(course.interesting_rating)

    @property
    def get_unique_url(self):
        current_site = Site.objects.get_current().domain
        print(f'url = {current_site}comment/{self.id}')
        return f"{current_site}"
