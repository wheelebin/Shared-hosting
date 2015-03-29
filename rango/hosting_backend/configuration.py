virtual_host = """<VirtualHost *:80>
	ServerAdmin %s@%s
	ServerName %s
	ServerAlias www.%s
	DocumentRoot %s
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>"""

sshd = """
Match group %s-group
    ChrootDirectory /home/%s
    X11Forwarding no
    AllowTcpForwarding no
    ForceCommand internal-sftp"""

token = "Bearer TOKEN GOES HERE"

ssh_config = """
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 768
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin yes
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
X11Forwarding yes
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp internal-sftp
UsePAM yes
UseDNS no


"""

