__author__ = 'faisal'
from django.contrib.auth.models import User
from django.db.models import Q

from models import Site
from models import UserProfile


class UserProfileInstanceResource:
    def __init__(self):
        """
        :rtype: Returns the User Profile Object,Creates it
        """
        pass

    @staticmethod
    def _post(user=None):
        user = UserProfile(user=user)
        user.save()
        return user

    @staticmethod
    def _get(user=None):
        return UserProfile.objects.get(user=user)


class UserInstanceResource:
    def __init__(self):
        """
        :rtype: Returns auth user object, creates it as well
        """
        pass

    @staticmethod
    def _post(username=None, email=None, password=None, first_name=None):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.save()
        return user

    @staticmethod
    def _get(user=None, first_name=None):
        if first_name:
            return User.objects.filter(Q(email=user) and Q(first_name=first_name) and Q(username=user))
        else:
            return User.objects.get(email=user)


class SiteInstanceResource:
    def __init__(self):
        """
        :rtype: Returns the Site object,Sites as per users registering them,lists the sites,creates
        and edits the site objects
        """
        pass

    @staticmethod
    def _get(site_id=None, user=None, sitename=None):

        if site_id:
            site = Site.objects.get(id=site_id)
            return site
        if sitename:
            site = Site.objects.filter(sitename__icontains=sitename)
            return site
        if user:
            user = UserProfile.objects.get(user=user)
            site_user = user.hassites.all()
            return site_user
        else:
            site = Site.objects.all()
            return site

    @staticmethod
    def create_edit_site(form, site_id=None, user=None):
        if site_id:
            site = SiteInstanceResource()._get(site_id=site_id)
        else:
            site = Site()
        site.sitename = form.cleaned_data['sitename']
        site.url = form.cleaned_data['url']
        site.auto_test_mode = int(form.cleaned_data['auto_test_mode'])
        site.save()
        if user:
            user = UserProfileInstanceResource()._get(user=user)
            user.hassites.add(site)
            user.save()
