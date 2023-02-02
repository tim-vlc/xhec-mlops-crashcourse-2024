import config
from orchestration_03_machine_learning_workflow import complete_ml
from orchestration_03_machine_learning_workflow import batch_inference

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import (
   CronSchedule,
   IntervalSchedule,
)


###################################################
# Workflows orchestration with prefect : EXERCISE 4
###################################################


modeling_deployment_every_sunday = Deployment.build_from_flow(
    name="Model training Deployment",
    flow=complete_ml,
    version="1.0",
    tags=["model"],
    schedule=CronSchedule(cron="0 0 * * 0")
)


inference_deployment_every_minute = Deployment.build_from_flow(
    name="Model Inference Deployment",
    flow=batch_inference,
    version="1.0",
    tags=["inference"],
    schedule=IntervalSchedule(interval=600)
)


if __name__ == "__main__":

    print(config.DATA_DIR)
    print(config.LOCAL_STORAGE)
    print(config.TRAIN_DATA)
    print(config.TEST_DATA)
    print(config.INFERENCE_DATA)

    modeling_deployment_every_sunday.apply()
    inference_deployment_every_minute.apply()

    complete_ml(config.TRAIN_DATA, config.TEST_DATA)
    inference = batch_inference(config.INFERENCE_DATA)
