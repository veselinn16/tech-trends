# set up the default terminal
ENV["TERM"]="linux"

Vagrant.configure("2") do |config|
  
  # set the image for the vagrant box
  # Used ubuntu because I was facing installation problems on suse.
  config.vm.box = "bento/ubuntu-18.04"
  ## Set the image version
  #config.vm.box_version = "15.2.31.473"

  # st the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.5"
  
  # consifure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.name = "kubemaster"
    vb.memory = "2048"
    vb.cpus = 2
    # vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
