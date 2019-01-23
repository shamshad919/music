from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from .models import Album,Song
from django.urls import reverse_lazy
from django.http import  Http404
from django.views.generic import View
from .forms import UserForm

class IndexView(generic.ListView):
    template_name='music/index.html'
    context_object_name = 'all_album'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model=Album
    template_name='music/detail.html'
def favourite(request,album_id):
    try:
        album=Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404('Album does not exist')
    try:
        select_song=album.song_set.get(pk=request.POST['song'])
    except(KeyError,Song.DoesNotExist):
        return render(request,'music/detail.html', {'album':album,'error_message':'You didnt select a valid song'})
    else:
        select_song.is_favourite=True
        select_song.save()
        return render(request,'music/detail.html',{'album':album})

class Albumcreate(CreateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']

class Albumdelete(DeleteView):
    model=Album
    success_url = reverse_lazy('index')

class UserFormView(View):
    form_class=UserForm
    template_name='music/registration_form.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False )

            username= form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user=authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index')
        return render(request,self.template_name,{'form':form})