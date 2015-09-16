# Talkie_Nedap Script alarme kalkie Nedap
2015-09-16
Mise en ligne initial du script écrit par Sarakha63.



# INSTALLATION :

Depuis dossier de l'utilisateur principal :
wget -O - https://raw.githubusercontent.com/alois66/Talkie_Nedap/master/install.sh | bash



# UTILISATION

http://IPBOX:4001/post/phrase=xx&jingle=xx&lang=xx
exemple : http://192.168.134.10:4001/post/phrase=antivol%20caisse%20douze&jingle=pager&lang=FR

"phrase" = phrase à envoyer

"jingle" = urgence, alarme, pager, 0(pas de jingle)

"lang" = DE, GB, US, ES, FR, IT



# DEBUG

Pour contôler l'état de fonctionnement depuis un navigateur :
http://IPBOX:4001/hello 

Pour contôler l'état des GPIO depuis un navigateur :
http://IPBOX:4001/gpio-read
