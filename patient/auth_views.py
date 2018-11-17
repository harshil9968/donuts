
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken
from hack.utils import notify as socket_notify
from django.db.models import Q
import time
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
            username=body['phoneNo'],
            _type='PAT'
        )

        try:
            u.save()
        except IntegrityError:
            u = User.objects.get(phoneNo=body['phoneNo'])
            if u.status == 3:
                return Response({'error': 'patient already signedup'})
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


class DoctorList(APIView):

    def get(self, request):
        user = request.user
        doctors = User.objects.filter(~Q(doctor_id=None) & Q(_type='DOC')).exclude(
            doctor__pcpId=user.patient.pcpId)

        try:
            pcp = User.objects.get(doctor__pcpId=user.patient.pcpId)

            r = {}
            r['pcp'] = {}
            r['cir'] = {}
            r['oth'] = {}
            payload = {}
            r['pcp']['head'] = 'PCP'
            r['cir']['head'] = 'You will be charged partial amount'
            r['oth']['head'] = 'You will be charged complete amount'
            r['pcp']['list'] = []
            r['cir']['list'] = []
            r['oth']['list'] = []
            payload['pcpId'] = pcp.doctor.pcpId
            payload['name'] = pcp.first_name + ' ' + pcp.last_name
            payload['rating'] = pcp.doctor.rating
            payload['price'] = pcp.doctor.price
            payload['copay'] = '0%'
            payload['speciality'] = pcp.doctor.price
            r['pcp']['list'].append(payload)
        except:
            r = {}
            payload = {}
            r['pcp'] = {}
            r['cir'] = {}
            r['oth'] = {}
            r['pcp']['head'] = 'PCP'
            r['cir']['head'] = 'You will be charged partial amount'
            r['oth']['head'] = 'You will be charged complete amount'
            r['pcp']['list'] = []
            r['cir']['list'] = []
            r['oth']['list'] = []
        for doc in doctors:
            payload = {}
            if doc.doctor.insuaranceNo == user.patient.insuaranceNo:
                payload['pcpId'] = doc.doctor.pcpId
                payload['name'] = doc.first_name + ' ' + doc.last_name
                payload['rating'] = doc.doctor.rating
                payload['price'] = doc.doctor.price
                payload['copay'] = '30%'
                payload['speciality'] = doc.doctor.speciality
                r['cir']['list'].append(payload)
            else:
                payload['pcpId'] = doc.doctor.pcpId
                payload['name'] = doc.first_name + " " + doc.last_name
                payload['rating'] = doc.doctor.rating
                payload['price'] = doc.doctor.price
                payload['copay'] = '100%'
                payload['speciality'] = doc.doctor.speciality
                r['oth']['list'].append(payload)

        return Response(r)


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
               'ln': u.last_name,
               'status': u.status}
        return Response(res)

    def patch(self, request):
        body = request._json_body
        u = request.user
        p = Patient(
            insuaranceNo=body['insuranceNo'],
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


class DoctorRequest(APIView):

    def post(self, request):
        u = request.user
        body = request._json_body
        desc = body['problemDesc']
        pcpId = body.get('pcpId', None)
        doctor = []
        if pcpId:
            type = 'SPECIFIC'
            for i in User.objects.filter(doctor__pcpId=pcpId):
                doctor.append(i.id)
        else:
            type = 'ALL'

        v = Visit(
            patient=u,
            status='PENDING',
            type=type,
            doctor=doctor
        )
        v.save()
        push_data = {
            'patientDesc': body['problemDesc'],
            'patientName': u.first_name + ' ' + u.last_name,
            'visit_id': v.id
        }

        if pcpId:
            socket_notify(push_data, channel=body['pcpId'])
        else:
            doc = User.objects.filter(_type='DOC')
            for doctor in doc:
                socket_notify(push_data, channel=doctor.id)
        print(v.id)
        return Response({})


class EndChat(APIView):

    def post(self, request):
        u = request.user
        body = request._json_body
        room = Rooms.objects.get(id=body['roomId'])
        visit = Visit.objects.get(id=room.visit_id)
        visit.status = 'ENDED'
        visit.save()
        room.status = 'INACTIVE'
        room.save()
        push_data = {
            'action': 3,
            'actionType': 'endChat'
        }
        message = Messages.objects.create(
            messageType='info',
            messageBody='visit has ended at {}'.format(
                time.strftime('%dth %b, %I:%M %p')),
            creator=u,
            room=room,
            visit=visit
        )
        for id in room.participants:
            socket_notify(push_data, channel=id)
        return Response({})
