import os
import configuration

class remove_user():

	def __init__(self, user):
		self.user = user

	def remove(self):
		os.system("sudo userdel %s" % self.user)
		print "deleted user"
		os.system("sudo rm -r /home/%s" % self.user)
		print "Deleted home dir"
		os.system("sudo groupdel %s-group" % self.user)
		print "Deleted group"

	# removes old users from sshd_config, needs amount of users left in db
	# OBS THIS IS NOT WORKING, WAS JUST AN IDEA
	def fix_ssh_config(self, amount):
		# Create blank(defaulted) ssh config
		with open("/etc/sshd/sshd_config", 'w') as f:
			f.writelines(configuration.ssh_config)
			f.close()
		#create new Match Group for every user still left in database
		for owner in amount:
			owner.name
			with open("/etc/ssh/sshd_config", 'a') as f:
				f.writelines(configuration.sshd % (self.owner, self.owner,))
				f.close()


# Example usage of remove users function
#for x in b:
#	remove_user(x).remove()
