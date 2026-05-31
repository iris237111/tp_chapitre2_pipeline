from dagster import job, op

@op
def ingest(context):
    import subprocess
    subprocess.run(["python", "pipeline/ingest.py"])
    return "done"

@op
def validate(context, start):
    import subprocess
    subprocess.run(["python", "pipeline/validate.py"])
    return "done"

@op
def transform(context, start):
    import subprocess
    subprocess.run(["dbt", "run", "--profiles-dir", "."], cwd="dbt_pipeline")
    return "done"

@op
def test_data(context, start):
    import subprocess
    subprocess.run(["dbt", "test", "--profiles-dir", "."], cwd="dbt_pipeline")

@job
def ventes_pipeline():
    test_data(transform(validate(ingest())))