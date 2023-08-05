import typing

from aws_cdk.aws_ec2 import IConnectable, Port
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecs import ICluster, ContainerImage, LogDriver, PortMapping, \
    Ec2Service, Ec2TaskDefinition, NetworkMode, PlacementStrategy, BuiltInAttributes
from aws_cdk.aws_iam import IRole
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Construct
from jsii import Number


class StandaloneEc2Service(Construct):
    def __init__(self, scope, id: str, *, service_name: str, cluster: ICluster, task_mem_limit_mib: Number,
                 ecr_repo_name: str, image_tag: str, desired_container_count: int,
                 environment: typing.Optional[typing.Mapping[str, str]] = None,
                 task_role: typing.Optional[IRole] = None,
                 container_port_mappings: typing.Optional[typing.List[PortMapping]] = None):
        super().__init__(scope, id)

        task_definition = Ec2TaskDefinition(scope, f'{service_name}-task-definition',
                                            network_mode=NetworkMode.BRIDGE,
                                            task_role=task_role)
        image_repo = Repository.from_repository_name(scope, f'{service_name}-repository',
                                                     repository_name=ecr_repo_name)
        container_definition = task_definition.add_container(
            f'{service_name}-container',
            image=ContainerImage.from_ecr_repository(image_repo, tag=image_tag),
            logging=LogDriver.aws_logs(stream_prefix=service_name, log_retention=RetentionDays.ONE_WEEK),
            environment=environment, memory_limit_mib=task_mem_limit_mib)
        if container_port_mappings:
            container_definition.add_port_mappings(*container_port_mappings)
        self.service = Ec2Service(scope, f'{service_name}-service', task_definition=task_definition,
                                  assign_public_ip=False, daemon=False,
                                  placement_strategies=[
                                      PlacementStrategy.spread_across(BuiltInAttributes.AVAILABILITY_ZONE,
                                                                      BuiltInAttributes.INSTANCE_ID)],
                                  cluster=cluster,
                                  desired_count=desired_container_count, min_healthy_percent=50,
                                  max_healthy_percent=100,
                                  service_name=service_name)

    @property
    def service_instance(self):
        return self.service

    def allow_connection_from(self, other: IConnectable, port: Port = None):
        connection_port = port or Port.tcp(80)
        return self.service.connections.allow_from(other, connection_port)
