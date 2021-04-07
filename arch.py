from diagrams import Diagram
from diagrams.aws.compute import Lambda, ECS
from diagrams.aws.devtools import Codebuild
from diagrams.aws.integration import Eventbridge
from diagrams.aws.database import Dynamodb, Timestream
from diagrams.onprem.client import User

with Diagram("SLO Infrastructure", direction="TB"):
  ci = Codebuild("CI/CD")
  producer = Eventbridge("Event Bus")
  function = Lambda("Event Handler")
  event_store = Dynamodb("EventStore")
  series_store = Timestream("SLO/Events")
  stores = [event_store, series_store]
  grafana = ECS("Dashboard")

  user = User()

  ci >> producer >> function >> stores
  user >> grafana >> series_store
