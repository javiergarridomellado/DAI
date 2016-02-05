## Despliegue en un Iaas: Azure

Para el despliegue en una máquina de Azure he usado [Vagrant](https://www.vagrantup.com/) para su creación y [Ansible](http://www.ansible.com/) para su provisionamiento y despliegue de la aplicación.

El primer paso es instalar el provisionador de azure para vagrant
```
vagrant plugin install vagrant-azure
```

![installvagrantazure](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/installvagranazure_zpsad7pzrjg.png)

El siguiente paso es loguearse y conseguir información de las credenciales de Azure (al ejecutar **azure account download** hay que acceder al enlace que nos facilita):
```
azure login
azure account download
```

Acto seguido importo a mi CLI de Azure mis credenciales:
```
azure account import Azure\ Pass-1-15-2016-credentials.publishsettings
```

![importarcredenciales](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/azureimport_zpsfwwiqjcc.png)


El siguiente paso es generar los certificados que se van a subir a Azure y nos va a permitir interaccionar con el:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azurevagrant.key -out azurevagrant.key
chmod 600 ~/.ssh/azurevagrant.key
openssl x509 -inform pem -in azurevagrant.key -outform der -out azurevagrant.cer
```

El siguiente paso es subir el archivo **.cer** a [Azure](https://manage.windowsazure.com/@franciscojaviergarmelhotmai.onmicrosoft.com#Workspaces/AdminTasks/ListManagementCertificates):


![certificado](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/subircredencial_zpshfktx7xg.png)

Para poder autenticar Azure desde Vagrantfile es necesario crear un archivo **.pem** y concatenarle el archivo **.key**, para ello:
```
openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out azurevagrant.pem
cat azurevagrant.key > azurevagrant.pem
```

Realizado estos pasos se procede a definir el archivo [Vagrantfile](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIV/Vagrantfile) que se encarga de la creación de la máquina virtual en Azure:
```
Vagrant.configure('2') do |config|
  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.56.101", virtualbox__intnet: "vboxnet0"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
   end

  config.vm.provider :azure do |azure, override|
      azure.mgmt_certificate = File.expand_path('/home/javi/Escritorio/VagrantIV/azurevagrant.pem') 
      azure.mgmt_endpoint = 'https://management.core.windows.net'
      azure.subscription_id = '477d87d6-b8d0-4025-8c1f-a3de5c520c99'
      azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB'
      azure.vm_name = 'restaurante'
      azure.cloud_service_name = 'restaurantejaviergarrido' 
      azure.vm_password = 'Clave#Javi#1'
      azure.vm_location = 'Central US' 
      azure.ssh_port = '22'
      azure.tcp_endpoints = '80:80'
  end	

  config.vm.provision "ansible" do |ansible|
      ansible.sudo = true
        ansible.playbook = "iv.yml"
        ansible.verbose = "v"
        ansible.host_key_checking = false
  end
end

```

En el primer bloque lo que hago es indicarle el box que va a usar, en este caso Azure, que tenga acceso a Internet mediante una red pública, una red privada, que haga reenvio de puertos y le aplico como hostname "localhost" para que Ansible pueda conectar con la máquina.

En el segundo bloque se configuran las propiedades de mi servicio de Azure, se le indica la ruta del certificado de Azure, el "endpoint", la imagen Ubuntu que va a usar, el nombre de la máquina, el nombre del cloud,la password,etc.

Por último, se ejecuta el "playbook" de Ansible que se llama [iv.yml](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/iv.yml):
```
- hosts: localhost
  sudo: yes
  remote_user: vagrant
  vars:
    mysql_root_password: 
  tasks:
  - name: Actualizar sistema 
    apt: update_cache=yes upgrade=dist 
  - name: Install MySQL
    apt: name={{ item }} update_cache=yes cache_valid_time=3600 state=present
    sudo: yes
    with_items:
    - python-mysqldb
    - mysql-server
  - name: Arrancar servicio MySQL 
    sudo: yes
    service: 
      name: mysql 
      state: started
      enabled: true
  - name: actualizacion password root mysql
    sudo: yes
    mysql_user: 
      name: root 
      host: "{{ item }}" 
      password: "{{ mysql_root_password }}"
      login_user: root
      login_password: "{{ mysql_root_password }}"
      check_implicit_admin: yes
      priv: "*.*:ALL,GRANT"
    with_items:
      - "{{ ansible_hostname }}"
      - 127.0.0.1
      - ::1
      - localhost 
  - name: Instalar paquetes
    apt: name={{ item }} update_cache=yes cache_valid_time=3600 state=present
    sudo: yes
    with_items:
    - python-setuptools
    - build-essential 
    - python-pip
    - git 
  - name: Instalar servidor Gunicorn
    command: sudo pip install gunicorn
  - name: Instalar servidor Nginx y supervisor
    apt: name={{ item }} update_cache=yes cache_valid_time=3600 state=present
    sudo: yes
    with_items:
    - nginx
    - supervisor  
  - name: Conector Postgre Heroku
    command: sudo easy_install pip
    command: sudo pip install --upgrade pip
    command: sudo apt-get install -y python-dev libpq-dev python-psycopg2
  - name: Obtener aplicacion git
    git: repo=https://github.com/javiergarridomellado/DAI.git  dest=DAI clone=yes force=yes
  - name: Permisos de ejecucion
    command: chmod -R +x DAI
  - name: Instalar requisitos
    command: sudo pip install -r DAI/requirements.txt
  - name: Crear www 
    command: sudo mkdir -p /var/www
  - name: Copiar static
    command: sudo cp -r DAI/static/ /var/www/
  - name: Copiar media
    command: sudo cp -r DAI/media/ /var/www/
  - name: Conf supervisor
    command: sudo mv DAI/scripts/webconfiguration/supervisor.conf /etc/supervisor/conf.d/
  - name: Conf nginx
    command: sudo mv DAI/scripts/webconfiguration/default /etc/nginx/sites-available/
  - name: crear bd
    command: mysqladmin  -h localhost -u root  create vagrant
  - name: app configuracion produccion 
    command: sudo mv DAI/ProyectoDAI/settings.py DAI/ProyectoDAI/bak_settings.py
    command: sudo mv DAI/ProyectoDAI/bak2_settings.py DAI/ProyectoDAI/settings.py
  - name: sincro bd
    command: sudo python DAI/manage.py syncdb --noinput
  - name: update bd
    command: sudo python DAI/populate_restaurante.py
  - name: Reiniciar Supervisor 
    sudo: yes
    service: 
      name: supervisor 
      state: restarted
      enabled: true
  - name: Reiniciar Nginx 
    sudo: yes
    service: 
      name: nginx 
      state: restarted
      enabled: true
    #command: sudo service nginx restart
    #command: sudo service supervisor restart
  #- name: ejecutar
    #command: nohup sudo python DAI/manage.py runserver 0.0.0.0:80

```

Aquí le indico como hosts "localhost" ya que esto se ejecuta dentro de la máquina.En los task se actualiza el sistema, se instala una base de datos MySQL, un servidor web Nginx con su correspondiente configuración, un servidor web Gunicorn, Supervisor con su correspondiente configuración para monitorizar constantemente el servidor Gunicorn, se instalan los paquetes necesarios de la aplicación, se clona el repositorio y se reinicia los servicios web para que la aplicación quede en modo de producción.

- El servidor web Gunicorn se encarga de servir el contenido dinámico a través del puerto 8000.
- El **watchdog** Supervisor se encarga de monitorizar el servidor Gunicorn para que esté siempre activo.
- El servidor web Nginx se encarga de servir el contenido estático, se configura un proxy para servir a través del 80 lo que sirve Gunicorn.

La configuración de Nginx puede verse [aqui](https://github.com/javiergarridomellado/DAI/blob/master/scripts/webconfiguration/default).

La configuración de Supervisor puede verse [aqui](https://github.com/javiergarridomellado/DAI/blob/master/scripts/webconfiguration/supervisor.conf).
 

Para realizar el despliegue basta con ejecutar el script [deploy_Azure](https://github.com/javiergarridomellado/DAI/blob/master/scripts/deploy_Azure.sh) que consta de lo siguiente:
```
#!/bin/bash
git clone https://github.com/javiergarridomellado/DAI.git
cd DAI/VagrantIV/
chmod 777 create_and_run.sh
./create_and_run.sh
```
Puede verse que el último paso es ejecutar el script [create_and_run](https://github.com/javiergarridomellado/DAI/blob/master/VagrantAzure/create_and_run.sh) que tiene el siguiente contenido:
```
#!/bin/bash
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
```
En él se le indica que debe descargar la "box" de Azure y después realizar un "vagrant up" (vagrant up --provider=azure). Ejecutado esto vemos como se crea la máquina y se provisiona. 

![ansible](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantazure_zps3fcm3fc4.png)

El enlace a la aplicación es el siguiente [http://restaurantejaviergarrido.cloudapp.net/restaurante/](http://restaurantejaviergarrido.cloudapp.net/restaurante/)

![appdespl](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/appdespleazure_zpsnfuqelxh.png)

![ssh](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/sshvagrantazure_zpscbxtkuca.png)


*Nota: Para su correcto funcionamiento es necesario tener instalado lo siguiente :*
```
$ sudo apt-get install nodejs-legacy
$ sudo apt-get install npm
$ sudo npm install -g azure-cli
$ sudo pip install paramiko PyYAML jinja2 httplib2 ansible
$ sudo dpkg -i vagrant_1.8.1_x86_64.deb
$ vagrant plugin install vagrant-azure
```

Se proporciona para mayor comodidad el script [install_tools.sh](https://github.com/javiergarridomellado/DAI/blob/master/scripts/install_tools.sh)



