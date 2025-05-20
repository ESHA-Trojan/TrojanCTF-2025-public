FROM php:8.1-apache
RUN useradd -m -d /home/ctfuser -s /bin/bash ctfuser
WORKDIR /var/www/html
COPY . /var/www/html

# Securely create the flag file
RUN mkdir -p /home/ctfuser && \
    echo "Trojan{f1Ve_mIni_buRg3r5-equ@lS-4_mixed-piZzZas}" > /home/ctfuser/flag.txt && \
    chmod 400 /home/ctfuser/flag.txt && \
    chown ctfuser:ctfuser /home/ctfuser/flag.txt

# Install sudo and allow ONLY `sudo -u ctfuser cat /home/ctfuser/flag.txt`
RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/* && \
    echo "www-data ALL=(ctfuser) NOPASSWD: /bin/cat /home/ctfuser/flag.txt" > /etc/sudoers.d/ctf && \
    chmod 440 /etc/sudoers.d/ctf

# Change ownership of web files to www-data
RUN chown -R www-data:www-data /var/www/html

# Expose port 80
EXPOSE 80

# Start Apache
CMD ["apache2-foreground"]
