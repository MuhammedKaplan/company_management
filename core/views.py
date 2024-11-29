from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, CheckInSerializer, LeaveRequestSerializer, CheckOutSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.employee.role == 'MANAGER':
            return Employee.objects.all()
        return Employee.objects.filter(user=self.request.user)


class CheckInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CheckInSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Check-in successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CheckOutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Check-out successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-requested_at')
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)


class LeaveRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)
            return Response({"message": "Leave request created successfully."}, status=201)
        return Response(serializer.errors, status=400)


class LeaveRequestApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, leave_request_id, status):
        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
            if status not in ['APPROVED', 'REJECTED']:
                return Response({"error": "Invalid status."}, status=400)

            if leave_request.status != 'PENDING':
                return Response({"error": "Leave request is not pending approval."}, status=400)

            leave_request.status = status
            leave_request.save()
            return Response({"message": f"Leave request {status.lower()} successfully."}, status=200)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found."}, status=404)
