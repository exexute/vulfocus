import shlex

from django.test import TestCase

# Create your tests here.
from kubeapi.kubeapi import KubeCtl

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
            cmd = ['ls', '-l', '/usr/lib/jvm/java-8-openjdk-amd64/jre/']
            cmd = ['ls', '-l', '/usr/lib/jvm/java-8-openjdk-amd64/jre/lib']
            cmd = ['ls', '-l', 'java']
            cmd = ['which', 'java']
            # cmd = ['ps', 'aux']
            resp = ctl.exec(
                name=pod['name'],
                cmds=cmd
            )
            print(resp)
            # break
            ctl.del_pod(name=pod['name'])
        # log = ctl.read_pod_log(name=pod['name'])
        # print(log)
        # status = ctl.read_pod_status(name=pod['name'])
        # print(status)
    else:
        print('不存在运行中的pod')
