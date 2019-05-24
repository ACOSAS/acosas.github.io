# Acos API Documentation
This is the source for https://acosas.github.io/

Committing changes to this repo will affect the site.

## Theme for Jekyll
This site is based on a theme from [Tom Johnson](https://github.com/tomjoht)<br/>
Site: [Documentation Theme for Jekyll](https://idratherbewriting.com/documentation-theme-jekyll/)


# Making changes

## Download source
- Download the source

## Install Ruby and Jekyll
Windows:
- Enable: Windows Subsystem for Linux , see: https://docs.microsoft.com/nb-no/windows/wsl/install-win10
- Install your linux flavour from Windows Store

Ruby
- Install Ruby on [Ubuntu](https://jekyllrb.com/docs/installation/ubuntu/)
```sh
sudo apt-get install ruby-full build-essential zlib1g-dev
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

gem install jekyll bundler
```

## Update gems
```sh
bundle update    
```

## Serve site
To build any pages from json run:
```sh
# Builds all pages based on json files in _data/swagger folder
./build_site.sh 
```

## Add documentation 
To add a swagger openapi json file to the site 
add the .json file to the _data/swagger/ folder. Add a unique name
Run:
```sh
# from site root folder ./
./build_pages.sh
```
This will produce a [name]_sidebar.yml file and files in ./pages/swagger folder named [name]_[path].md

In index.md file in the root add the newly created _sidebar.yml file to the list of sidebars:
```yml
sidebars: 
    - name: UserAPI_sidebar
    # add sidebars here:
    - name: [name]_sidebar.yml
```
Test and validate changes.

To publish site just push to git.
```ps
git push -u origin master
```
If remote is not added:
```ps
git remote add origin https://github.com/ACOSAS/acosas.github.io.git
```
To generate pages it is developed a gem for producing the files.<br/>
Source: [github](https://github.com/ACOSAS/acos_jekyll_openapi_helper.git)

*Should maybe regiser acos on rubygems.org...*





