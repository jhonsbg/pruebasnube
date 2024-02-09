import pytest
from src.commands.crea import Create
from src.commands.consulta import Consulta
from src.errors.errors import BadRequestException, NotFoundException
import json
from datetime import datetime, timezone, timedelta
from flask import Response

class TestConsulta():
  def test_consulta(self):
    current_utc_time = datetime.now(timezone.utc)
    dateStart = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    current_utc_time = datetime.now(timezone.utc) + timedelta(days=5)
    dateEnd = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    result = Create(
    json.loads('''
        {
            "flightId": "100",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LOW",
            "destinyCountry": "Inglaterra",
            "bagCost": 386,
            "plannedStartDate": "''' + dateStart + '''",
            "plannedEndDate": "''' + dateEnd + '''"
        }
    ''')
    ).execute()
    result_json = json.loads(result.get_data(as_text=True))

    assert isinstance(result, Response)
    assert "id" in result_json

    result_consulta = Consulta(
        result_json["id"]).execute()

    assert 'id' in result_consulta

    with pytest.raises(BadRequestException) as exc_info:
            result_consulta = Consulta(id='1').execute()

    with pytest.raises(NotFoundException) as exc_info:
            result_consulta = Consulta(id='A375562a-3850-4757-b5e3-c751b1fca0c4').execute()

    assert exc_info.type == NotFoundException
