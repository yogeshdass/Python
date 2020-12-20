from kubernetes.client.models import V1Deployment, V1ObjectMeta, V1DeploymentSpec, V1LabelSelector, V1DeploymentStrategy, V1PodTemplateSpec, V1PodSpec, V1Container, V1EnvFromSource, V1ConfigMapEnvSource, V1ContainerPort, V1ResourceRequirements, V1VolumeMount, V1LocalObjectReference, V1Volume, V1HostPathVolumeSource
from kubernetes.client.api_client import ApiClient
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api.apps_v1_api import AppsV1Api
from kubernetes.config import kube_config

from json import dumps
from yaml import dump

def create_deploy():

    """
    Reference :
    lib/python3.8/site-packages/kubernetes/client/models/v1_deployment.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_object_meta.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_deployment_spec.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_label_selector.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_deployment_strategy.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_pod_template_spec.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_pod_spec.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_container.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_env_from_source.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_config_map_env_source.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_container_port.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_resource_requirements.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_volume_mount.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_local_object_reference.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_volume.py
    lib/python3.8/site-packages/kubernetes/client/models/v1_host_path_volume_source.py
    lib/python3.8/site-packages/kubernetes/client/api_client.py
    lib/python3.8/site-packages/kubernetes/config/kube_config.py
    lib/python3.8/site-packages/kubernetes/client/api/core_v1_api.py
    lib/python3.8/site-packages/kubernetes/client/api/apps_v1_api.py
    """
    return V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=V1ObjectMeta(
            name="yogesh",
            labels=dict({'app': 'yogesh'})
        ),
        spec=V1DeploymentSpec(
            replicas=1,
            revision_history_limit=3,
            selector=V1LabelSelector(
                match_labels=dict({'app': 'yogesh'})
            ),
            strategy=V1DeploymentStrategy(
                type="Recreate"
            ),
            template=V1PodTemplateSpec(
                metadata=V1ObjectMeta(
                    labels=dict({'app': 'yogesh'})
                ),
                spec=V1PodSpec(
                    containers=[
                        V1Container(
                            env_from=[
                                V1EnvFromSource(
                                    config_map_ref=V1ConfigMapEnvSource(
                                        name="yogesh"
                                    )
                                )
                            ],
                            image="tomcat:latest",
                            image_pull_policy="Always",
                            name="yogesh",
                            ports=[
                                V1ContainerPort(
                                    container_port=8080,
                                    protocol="TCP"
                                )
                            ],
                            resources=V1ResourceRequirements(
                                limits=dict(
                                    {
                                        'memory': '2500Mi'
                                    }
                                ),
                                requests=dict(
                                    {
                                        'cpu': '200m',
                                        'memory': '800Mi'
                                    }
                                )
                            ),
                            volume_mounts=[
                                V1VolumeMount(
                                    mount_path="/log",
                                    name="yogesh"
                                )
                            ]
                        )
                    ],
                    image_pull_secrets=[
                        V1LocalObjectReference(
                            name="docker-registry-credentials"
                        )
                    ],
                    node_selector=dict(
                        {
                            'nodeType': 'worker',
                            'kubernetes.io/hostname': 'worker1'
                        }
                    ),
                    termination_grace_period_seconds=300,
                    volumes=[
                        V1Volume(
                            host_path=V1HostPathVolumeSource(
                                path="/logs",
                                type="Directory"
                            ),
                            name="yogesh"
                        )
                    ]
                )
            )
        )
    )

def main():
    print(dumps(ApiClient().sanitize_for_serialization(create_deploy())))
    print(dump(ApiClient().sanitize_for_serialization(create_deploy())))
    
    kube_config().load_kube_config()
    AppsV1Api().create_namespaced_deployment(
        namespace="default",
        body=create_deploy()
    )

if __name__ == "__main__":
    main()