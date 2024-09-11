

from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['first_name', 'email', 'mobile_number']

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError({"email": "Email is required."})
        if not data.get('mobile_number'):
            raise serializers.ValidationError({"mobile_number": "Mobile number is required."})
        return data
