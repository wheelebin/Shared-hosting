import requests
import json
import time
import os
import configuration
import crypt
import pwd, grp
import random, string

def random_pass():
	randomPswd = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(n))
	return randomPswd

class fix_files():
	
	def __init__(self, folder, domain, owner):
		self.folder = folder
		self.domain = domain
		self.owner = owner

	def create_folder(self):
		# Setup Apache2
		if not os.path.exists(self.folder): 
			os.makedirs(self.folder)
			print "Created folder"
		else:
			print "domain path existed"

		os.system("sudo chown -R $USER:$USER %s" % self.folder)
		os.system("sudo touch index.html")

		config = configuration.virtual_host % (self.owner, self.domain, self.domain, self.domain, self.folder)

		with open("/etc/apache2/sites-available/%s.conf" % self.domain, "w") as f:
			f.write(config)
			f.close()

		os.system("sudo a2ensite %s.conf" % self.domain)
		os.system("sudo service apache2 reload")


	def delete_domain(self):
		if os.path.exists(self.folder): 
			os.system("sudo rm -r /etc/apache2/sites-available/%s.conf" % self.domain)
			os.system("sudo rm -r /etc/apache2/sites-enabled/%s.conf" % self.domain)
			os.system("sudo rm -r /home/%s/%s" % (self.owner, self.domain,))
			os.system("sudo service apache2 reload")
		else:
			print "domain path did not exist. cant delete"

	def add_sftp_user(self, ranPass):
		self.pas = ranPass
		err = None
		try:
			pwd.getpwnam(str(self.owner))
		except KeyError as e:
			print e
			err = "User_does_not_exist"

		if err == "User_does_not_exist":
			#Setup sftp
			with open("/etc/ssh/sshd_config", 'a') as f:
				f.writelines(configuration.sshd % (self.owner, self.owner,))
				f.close()
			os.system("sudo addgroup --system %s-group" % self.owner)
			pas = crypt.crypt(ranPass, "22")
			os.system("sudo useradd --password %s %s" % (pas, self.owner,))
			os.system("sudo usermod -s /bin/false %s" % self.owner)
			os.system("sudo usermod -G %s-group %s" % (self.owner, self.owner,))
			os.system("sudo chown root:root /home/%s" % self.owner)
			os.system("sudo chmod 0755 /home/%s" % self.owner)
			os.system("sudo chmod 777 /home/%s/%s/html" % (self.owner, self.domain))
			os.system("sudo chown %s:%s-group *" % (self.owner, self.owner,))
			os.system("sudo service ssh restart")
			print "Succesfully added user %s" % self.owner
		else:
			print "User already exists!"

	def reset_ftp_pass(self, ranPass):
		pas = ranPass
		pas = crypt.crypt(ranPass, "22")
		os.system("sudo usermod --password %s %s" % (pas, self.owner))



class Handle_dns():

	def __init__(self, domain, type=0):

		self.domain = domain
		self.base_url = "https://api.digitalocean.com/v2/domains/"
		self.header = {
			'Authorization':configuration.token,
			'content-type':'application/json',
		}
		if type == "domains":
			self.type = type
		elif type == "records":
			self.type = type
		elif type == "del":
			self.type = type
		else:
			return "Error"

	def create_domain(self):
		params = {
			'name':self.domain,
			'ip_address':'83.251.139.196',
		}
		r = requests.post(self.base_url, data=json.dumps(params), headers=self.header)
		resp = r.json()
		print resp
		try:
			if resp[u"id"] == 'unprocessable_entity' or resp["id"] == 'not_found':
				return True
			else:
				pass
		except KeyError, e:
			pass
		
	def create_records(self):
		params = {
			'type':'CNAME',
			'name':'www',
			'data':self.domain + ".",
		}
		r = requests.post(self.base_url + self.domain + "/" + self.type, data=json.dumps(params), headers=self.header)
		resp = r.json()
		print resp
		try:
			if resp[u"id"] == 'unprocessable_entity' or resp["id"] == 'not_found':
				return True
			else:
				pass
		except KeyError, e:
			pass

	def del_domain(self):
		r = requests.delete(self.base_url + self.domain, headers=self.header)
		print r


#Handle_dns("joakimallen.se", "domains").create_domain()
#Handle_dns("joakimallen.se", "records").create_records()
#Handle_dns("joakimallen.se", "del").del_domain()