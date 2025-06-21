from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Asset, Notification, Violation
from .serializers import *

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

@api_view(['GET'])
def run_checks(request):
    now = timezone.now()
    fifteen_min_later = now + timedelta(minutes=15)
    notifications = []
    violations = []

    for asset in Asset.objects.all():
        # Notification 15 min before service
        if now <= asset.service_time <= fifteen_min_later:
            notif, _ = Notification.objects.get_or_create(
                asset=asset,
                notification_type='SERVICE'
            )
            notifications.append(notif)

        # Notification 15 min before expiration
        if now <= asset.expiration_time <= fifteen_min_later:
            notif, _ = Notification.objects.get_or_create(
                asset=asset,
                notification_type='EXPIRATION'
            )
            notifications.append(notif)

        # Violation if service time passed and not serviced
        if asset.service_time < now and not asset.serviced:
            violation, _ = Violation.objects.get_or_create(
                asset=asset,
                violation_type='SERVICE'
            )
            violations.append(violation)

        # Violation if expiration time passed
        if asset.expiration_time < now:
            violation, _ = Violation.objects.get_or_create(
                asset=asset,
                violation_type='EXPIRATION'
            )
            violations.append(violation)

    return Response({
        'notifications': NotificationSerializer(notifications, many=True).data,
        'violations': ViolationSerializer(violations, many=True).data,
    })
