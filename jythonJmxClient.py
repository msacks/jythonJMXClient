# jythonJmxClient.py
# Jython Script for gathering metrics via JMX via command line interface
# matthew@thebitsource.com
# Licensed under the Apache License (AL2)
# v 0.2.0
#

#Java Dependencies
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import java.lang.management.ManagementFactory;

#Python Dependencies
import sys, cmd, socket, optparse
from urlparse import urljoin
from cmd import Cmd

class jmxCmd(Cmd):
	prompt = 'jymx> '

	def do_connect(self, line):
		#annoying option parsing stuff
		parser = optparse.OptionParser(conflict_handler="resolve")
		parser.add_option('-h', '--hostip', dest='host')
		parser.add_option('-p', '--portnum', dest='port')
		(options, args) = parser.parse_args(line.split())
	
		options.port = int(options.port)

		print "Host: ", type(options.host)
		print "Port: ", type(options.port)
		
		connectionArgs = ((options.host,options.port))
		
		#Test Connection Arguments
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(connectionArgs)
			s.close()
		except socket.error, (value,message):
			if s:
				s.close()
			print "Could not open connection: " + message
			sys.exit(1)

		#Establish Connection to JMX Server
		serviceURL = str()
		serviceURL = "service:jmx:rmi:///jndi/rmi://"
		serviceURL = serviceURL + options.host + ":" + str(options.port) + "/jmxrmi"
		
		#DEBUG
		print options.host, options.port, serviceURL

		url =  javax.management.remote.JMXServiceURL(serviceURL);
		connector = javax.management.remote.JMXConnectorFactory.connect(url);
		global remote
		remote = connector.getMBeanServerConnection();
		
	def do_getDomains(self, line):
		domainList = []
		domainList = remote.getDomains()
		
		for element in domainList:
			print element

	#def do_getAttribute(self, line):
		
	#	obn =  javax.management.ObjectName("java.lang:type=Memory");
	#	result = remote.getAttribute(obn,"HeapMemoryUsage");

	def do_quit(self, arg):
        	print("bye.")
       		return True    
	
	default_to_shell = True


if __name__ == '__main__':
	jmxCmd().cmdloop()		
