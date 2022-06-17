from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from requests import request
from knox.models import AuthToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import EmployeeSerializer, AttendenceSerializer
from .models import Employee, Attendence
import jwt
import re
import datetime
from rest_framework.views import APIView


class RegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', request.data['password']):
            raise ValidationError(
                {"password": 'password at least should be 8 characters'})
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = Employee.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Credentials Not found for user')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(hours=1),  # expire after 1 hour
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'jwt': token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'you are logged out successfully',
        }
        return response


class CheckInView(APIView):
    def post(self, request):
        empId = getIdFromCookie(request)
        # emp = Employee.objects.filter(id=userId).first()
        if checkUserCheckIn(empId):
            raise ValidationError(
                {'check_in': 'can\'t make check in twice in a day'})
        check_in_time = datetime.datetime.now()
        Attendence.objects.create(emp_id=empId, check_in=check_in_time)
        return Response({"msg": "check In made at {check_in_time}"})


class CheckoutView(APIView):
    def put(self, request):
        empId = getIdFromCookie(request)
        if not checkUserCheckIn(empId):
            raise ValidationError('can\'t make check out before check In')
        check_out_time = datetime.datetime.now()
        todayAttendence = Attendence.objects.filter(emp_id_id=empId).update(
            check_out=check_out_time)
        return Response({"msg": "you checkout Successfully"})


class AttendenceHistoryView(APIView):
    def get(self, request):
        empId = getIdFromCookie(request)
        history = Attendence.objects.filter(emp_id_id=empId)
        serializer = AttendenceSerializer(history, many=True)
        return Response({'attendenceHistory': serializer.data})


# to get user Id from cookie
def getIdFromCookie(req):
    token = req.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated', 401)
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except:
        raise AuthenticationFailed('Unauthenticated')

    return payload['id']


def checkUserCheckIn(empId):
    check_in_time = datetime.datetime.now()  # get time of now
    day = check_in_time.day
    month = check_in_time.month
    year = check_in_time.year
    if Attendence.objects.filter(emp_id_id=empId,
                                 check_in__year=year, check_in__month=month, check_in__day=day).count():
        return True
    return False
