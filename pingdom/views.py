import urllib2

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, TemplateView
from models import SiteLog
import datetime

from api import UserProfileInstanceResource, UserInstanceResource, SiteInstanceResource
from forms import AddTest, RegisterForm, LoginForm, EditForm


class DashboardView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/?login')
        name = request.GET.get('name','')    
        if name:
            site_user = SiteInstanceResource()._get(sitename=name)
        else:
            site_user = SiteInstanceResource()._get(user=request.user)
        new_site_user = []
        for key in reversed(site_user):
            new_site_user.append(key)
        page_num = request.GET.get('page', '1')
        paginator = Paginator([], 6)
        paginator.object_list = new_site_user
        try:
            pageno = paginator.page(page_num)
        except:
            pageno = ''       
        if request.is_ajax():
            self.template_name = 'index_ajax.html'
            context = {'site_user': site_user, 'pageno': pageno}
            return self.render_to_response(context)
        site_count = SiteInstanceResource()._get(user=request.user).count()
        testsuc_list = []
        testfail_list = []
        mailsent_list = []
        for items in site_user:
            testsuc_list.append(items.testsuc)
            testfail_list.append(items.testfail)
            mailsent_list.append(items.mailsent)
        context = {'pageno': pageno, 'site_user': site_user, 'site_count': site_count, 'testsuc': sum(testsuc_list),
                   'testfail': sum(testfail_list), 'mailsent': sum(mailsent_list), 'request_path': request.path}
        return self.render_to_response(context)


def run_test(request, id=1):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/?login')

    site = SiteInstanceResource()._get(site_id=id)
    try:
        urllib2.urlopen(site.url)
        site.date = timezone.now()
        site.testsuc += 1
        site.save()
        site_log = SiteLog()
        site_log.site = site
        site_log.month = str(datetime.datetime.now().strftime('%B'))
        site_log.save()
        return render(request, 'run_test.html', {'site': site})
    except urllib2.HTTPError, error:
        site.date = timezone.now()
        site.testfail += 1
        site.save()
        site_log = SiteLog()
        site_log.site = site
        site_log.month = str(datetime.datetime.now().strftime('%B'))
        site_log.save()
        return render(request, 'run_test.html', {'error': error, 'site': site})
    except urllib2.URLError, error:
        site.date = timezone.now()
        site.testfail += 1
        site.save()
        site_log = SiteLog()
        site_log.site = site
        site_log.month = str(datetime.datetime.now().strftime('%B'))
        site_log.save()
        return render(request, 'run_test.html', {'error': error, 'site': site})


def send_email(request, id=1):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/?login')

    site = SiteInstanceResource()._get(site_id=id)
    INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL = 'email_templates/url_mail_error.html'
    try:
        urllib2.urlopen(site.url)
    except urllib2.URLError, error:
        site_url = site.url
        subject = "Please Check this Url Is Down This Time"
        body = 'Error:', error
        inbox_body = render_to_string(INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL,
                                      {'site_user': request.user.email, 'Subject': subject, 'error': error,
                                       'url': site.url})
        emailmsg = EmailMultiAlternatives(subject, inbox_body, 'faisalbhattt239@gmail.com', [request.user.email,])
        emailmsg.attach_alternative(inbox_body, "text/html")
        emailmsg.send()
        site.mailsent += 1
        site.save()
        site_log = SiteLog()
        site_log.site = site
        site_log.month = str(datetime.datetime.now().strftime('%B'))
        site_log.save()
        return HttpResponse()
    except urllib2.HTTPError, error:
        site_url = site.url
        subject = "Please Check this Url Is Down This Time"
        body = 'Error:', error
        inbox_body = render_to_string(INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL,
                                      {'site_user': request.user.email, 'Subject': subject, 'error': error,
                                       'url': site.url})
        emailmsg = EmailMultiAlternatives(subject, inbox_body, 'faisalbhattt239@gmail.com', [request.user.email,])
        emailmsg.attach_alternative(inbox_body, "text/html")
        emailmsg.send()
        site.mailsent += 1
        site_log = SiteLog()
        site_log.site = site
        site_log.month = str(datetime.datetime.now().strftime('%B'))
        site_log.save()
        return HttpResponse()


def test_report(request):
    try:
        username = UserProfileInstanceResource()._get(user=request.user)
    except:
        return HttpResponseRedirect('/?login')
    if username:
        site_user = username.hassites.all()
    return render(request, 'report.html', {'site_user': site_user})


