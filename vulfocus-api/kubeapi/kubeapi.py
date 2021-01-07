#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/6 下午4:33
# software: PyCharm
# project: vulfocus
import re
import time

from kubernetes import client, config
from kubernetes.client import V1ContainerPort
from kubernetes.stream import stream

from vulfocus.settings import KUBE_CONFIG_FILE


class KubeCtl:
    config.kube_config.load_kube_config(config_file=KUBE_CONFIG_FILE)
    V1 = client.CoreV1Api()

    def __init__(self, namespace):
        self.namespace = namespace

    @staticmethod
    def init_pod(namespace, pod_name, image, image_name, ports, command=None):
        pod = client.V1Pod()
        pod.metadata = client.V1ObjectMeta(name=pod_name, namespace=namespace)
        ports = [
            V1ContainerPort(host_port=int(port.split(':')[0]), container_port=int(port.split(':')[1]), protocol='TCP')
            for
            port in ports]
        container = client.V1Container(
            name=image_name,
            image=image,
            ports=ports
        )
        print(f'正在创建pod，主机名为{pod_name}')
        spec = client.V1PodSpec(containers=[container], hostname=pod_name)
        pod.spec = spec
        return pod

    def __create_pod(self, pod_name: str, image: str, image_name: str, ports: list):
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
            print(f'pod_name: {pod_name}\nimage: {image}\nimage_name: {image_name}\nports: {ports}')
            pod = self.init_pod(self.namespace, pod_name, image, image_name, ports)
            KubeCtl.V1.create_namespaced_pod(namespace=self.namespace, body=pod)
            return True, 'success'
        except Exception as e:
            # fixme 记录异常类型并分析解决
            return False, str(e)

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
        try:
            KubeCtl.V1.delete_namespaced_pod(name=name, namespace=self.namespace, body=client.V1DeleteOptions())
            return True, f'pod {name} 删除成功'
        except client.exceptions.ApiException as e:
            if e.status == 404:
                return True, f'pod {name} 删除成功'
            elif e.status == 403:
                return False, 'No Premission'
            else:
                return False, 'Exception'
        except Exception as e:
            return False, f'pod {name} 删除失败，原因：{e}'

    def read_pod_log(self, name):
        try:
            log = KubeCtl.V1.read_namespaced_pod_log(namespace=self.namespace, name=name)
            return log
        except client.exceptions.ApiException as e:
            pass

    def read_pod_status(self, name):
        try:
            status = KubeCtl.V1.read_namespaced_pod_status(namespace=self.namespace, name=name)
            host_ip = status.status.host_ip
            ports = status.spec.containers[0].ports
            phase = status.status.phase
            return phase, host_ip
        except client.exceptions.ApiException as e:
            if e.status == 404:
                return 'Not Found', None
            elif e.status == 403:
                return 'No Premission', None
            else:
                return 'Exception', None
        except Exception as e:
            return False, None

    def create_pod(self, pod_name: str, image: str, image_name: str, ports: list):
        status, msg = self.__create_pod(pod_name, image, image_name, ports)
        phase = None
        host_ip = None
        if status:
            while True:
                time.sleep(10)
                phase, host_ip = self.read_pod_status(pod_name)
                if phase == 'Pending':
                    continue
                else:
                    break
        return status, phase, host_ip, msg

    def exec(self, name, cmds):
        """

        :param name:
        :return:
        """
        try:
            resp = stream(
                KubeCtl.V1.connect_get_namespaced_pod_exec,
                name,
                self.namespace,
                command=cmds,
                stderr=True, stdin=False,
                stdout=True, tty=False
            )
            return resp
        except Exception as e:
            return None


if __name__ == '__main__':
    namespace = 'iast-test'
    ctl = KubeCtl(namespace=namespace)
    # ctl.create_pod(
    #     pod_name='iast-demo01',
    #     image='owef/iast-demo01:latest',
    #     image_name='iast-demo01',
    #     ports=['8080:8080']
    # )

    # ctl.create_pod(
    #     pod_name='shiro-cve-2016-4437',
    #     image='vulhub/shiro:1.2.4',
    #     image_name='shiro/CVE-2016-4437',
    #     ports=['59514:8080']
    # )
    pods = ctl.list_pods()
    if pods:
        for pod in pods:
            print(f'name {pod["name"]}')
            # resp = ctl.exec(
            #     name=pod['name'],
            #     cmds=['curl', f'http://{pod["name"]}.bbc3.showmeshell.com']
            # )
            # print(resp)
            # ctl.del_pod(name=pod['name'])
            log = ctl.read_pod_log(name=pod['name'])
            print(log)
            status = ctl.read_pod_status(name=pod['name'])
            print(status)
    else:
        print('不存在运行中的pod')
