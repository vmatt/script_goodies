from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, ECS, AutoScaling
from diagrams.aws.database import RDS, RDSInstance
from diagrams.aws.network import ELB
from diagrams.aws.general import Client
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.network import Route53
from diagrams.aws.devtools import Codecommit

with Diagram("Flask Web Application Architecture", show=False):
	user = Client("User")

	with Cluster("AWS Cloud"):
		dns = Route53("DNS")

		with Cluster("Web Tier"):
			load_balancer = ELB("Load Balancer")
			auto_scaling_group = AutoScaling("Auto Scaling Group")
			web_server = EC2("Flask Web Server")

		with Cluster("Database Cluster"):
			db_primary = RDSInstance("RDS Postgres Primary")
			db_secondary = RDSInstance("RDS Postgres Replica")

		with Cluster("Cache Cluster"):
			redis = RDS("Redis Cluster")

	user >> dns
	dns >> load_balancer
	auto_scaling_group >> load_balancer
	auto_scaling_group >> web_server
	web_server >> db_primary
	db_primary - Edge(style="dashed") >> db_secondary
	web_server >> redis
