#!/usr/bin/expect
set timeout 5
spawn /opt/xxxxx_UC/sssss_UC_Server/Jre/jre/bin/keytool -import -trustcacerts -alias pupuxsh -file /opt/installer/script/server_auto.cer -keystore /opt/sssss_UC/sssss_UC_Server/Jre/jre/lib/security/cacerts
expect "Enter keystore password:"
send "changeit\r"
expect "Trust this certificate*"
send "yes\r"
interact
