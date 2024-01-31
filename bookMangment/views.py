from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render ,redirect
from .forms import *
from django.contrib import messages

from .models import *


# Create your views here.
@login_required
def index(request):
    bookList = Book.objects.all()

    context = {'bookList': bookList}

    return render(request, 'book_list.html', context)
def userRegister(request):
    if request.method == 'POST':
        print('POST')
        form = UserRegister(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            return redirect('login')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'user_register.html', context)

    elif request.method == 'GET':
        form = UserRegister()
        errorsForm = form.errors
        context={'form': form, 'errorsForm': errorsForm}
        return render(request, 'user_register.html', context)
    return render(request, 'user_register.html', {})

# def userRegister(request):
#     if request.method == 'POST':
#         form = UserRightForm(request.POST)
#         print(form)
#         context={'form': form}
#         if form.is_valid():
#             form.save()

#             return redirect('login')
#     elif request.method == 'GET':
#             form = UserRightForm()
#             context={'form': form}
#             return render(request, 'user_register.html', context)
#     return render(request, 'user_register.html', {})
def detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}

    return render(request, 'book_detail.html', context)


def home(request):
    visitCounter = request.session.get('visitCounter', 0)
    visitCounter += 1
    request.session['visitCounter'] = visitCounter
    # Staff = Group(name='Staff')
    user = request.user  #
    type = ''
    if user.groups.filter(name='staff').exists():
        type = 'staff'
    elif user.groups.filter(name='normalUser').exists():
        type = 'normalUser'
    elif user.groups.filter(name='libraryManager').exists():
        type = 'libraryManager'

    print(type)
    context = {'visitCounter': visitCounter, 'type': type}
    return render(request, 'home.html', context)


def staffPage(request):

    return render(request, 'staff.html')


def managerPage(request):

    return render(request, 'manager.html')


def userPage(request):

    return render(request, 'normal.html')


def author_list(request):
    author = Author.objects.all()
    authList = []
    for i in author:
        authList.append(i)
        auteerBook = Book.objects.filter(author=i)

        authDeatels = {'author': i, 'books': auteerBook}
        authList.append(authDeatels)
    context = {'authDeatels': authList}
    return render(request, 'authorlist.html', context)


def userBooks(request):
    user = request.user
    userBooksList = BookInstance.objects.filter(brower=user)
    context = {'userBooksList': userBooksList}
    return render(request, 'userBooks.html', context)
# views.py


from django.shortcuts import render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from social_django.models import UserSocialAuth

from .models import Playlist


def user_playlists(request):

    user_playlists = request.user.playlists.all()
    return render(request, 'user_playlists.html', {'playlists': user_playlists})
from .models import Playlist

@login_required
def playlist_videos(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, users=request.user)
        user_social_auth = UserSocialAuth.objects.get(user=request.user, provider='google-oauth2')
        credentials = Credentials(
            token=user_social_auth.extra_data['access_token'],
            refresh_token=user_social_auth.extra_data['refresh_token'],
            token_uri='https://oauth2.googleapis.com/token',
            client_id='1018666682038-9ifloj0alkpn6ct85tjse2pf0rrnnoau.apps.googleusercontent.com',  # Replace with your actual client ID
            client_secret='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'  # Replace with your actual client secret
        )

        youtube = build('youtube', 'v3', credentials=credentials)

        youtube_request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist.youtube_playlist_id,
            maxResults=25
        )
        response = youtube_request.execute()

        videos = []
        for item in response.get('items', []):
            video_id = item['contentDetails']['videoId']
            videos.append({
                'title': item['snippet']['title'],
                'video_id': video_id,
                'url': f'https://www.youtube.com/watch?v={video_id}'
            })

        return render(request, 'playlist_videos.html', {'videos': videos})
    except Playlist.DoesNotExist:
        # Handle the case where the Playlist does not exist
        return redirect('some_error_page')  # Replace with the actual URL name or path
    except UserSocialAuth.DoesNotExist:
        # Handle the case where the UserSocialAuth does not exist
        return redirect('connect_google_account')  # Replace with the actual URL name or path
    except Exception as e:
        # Handle other exceptions such as API errors
        return render(request, 'error_page.html', {'error': str(e)})  # Replace with your error handling template

# def playlist_videos(request, playlist_id):
#     playlist = Playlist.objects.get(id=playlist_id, users=request.user)
#     user_social_auth = UserSocialAuth.objects.get(user=request.user, provider='google-oauth2')
#     credentials = Credentials(
#         token=user_social_auth.extra_data['access_token'],
#         refresh_token=user_social_auth.extra_data['refresh_token'],
#         token_uri='https://oauth2.googleapis.com/token',
#         client_id='1018666682038-9ifloj0alkpn6ct85tjse2pf0rrnnoau.apps.googleusercontent.com',
#         client_secret='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'
#     )

#     youtube = build('youtube', 'v3', credentials=credentials)

#     request = youtube.playlistItems().list(
#         part='snippet,contentDetails',
#         playlistId=playlist.youtube_playlist_id,
#         maxResults=25
#     )
#     response = request.execute()

#     videos = []
#     for item in response.get('items', []):
#         video_id = item['contentDetails']['videoId']
#         videos.append({
#             'title': item['snippet']['title'],
#             'video_id': video_id,
#             'url': f'https://www.youtube.com/watch?v={video_id}'
#         })

#     return render(request, 'playlist_videos.html', {'videos': videos})
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from social_django.models import UserSocialAuth
# from django.core.exceptions import ObjectDoesNotExist
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build


# @login_required
# def playlist_videos(request, playlist_id):
#     # Get the playlist object, ensuring the user has access to it
#     playlist = get_object_or_404(Playlist, id=playlist_id, users=request.user)

#     # Fetch the videos for the playlist from your own database or another source
#     # For this example, let's assume that your Playlist model has a many-to-many relationship
#     # with a Video model, which stores video information.
#     videos = playlist.videos.all()  # Adjust this line to match your actual model relationship
# #         videos = []
# #         for item in response.get('items', []):
# #             video_id = item['contentDetails']['videoId']
# #             videos.append({
# #                 'title': item['snippet']['title'],
# #                 'video_id': video_id,
# #                 'url': f'https://www.youtube.com/watch?v={video_id}'
# #             })
#     # Prepare the context with the videos
#     context = {
#         'playlist': playlist,
#         'videos': videos,
#     }

#     # Render the playlist_videos template with the videos context
#     return render(request, 'playlist_videos.html', context)
