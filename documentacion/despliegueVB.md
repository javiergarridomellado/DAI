## Despliegue en VirtualBox

Para el despliegue en una máquina de VirtualBox he usado [Vagrant](https://www.vagrantup.com/) para su creación y [Ansible](http://www.ansible.com/) para su provisionamiento y despliegue de la aplicación.

El primer paso es instalar el provisionador de azure para vagrant
```
vagrant plugin install vagrant-azure
```

![installvagrantazure](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/installvagranazure_zpsad7pzrjg.png)


El siguiente paso es definir el archivo [Vagrantfile](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/Vagrantfile) que se encarga de la creación de la máquina virtual en VirtualBox:
```
Vagrant.configure('2') do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = 'ubuntu'
  config.vm.network "forwarded_port", guest: 22, host:2222, id: "ssh", auto_correct: true
  config.vm.network "forwarded_port", guest: 80, host:8080, id: "web", auto_correct: true
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
   end

   config.vm.provision "ansible" do |ansible|
      ansible.sudo = true
      ansible.playbook = "iv.yml"
      ansible.verbose = "v"
      ansible.host_key_checking = false
  end
end

```

En el primer bloque lo que hago es indicarle el box que va a usar, en este caso Ubuntu, que haga reenvio de puertos de SSH y Web y le aplico como hostname "localhost" para que Ansible pueda conectar con la máquina.

En el segundo bloque  se ejecuta el "playbook" de Ansible que se llama [iv.yml](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/iv.yml):
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
```

Aquí le indico como hosts "localhost" ya que esto se ejecuta dentro de la máquina.En los task se actualiza el sistema, se instala una base de datos MySQL, un servidor web Nginx con su correspondiente configuración, un servidor web Gunicorn, Supervisor con su correspondiente configuración para monitorizar constantemente el servidor Gunicorn, se instalan los paquetes necesarios de la aplicación, se clona el repositorio y se reinicia los servicios web para que la aplicación quede en modo de producción.

- El servidor web Gunicorn se encarga de servir el contenido dinámico a través del puerto 8000.
- El **watchdog** Supervisor se encarga de monitorizar el servidor Gunicorn para que esté siempre activo.
- El servidor web Nginx se encarga de servir el contenido estático, se configura un proxy para servir a través del 80 lo que sirve Gunicorn.

La configuración de Nginx puede verse [aqui](https://github.com/javiergarridomellado/DAI/blob/master/scripts/webconfiguration/default).

La configuración de Supervisor puede verse [aqui](https://github.com/javiergarridomellado/DAI/blob/master/scripts/webconfiguration/supervisor.conf).

Para realizar el despliegue basta con ejecutar el script [deploy_VB](https://github.com/javiergarridomellado/DAI/blob/master/scripts/deploy_VB.sh) que consta de lo siguiente:
```
#!/bin/bash
git clone https://github.com/javiergarridomellado/DAI.git
cd DAI/VagrantIVLocal/
chmod 777 create_and_run.sh
./create_and_run.sh
```
Puede verse que el último paso es ejecutar el script [create_and_run](https://github.com/javiergarridomellado/DAI/blob/master/VagrantIVLocal/create_and_run.sh) que tiene el siguiente contenido:
```
#!/bin/bash
vagrant box add ubuntu https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box
vagrant up
```
En él se le indica que debe descargar la "box" de Ubuntu y después realizar un "vagrant up". Ejecutado esto vemos como se crea la máquina y se provisiona. 

![ansible](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantlocal_zps95e6qrly.png)

Para visitar la aplicación desplegada solo es necesario usar la url *localhost:8080*:

![appdespl](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/appdesplegadalocal_zpsutxl6mvb.png)

![ssh](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/sshvagrantlocal_zpsjl920y6e.png)


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
