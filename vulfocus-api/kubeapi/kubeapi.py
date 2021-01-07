#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/6 下午4:33
# software: PyCharm
# project: vulfocus

from kubernetes import client, config
from kubernetes.client import V1ContainerPort

from vulfocus.settings import KUBE_CONFIG_FILE


class KubeCtl:
    config.kube_config.load_kube_config(config_file=KUBE_CONFIG_FILE)
    V1 = client.CoreV1Api()

    def __init__(self, namespace):
        self.namespace = namespace

    @staticmethod
    def init_pod(namespace, pod_name, image, image_name, ports):
        pod = client.V1Pod()
        pod.metadata = client.V1ObjectMeta(name=pod_name, namespace=namespace)
        ports = [V1ContainerPort(host_port=port.split(':')[0], container_port=port.split(':')[1], protocol='TCP') for
                 port in ports]
        container = client.V1Container(
            name=image_name,
            image=image,
            ports=ports
        )
        spec = client.V1PodSpec(containers=[container])
        pod.spec = spec
        return pod

    def create_pod(self, pod_name: str, image: str, image_name: str, ports: list):
        """
        example:
        ctl = KubeCtl(namespace=namespace)
        ctl.create_pod(
            pod_name='pod_name',
            image='',
            image_name='',
            ports=['8080:8080','8081:8081']
        )
        """
        try:
            pod = self.init_pod(namespace, pod_name, image, image_name, ports)
            KubeCtl.V1.create_namespaced_pod(namespace=self.namespace, body=pod)
            return True
        except Exception as e:
            # fixme 记录异常类型并分析解决
            return False

    def stop_pod(self, pod_name):
        pass

    def list_pods(self):
        try:
            ret = KubeCtl.V1.list_namespaced_pod(namespace=self.namespace)
            pods = list()
            for i in ret.items:
                pods.append({
                    'ip': i.status.pod_ip,
                    'status': i.status.phase,
                    'name': i.metadata.name,
                    'namespace': i.metadata.namespace
                })
            return pods
        except client.exceptions.ApiException as e:
            if e.status == 404:
                return 'Not Found'
            elif e.status == 403:
                return 'No Premission'
            else:
                return 'Exception'

    def del_pod(self, name):
        KubeCtl.V1.delete_namespaced_pod(name=name, namespace=self.namespace, body=client.V1DeleteOptions())

    def read_pod_log(self, name):
        try:
            log = KubeCtl.V1.read_namespaced_pod_log(namespace=self.namespace, name=name)
            return log
        except client.exceptions.ApiException as e:
            pass

    def read_pod_status(self, name):
        try:
            status = KubeCtl.V1.read_namespaced_pod_status(namespace=self.namespace, name=name)
            return status.status.phase
        except client.exceptions.ApiException as e:
            if e.status == 404:
                return 'Not Found'
            elif e.status == 403:
                return 'No Premission'
            else:
                return 'Exception'


if __name__ == '__main__':
    namespace = 'iast-test'
    ctl = KubeCtl(namespace=namespace)
    # ctl.create_pod(
    #     pod_name='iast-demo01',
    #     image='owef/iast-demo01:latest',
    #     image_name='iast-demo01',
    #     ports=['8080:8080']
    # )
    pods = ctl.list_pods()
    # ctl.del_pod(name='iast-demo01')
    ctl.read_pod_log(name='iast-demo01')
    status = ctl.read_pod_status(name='iast-demo01')
    print(status)
