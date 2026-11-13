
import json
import os
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentTaxonomyInput,
    AzureAIAgentTarget,
    EvaluationTaxonomy,
    RiskCategory,
)
from azure.identity import AzureDeveloperCliCredential
from dotenv import load_dotenv

load_dotenv()

agent_name = os.environ["AGENT_NAME"]
endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    AzureDeveloperCliCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"]
    ) as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
    ) as project,
    project.get_openai_client() as client,
):
    # Obtener la versión existente del agente
    versions = list(project.agents.list_versions(
        agent_name=agent_name,
        order="desc",
        limit=1,
    ))
    if not versions:
        raise RuntimeError("No se encontró una versión del agente")

    target = AzureAIAgentTarget(
        name=agent_name,
        version=versions[0].version,
    )
    print(f"Agente: {agent_name}, versión: {versions[0].version}")

    # Definir qué riesgos queremos evaluar
    evaluation = client.evals.create(
        name=f"Red Team - {agent_name} - {int(time.time())}",
        data_source_config={
            "type": "azure_ai_source",
            "scenario": "red_team",
        },
        testing_criteria=[
            {
                "type": "azure_ai_evaluator",
                "name": "Prohibited Actions",
                "evaluator_name": "builtin.prohibited_actions",
                "evaluator_version": "1",
            },
            {
                "type": "azure_ai_evaluator",
                "name": "Sensitive Data Leakage",
                "evaluator_name": "builtin.sensitive_data_leakage",
                "evaluator_version": "1",
            },
        ],
    )
    print(f"Evaluación creada: {evaluation.id}")

    # Generar objetivos de ataque
    taxonomy = project.beta.evaluation_taxonomies.create(
        name=agent_name,
        taxonomy=EvaluationTaxonomy(
            description="Prueba formativa de Red Teaming",
            taxonomy_input=AgentTaxonomyInput(
                risk_categories=[RiskCategory.PROHIBITED_ACTIONS],
                target=target,
            ),
        ),
    )
    print(f"Taxonomía creada: {taxonomy.id}")

    # Ejecutar el escaneo
    run = client.evals.runs.create(
        eval_id=evaluation.id,
        name="Red Team - Primera prueba",
        data_source={
            "type": "azure_ai_red_team",
            "item_generation_params": {
                "type": "red_team_taxonomy",
                "attack_strategies": ["Flip", "Base64"],
                "num_turns": 1,
                "source": {
                    "type": "file_id",
                    "id": taxonomy.id,
                },
            },
            "target": target.as_dict(),
        },
    )

    print(f"Escaneo iniciado: {run.id}")
    print(f"Estado: {run.status}")

    # Consultar el estado de la ejecución
    for _ in range(60):
        run = client.evals.runs.retrieve(
            run_id=run.id,
            eval_id=evaluation.id,
        )
        if run.status in ("completed", "failed", "canceled"):
            break
        time.sleep(5)

    print(f"Estado final consultado: {run.status}")

    if run.status == "completed":
        items = list(client.evals.runs.output_items.list(
            run_id=run.id,
            eval_id=evaluation.id,
        ))

        Path("results").mkdir(exist_ok=True)
        output_file = Path("results/red_team_results.json")
        output_file.write_text(
            json.dumps(
                [
                    item.model_dump(mode="json")
                    if hasattr(item, "model_dump")
                    else str(item)
                    for item in items
                ],
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        print(f"Resultados guardados: {output_file}")
    else:
        print("Revisa el estado y los errores de la ejecución en Foundry.")