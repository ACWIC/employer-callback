import random
from datetime import datetime
from unittest import mock
from uuid import uuid4

from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_callbacks_list import GetCallbacksList

dummy_callback_id = str(uuid4())
dummy_enrolment_id = str(uuid4())
dummy_invalid_enrolment_id = str(uuid4())
dummy_shared_secret = str(uuid4())
dummy_invalid_shared_secret = str(uuid4())
dummy_received = datetime.now()
dummy_ref = "dummy_ref"
dummy_tp_ref = random.randint(0, 99999)
dummy_payload = {"data": "blbnjsd;fnbs"}


def test_get_callbacks_list_success():
    repo = mock.Mock(spec=CallbackRepo)
    callback = Callback(
        callback_id=dummy_callback_id,
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        tp_sequence=dummy_tp_ref,
        received=dummy_received,
        payload=dummy_payload,
    )

    repo.get_callbacks_list.return_value = {"callbacks_list": [callback]}
    use_case = GetCallbacksList(callback_repo=repo)
    response = use_case.execute(dummy_enrolment_id)

    assert response.type == SuccessType.SUCCESS
    assert "callbacks_list" in response.value
    assert response.value["callbacks_list"][0] == callback


def test_get_callbacks_list_failure():
    repo = mock.Mock(spec=CallbackRepo)
    repo.get_callbacks_list.side_effect = Exception()
    use_case = GetCallbacksList(callback_repo=repo)
    response = use_case.execute(dummy_enrolment_id)

    assert response.type == FailureType.RESOURCE_ERROR
