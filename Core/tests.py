from django.db.models import F
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from Core.models import Picture

class RaceConditionDemo(TestCase):

    def setUp(self):
        fakepic = SimpleUploadedFile('sample_pic.jpg', b'__content__')
        pic = Picture.objects.create(key='q1w2e3r4', picture=fakepic)
        self.pk = pic.pk

    def get_view_count(self):
        return Picture.objects.values_list('viewCounter', flat=True)\
                              .get(pk=self.pk)

    def test_simultaneous_access_incorrect(self):
        # thread 1
        ref1 = Picture.objects.get(pk=self.pk)
        ref1.viewCounter += 1

        # thread 2
        ref2 = Picture.objects.get(pk=self.pk)
        ref2.viewCounter += 1

        # thread 1
        ref1.save()
        # update core_picture set viewCounter=1

        # thread 2
        ref2.save()
        # update core_picture set viewCounter=1

        nviews = self.get_view_count()
        self.assertEquals(nviews, 2)

    def test_simultaneous_access_correct(self):
        # thread 1
        ref1 = Picture.objects.get(pk=self.pk)
        ref1.viewCounter = F('viewCounter') + 1

        # thread 2
        ref2 = Picture.objects.get(pk=self.pk)
        ref2.viewCounter = F('viewCounter') + 1

        # thread 1
        ref1.save()
        # update core_picture set viewCounter=viewCounter + 1

        # thread 2
        ref2.save()
        # update core_picture set viewCounter=viewCounter + 1

        nviews = self.get_view_count()
        self.assertEquals(nviews, 2)