server {
    listen 80;
    server_name groep22.webdev.ilabt.imec.be;

    if ($request_method = GET) {
        return 301 https://$server_name$request_uri;
    }

    return 308 https://$server_name$request_uri;

    include snippets/letsencrypt.conf;
}

server {
    listen 443 ssl http2;
    server_name groep22.webdev.ilabt.imec.be;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/resto/RestoWeb/server/restoweb.sock;
    }

    ####################
    # SSL OPTIONS
    ####################
    include snippets/letsencrypt.conf;
    include snippets/ssl_options.conf;
    ssl_certificate /home/groep22/.acme.sh/groep22.webdev.ilabt.imec.be/fullchain.cer;
    ssl_certificate_key /home/groep22/.acme.sh/groep22.webdev.ilabt.imec.be/groep22.webdev.ilabt.imec.be.key;
}
