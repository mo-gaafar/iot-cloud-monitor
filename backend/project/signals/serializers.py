# Serializer for the Signal model

from rest_framework import serializers
from .models import Signal

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ('signal_id', 'signal_name', 'signal_type', 'signal_values', 'signal_timestamp')

# Serializer for the SignalAnalysis model
from rest_framework import serializers
from .models import SignalAnalysis

class SignalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalAnalysis
        fields = ('signal', 'last_analyzed', 'mean', 'median', 'mode', 'standard_deviation', 'variance', 'skewness', 'kurtosis', 'min', 'max', 'range')

# Serializer for the SignalValue model
from rest_framework import serializers
from .models import SignalValue

class SignalValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalValue
        fields = ('signal_value_id', 'signal', 'signal_value', 'signal_value_timestamp')
    
# ViewSets define the view behavior.
from rest_framework import viewsets
from .models import Signal

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer


