# Jython Script for gathering metrics via JMX
# matthew@matthewsacks.com
# Licensed under the Apache License (AL2)

import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import java.lang.management.ManagementFactory;

import sys,cmd
from urlparse import urljoin

#TODO: Replace sys with cmd option parsing

host = sys.argv[1]
port = sys.argv[2]

serviceURL = "service:jmx:rmi:///jndi/rmi://"
serviceURL = serviceURL + host + ":" + port + "/jmxrmi"

url =  javax.management.remote.JMXServiceURL(serviceURL);

connector = javax.management.remote.JMXConnectorFactory.connect(url);
remote = connector.getMBeanServerConnection();

obn =  javax.management.ObjectName("java.lang:type=Memory");
#remoteRuntime = java.lang.management.ManagementFactory.newPlatformMXBeanProxy(remote,ManagementFactory.RUNTIME_MXBEAN_NAME,RuntimeMXBean.class);
result = remote.getAttribute(obn,"HeapMemoryUsage");

print result

