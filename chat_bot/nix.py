# server {
#     listen 80;

#     # Server name (your domain name or IP)
#     server_name your-domain.com;

#     location / {
#         proxy_pass http://127.0.0.1:8000;  # Point to your backend application, for example, Django running at localhost:8000
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_redirect off;
#     }
# }
