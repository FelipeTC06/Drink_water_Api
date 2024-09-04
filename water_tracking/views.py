from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import WaterIntake
from user_auth.models import User_Auth
from django.utils import timezone
from django.db.models import Sum

@api_view(['POST'])
def register_intake(request):
    user_id = request.data.get('user_id')
    intake_ml = request.data.get('intake_ml')
    user = User_Auth.objects.get(id=user_id)

    WaterIntake.objects.create(user=user, intake_ml=intake_ml)
    return Response({'message': 'Intake registered successfully!'})

@api_view(['GET'])
def daily_progress(request, user_id):
    try:
        user = User_Auth.objects.get(pk=user_id)
    except User_Auth.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    daily_goal = int(user.weight) * 35

    today = timezone.now().date()
    total_intake = WaterIntake.objects.filter(user=user, date=today).aggregate(Sum('intake_ml'))['intake_ml__sum'] or 0

    remaining = max(0, daily_goal - total_intake)

    data = {
        'daily_goal': daily_goal,
        'total_intake': total_intake,
        'remaining': remaining,
        'goal_achieved': total_intake >= daily_goal,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def intake_history(request, user_id):
    user = User_Auth.objects.get(id=user_id)
    history = WaterIntake.objects.filter(user=user).values('date', 'intake_ml')

    return Response(history)
