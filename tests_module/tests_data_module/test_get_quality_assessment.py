import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_file import _get_quality_assessment

class TestGetQualityAssessment:
    
    def test_get_quality_assessment_excellent(self):
        """
        Тест, который проверяет оценку 'ОТЛИЧНО' 
        для низких значений ошибок
        """
        assert _get_quality_assessment(1.5) == "ОТЛИЧНО"
        assert _get_quality_assessment(0.0) == "ОТЛИЧНО"
        assert _get_quality_assessment(1.9) == "ОТЛИЧНО"
    
    def test_get_quality_assessment_good(self):
        """
        Тест, который проверяет оценку 'ХОРОШО' 
        для средних значений ошибок
        """
        assert _get_quality_assessment(2.0) == "ХОРОШО"
        assert _get_quality_assessment(3.5) == "ХОРОШО"
        assert _get_quality_assessment(4.9) == "ХОРОШО"
    
    def test_get_quality_assessment_average(self):
        """
        Тест, который проверяет оценку 'СРЕДНЕ' 
        для повышенных значений ошибок
        """
        assert _get_quality_assessment(5.0) == "СРЕДНЕ"
        assert _get_quality_assessment(7.5) == "СРЕДНЕ"
        assert _get_quality_assessment(9.9) == "СРЕДНЕ"
    
    def test_get_quality_assessment_poor(self):
        """
        Тест, который проверяет оценку 'ПЛОХО' 
        для высоких значений ошибок
        """
        assert _get_quality_assessment(10.0) == "ПЛОХО"
        assert _get_quality_assessment(15.5) == "ПЛОХО"
        assert _get_quality_assessment(100.0) == "ПЛОХО"
    
    def test_get_quality_assessment_negative(self):
        """
        Тест, который проверяет обработку отрицательных 
        значений ошибок
        """
        assert _get_quality_assessment(-1.0) == "ОТЛИЧНО"  # отрицательные считаются отличными