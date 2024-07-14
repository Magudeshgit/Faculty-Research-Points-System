from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import publication as publ
from authentication.models import staff
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/signin')
def home(request):
    return render(request, 'central/home.html')

def publication(request):
    return render(request, 'central/publication.html')

def publication_application(request):
    context = {'error': '', 'title': '', 'index':'', 'identification': '', 'url': '', 'authorcount': ''}
    if request.method == 'POST':
        print(request.POST)
        title = request.POST['title']
        index = request.POST['index']
        identification = request.POST['identification']
        url = request.POST['url']
        authorcount= request.POST['authorcount']
        guideid = request.POST['guideid']
        # empid = request.POST['authorid']
        authorsobj = []
        
        try:
            for i in range(1,int(authorcount)+1):
                _username = request.POST['authorid' + str(i)]
                author = staff.objects.get(username=_username)
                authorsobj.append(author)
        except ObjectDoesNotExist:
            context['error'] = f'Specified Employee ID of authors: {_username} is invalid or does not exist'
            context['title'] = title
            context['index'] = index
            context['identification'] = identification
            context['url'] = url
            context['authorcount'] = authorcount
            return render(request, 'central/publication_application.html', context)
        print(authorsobj)
            
        paper = publ.objects.create(publication=index, 
                            title=title,
                            identification = identification,
                            url=url)
        
        paper.authors.add(*authorsobj)
        paper.save()
        
    return render(request, 'central/publication_application.html', context)
