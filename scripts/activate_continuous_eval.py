
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    EvaluationScheduleTask,
    HourlyRecurrenceSchedule,
    RecurrenceTrigger,
    Schedule,
)
from azure.identity import AzureDeveloperCliCredential
from dotenv import load_dotenv

load_dotenv(override=True)

AGENT_NAME = os.environ["AGENT_NAME"]
AGENT_ID = os.environ["AGENT_ID"]
EVAL_ID = os.environ["CONTINUOUS_EVAL_ID"]
MAX_TRACES = int(os.environ.get("CONTINUOUS_EVAL_MAX_TRACES", "10"))
SCHEDULE_ID = f"{AGENT_NAME}-continuous-eval"

with (
    AzureDeveloperCliCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"]
    ) as credential,
    AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=credential,
    ) as project,
    project.get_openai_client() as openai_client,
):
    evaluation = openai_client.evals.retrieve(EVAL_ID)
    print(f"Reutilizando evaluación: {evaluation.id}")
    print(
        "Configuración de datos:",
        getattr(evaluation, "data_source_config", None),
    )

    schedule = Schedule(
        display_name=f"Continuous Eval - {AGENT_NAME}",
        enabled=True,
        trigger=RecurrenceTrigger(
            interval=1,
            schedule=HourlyRecurrenceSchedule(),
        ),
        task=EvaluationScheduleTask(
            eval_id=EVAL_ID,
            eval_run={
                "eval_id": EVAL_ID,
                "name": f"Continuous trace evaluation - {AGENT_NAME}",
                "data_source": {
                    "type": "azure_ai_traces",
                    "agent_id": AGENT_ID,
                    "lookback_hours": 1,
                    "max_traces": MAX_TRACES,
                },
            },
        ),
        properties={
            "target_default": "true",
            "target_type": "AzureAITraces",
        },
    )

    result = project.beta.schedules.create_or_update(
        schedule_id=SCHEDULE_ID,
        schedule=schedule,
    )

    print(f"Programación creada/actualizada: {result.schedule_id}")
    print(f"Agente: {AGENT_ID}")
    print(f"Máximo de trazas: {MAX_TRACES}")
