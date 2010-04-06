# jythonJmxClient.py
# Jython Script for gathering metrics via JMX via command line interface
# matthew@thebitsource.com
# Licensed under the Apache License (AL2)
# v 0.2.1
# NOTE: Commands may also be passed as a script, just store commands as a text file and feed it to the parser

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
	prompt = 'jmx> '
	intro = "Simple Command-line JMX Client"

	def do_connect(self, line):
                """connect -h|--hostip <hostname or ip_addr> -p|--portnum <port>
                Establish a connection to the JMX Server. Uses jmxrmi protocol by default"""
		
		#annoying option parsing stuff
		parser = optparse.OptionParser(conflict_handler="resolve")
		parser.add_option('-h', '--hostip', dest='host')
		parser.add_option('-p', '--portnum', dest='port')
		(options, args) = parser.parse_args(line.split())
	
		options.port = int(options.port)
		
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
		
		url =  javax.management.remote.JMXServiceURL(serviceURL);
		connector = javax.management.remote.JMXConnectorFactory.connect(url);
		global remote
		remote = connector.getMBeanServerConnection();
		
	def do_getDomains(self, line):
                """getDomains 
                Retrieve a list of all available JMX Domains"""

		domainList = []
		domainList = remote.getDomains()
		
		for element in domainList:
			print element

	def do_getAttribute(self, line):
                """getAttribute -m|--mbeanpath <path to mbeanr> -a|--attribute <name of attribute>
                Query the mbean server for a specific attribute and return the result"""

		#annoying option parsing stuff - need cmd2
		parser = optparse.OptionParser(conflict_handler="error")
		parser.add_option('-m', '--mbeanpath', dest='mbp', type='string')
		parser.add_option('-a', '--attribute', dest='attr')
		(options, args) = parser.parse_args(line.split())
		
		obn =  javax.management.ObjectName(options.mbp);
		result = remote.getAttribute(obn, options.attr);

		print result		
	
	def do_quit(self, arg):
        	print("bye.")
       		return True    

			
	default_to_shell = True

if __name__ == '__main__':
	jmxCmd().cmdloop()		
