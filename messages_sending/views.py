from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import requests
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from messages_sending.models import Message, Profile
from messages_sending.serializers import MessageSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'counter/index.html', {})


# class for display all the users through the api
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('username',)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        qs = super(ProfileViewSet, self).get_queryset()
        qs = qs.order_by("-id")
        return qs

    def get(self, request, format=None):
        # now here in your post you will be able to use `request.user` to know the user requesting this view.
        print('line567')


# class for display all the messages through the api
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('sender',)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()
        qs = qs.order_by("-id")
        return qs


@api_view(['GET'])
# login method
def login_method(request):
    if request.method == 'GET':
        user_name = request.data['username']
        password = request.data['password']

        # works only for the admin
        user = authenticate(request=request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(user_name + ' is logged in')
        return HttpResponse('cannot login')


# function for create a new message
@api_view(['POST'])
def create_message(request):
    if request.method == 'POST':
        user = Profile.objects.filter(username=request.data['sender'])[0]
        if user:
            Message.objects.create(content=request.data['content'], subject=request.data['subject'], sender=user,
                                   receiver=request.data['receiver'])

            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# helper function for get messages for specific user
def get_messages(user, read=True, type=None):
    if type == 'admin':
        user_messages = list(Message.objects.all())
    elif not read:
        user_messages = list(Message.objects.filter(sender=user).filter(read=read))
    else:
        user_messages = list(Message.objects.filter(sender=user))
    for index, msg in enumerate(user_messages):
        user_messages[index] = model_to_dict(msg)
    return user_messages


# function for get the read messages for the user
# check first if the admin is connected is if he is we get all the messages and do log out
@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def message_per_user(request):
    if request.method == 'GET':
        try:
            if request.user.is_authenticated:
                user = Profile.objects.filter(username=request.user.username)[0]
                logout(request)
                return HttpResponse(get_messages(user, type='admin'))
            else:
                user_name = request.data['username']
                user = is_user(user_name)
                if user:
                    return HttpResponse(get_messages(user))
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.ConnectionError:
            return HttpResponseNotFound('502 Bad Gateway server error response code')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('Timeout error')
        except Exception as e:
            return HttpResponseNotFound('data not found')
    return HttpResponse('None')


# helper function to check if the user is existed
def is_user(username):
    try:
        user = Profile.objects.filter(username=username)[0]
    except:
        user = None
    return user


# function for get the unread messages for the user
# check first if the admin is connected is if he is we get all the messages and do log out
@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def message_unread_per_user(request):
    if request.method == 'GET':
        try:
            if request.user.is_authenticated:
                user = Profile.objects.filter(username=request.user.username)[0]
                logout(request)
                return HttpResponse(get_messages(user, type='admin'))
            else:
                user_name = request.data['username']
                user = is_user(user_name)
                if user:
                    return HttpResponse(get_messages(user, False))
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.ConnectionError:
            return HttpResponseNotFound('502 Bad Gateway server error response code')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('Timeout error')

    return HttpResponse('None')


# function for read a specific function
@api_view(['PUT'])
def read_message(request, message_id):
    if request.method == 'PUT':
        try:
            message = Message.objects.get(id=message_id)
            if not message.read:
                message.read = True
                message.save()
                return JsonResponse(model_to_dict(message))
            return HttpResponseNotFound('message already read ' + '"' + message.content + '"')
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.ConnectionError:
            return HttpResponseNotFound('502 Bad Gateway server error response code')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('Timeout error')
    return HttpResponse('None')


# function for delete a specific message as owner and as receiver
@api_view(['DELETE'])
def delete_message(request, message_id):
    if request.method == 'DELETE':
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return HttpResponseNotFound('Message Deleted')
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.ConnectionError:
            return HttpResponseNotFound('502 Bad Gateway server error response code')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('Timeout error')
    return HttpResponse('None')