def about(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/?login')
    return render(request, 'about.html', {'request': request.path})


def site_detail(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/?login')
    site = SiteInstanceResource()._get(site_id=id)
    total_tests = int(site.testsuc) + int(site.testfail)
    data = {'testsuc': site.testsuc, 'testfail': site.testfail, 'sitename': site.sitename, 'mailsent': site.mailsent,
            'datetime': site.date, 'total_tests': total_tests}
    return render(request, 'last_details.html', {'data': data})


def edit_user(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/?login')
    user = UserInstanceResource()._get(user=request.user.email)
    data = {
        'username': user.first_name,
        'email': user.email,
    }
    if request.POST:
        form = EditForm(request.POST)
        if request.POST['username'] == data['username'] and request.POST['email'] == data['email']:
            return render(request, 'edit_user.html', {'form': form, 'request': request.path, 'checked': True})
        if form.is_valid():
            user.first_name = form.cleaned_data['username']
            user.username = form.cleaned_data['email']
            user.email = form.cleaned_data['email']
            user.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = EditForm(data)
    return render(request, 'edit_user.html', {'form': form, 'request': request.path})


class CreateEditSiteView(TemplateResponseMixin, View):
    template_name = "site_register.html"
    form_class = AddTest

    def get(self, request):
        template_values = {}
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/?login')
        if request.GET.has_key("delete_site_id"):
            delete_site_id = request.GET['delete_site_id']
            site = SiteInstanceResource()._get(site_id=delete_site_id)
            site.delete()
            return HttpResponseRedirect('/dashboard')
        if request.GET.has_key("auto_test_mode"):
            site_id = request.GET['site_id']
            auto_test_mode = request.GET['auto_test_mode']
            site = SiteInstanceResource()._get(site_id=site_id)
            site.auto_test_mode = int(auto_test_mode)
            site.save()
            return HttpResponse('ok')
        if request.GET.has_key("site_id"):
            params = {'edit': True}
            site_id = request.GET["site_id"]
            site = SiteInstanceResource()._get(site_id=site_id)
            data = {
                'sitename': site.sitename,
                'url': site.url,

            }
            if site.auto_test_mode == True:
                data['auto_test_mode'] = 1
            else:
                data['auto_test_mode'] = 0
            template_values['form'] = self.form_class(data)
            template_values['params'] = params
            return self.render_to_response(template_values)
        else:
            template_values['form'] = self.form_class()
            template_values['request_path'] = request.path
            return self.render_to_response(template_values)

    def post(self, request):
        data = request.POST.copy()
        form = self.form_class(data)
        if form.is_valid():
            try:
                site_id = request.GET['site_id']
            except:
                site_id = None
            SiteInstanceResource().create_edit_site(form, site_id, user=request.user)
            return HttpResponseRedirect('/dashboard')

        else:
            return self.render_to_response({
                'form': form,
                'request_path':request.path,
            })


class LoginRegisterUserView(TemplateResponseMixin, View):
    template_name = "signin.html"

    def get(self, request):
        if request.GET.has_key('logout'):
            if request.user.is_authenticated():
                logout(request)
            return HttpResponseRedirect('/?login')
        if request.user.is_authenticated():
            return HttpResponseRedirect('/dashboard')
        if request.GET.has_key('register'):
            self.form_class = RegisterForm
            template_values = {}
            template_values['form'] = self.form_class()
            return self.render_to_response(template_values)
        else:
            self.form_class = LoginForm
            template_values = {}
            template_values['form'] = self.form_class()
            return self.render_to_response(template_values)

    def post(self, request):
        data = request.POST.copy()
        if request.GET.has_key('register'):
            form_class = RegisterForm
            self.form_class = form_class
        else:
            form_class = LoginForm
            self.form_class = form_class
        form = self.form_class(data)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if request.GET.has_key('register'):
                first_name = form.cleaned_data['username']
                if UserInstanceResource()._get(user=email, first_name=first_name):
                    not_register = True
                    return render(request, 'signin.html', {'form': form, 'not_register': not_register})
                email = UserInstanceResource()._post(username=email, email=email, password=password,
                                                     first_name=first_name)
                UserProfileInstanceResource()._post(user=email)
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                error = True
                return render(request, 'signin.html', {'form': form, 'error': error})
        else:
            return self.render_to_response({
                'form': form,
            })
