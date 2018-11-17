
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Patient
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken

# Create your views here.


class SignUp(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = request._json_body
        u = User(
            first_name=body['fn'],
            last_name=body['ln'],
            phoneNo=body['phoneNo'],
            username=body['phoneNo']
        )
        try:
            u.save()
        except IntegrityError:
            u = User.objects.get(phoneNo=body['phoneNo'])
            # if u.status == 2:
            #     return Response({'error': 'patient already signedup'})
        u.set_password(body['password'])
        _otp = randrange(1000, 9999)
        u.otp = _otp
        u.save()
        sms_text = 'Your OTP is {otp} please use this to verify'.format(
            otp=_otp)
        send_sms(sms_text, body['phoneNo'])
        return Response({'status': 'otp sent'})


class OTPVerify(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = request._json_body
        u = User.objects.get(phoneNo=body['phoneNo'])
        if str(u.otp) != str(body['otp']):
            return Response({'error': 'otp not valid'}, 400)
        u.status = 2
        u.save()
        token, _ = MultiToken.create_token(u)
        return Response({'token': token.key})


class Login(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            _username = request._json_body['phoneNo']
            _password = request._json_body['password']
        except KeyError as e:
            raise Response(str(e) + ' is required in request body.', 400)
        _user = User.objects.get(phoneNo=_username)
        if not _user:
            raise Response('username or password seems incorrect.')
        if not _user.check_password(_password):
            locked_response = Response(
                {
                    "error": {"message": "Account Locked.", "code": -1},
                    "statusCode": 400,
                }, 400,
            )
            return locked_response
        token, _ = MultiToken.create_token(_user)
        return Response(
            {'token': token.key,
             'fn': _user.first_name,
             'ln': _user.last_name}
        )


class Me(APIView):

    def get(self, request):
        u = request.user
        res = {'fn': u.first_name,
                'ln':u.last_name,
                'status':u.status}
        return Response(res)

    def patch(self, request):
        body = request._json_body
        u = request.user
        p = Patient(
            insuaranceNo=body['insuaranceNo'],
            creditcardNo=body['creditcardNo'],
            expiryDate=body['expiryDate'],
            cvv=body['cvv'],
            pcpId=body['pcpId'],
            ssn=body['ssn'],
        )
        p.save()
        u._type = 'PAT'
        u.patient = p



        
        u.save()

        return Response({})