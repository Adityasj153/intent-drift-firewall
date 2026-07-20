from core.context import Context
from core.pipeline import Pipeline


def test_safe_calculator():

    pipeline = Pipeline()

    context = Context("2 + 2")

    result = pipeline.run(context)

    assert result.policy == "ALLOW"
    assert result.execution["status"] == "SUCCESS"
    assert result.result == 4