from django.shortcuts import redirect, render
from django.http import request
from django.contrib import messages
import requests 
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
import datetime

from .models import Site, Page, ExceptedPages




def Index(request):

    sites = Site.objects.all().order_by('-created_at')
    pages = Page.objects.all()
    template_dir = 'pages/index.htm'
    context = {
        'sites': sites,
        'pages': pages
    }
    return render(request, template_dir, context)

def css_file(soup):
    # get the CSS files
    css_files = []

    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(url, css.attrs.get("href"))
            css_files.append(css_url)
    return css_files


def script_files(soup):
    # get the JavaScript files
    script_files = []

    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            # if the tag has the attribute 'src'
            script_url = urljoin(url, script.attrs.get("src"))
            script_files.append(script_url)
    return script_files


def aparser(request):
    if request.method == 'POST':
        # values from form
        url = request.POST.get('url')
        name = request.POST.get('name')
        max_pages = request.POST.get('max-pages')
        parse_time = request.POST.get('parse-time')
        # getting the page using python's 'requests' library
        page_source = requests.get(url)
        # passing the returned 'page_source' object, and using 'html.parser' to return bs4 object for further processing
        site_bs4 = BeautifulSoup(page_source.content, 'html.parser')
        
        # setting time limit
        current_date_and_time = datetime.datetime.now()
        seconds = parse_time
        limit = datetime.timedelta(seconds=int(seconds))
        new_time = current_date_and_time + limit
        
        if 'https' in url:
            url_s = url
            url = url[:4]+url[5:]
        else:
            url_s = url[:4] + 's' + url[4:]
        
        # creating site objects
        site = Site.objects.create(
            url=url,
            name=name
        )
        site.save()
        
        # getting the title as string
        title = re.compile('(?<=<title>)(.*)(?=</title>)')
        title_re = re.findall('(?<=<title>)(.*)(?=</title>)', page_source.text)
        title = ''.join(title_re)

        # creating the main page and saving it in to the database
        page = Page.objects.create(
                site = site,
                uri = url,
                content = site_bs4.prettify(),
                title = title
            )
        page.save()

        amount = 0
        for a_tag in site_bs4.find_all('a', href=True):

            if new_time <= datetime.datetime.now():
                messages.error(request, 'Max time limit reached!')
                return redirect('/')

            if amount == int(max_pages):
                return redirect('/')

            if '/' not in a_tag['href']:
                print('########## ', a_tag['href'])
                continue
            
            if len(a_tag['href']) < 2:
                print('########## ', a_tag['href'])
                continue
            
            try:
                # checking if the href already have the site domain
                if (url in a_tag['href']) or (url_s in a_tag['href']):
                    # checking wether the page with the uri already parsed
                    uri = a_tag['href']
                    if Page.objects.filter(uri=uri).exists():
                        continue

                    page_source = requests.get(a_tag['href'])
                    
                else:
                    # checking wether the page with the uri already parsed
                    uri = url+a_tag['href']
                    if Page.objects.filter(uri=uri).exists():
                        continue

                    page_source = requests.get(url+a_tag['href'])

                '''
                # using urljoin to make the url valid
                url = urljoin(url, a_tag['href'])
                page_source = requests.get(url)
                '''

                # checking if the pagesource is not valid text; like it is binary
                if page_source.encoding is None:
                    continue

                site_bs4 = BeautifulSoup(page_source.content, 'html.parser')

                title_re = re.findall('(?<=<title>)(.*)(?=</title>)', page_source.text)
                title = ''.join(title_re)

                page = Page.objects.create(
                    site = site,
                    uri = uri,
                    content = site_bs4.prettify(),
                    title = title,
                )
                # if css == True:
                #     page.css = css_files(site_bs4)
                # if scripts == True:
                #     page.scripts = script_files(site_bs4)
                page.save()

                amount += 1
            except:
                ePages = ExceptedPages.objects.create(
                    uri=a_tag['href'],
                    site=site
                )
                ePages.save()
                continue
        return redirect('/')

    template_dir = 'forms/use_soup.htm'
    context = {
        'text': 'text',
    }
    return render(request, template_dir, context)

def details(request, pk):
    site = Site.objects.filter(id=pk).first()
    
    pages = Page.objects.all().filter(site=site)
    template_dir = 'pages/details.htm'
    context = {
        'site': site,
        'pages': pages
    }
    return render(request, template_dir, context)
