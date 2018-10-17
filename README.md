# PiDev
Development Repo to test code chunks on mounted pis

Demonstration pi code being installed is currently stored [here](https://github.com/dronology-outdoor/PiDronology.git)

## Create new pi:
* Login to resin.io with outdoor account
* Click on Dronology application and download and image
* Unzip image and for easy copy to SD card use [etcher](https://etcher.io/)
* Plug SD card into pi, power up, and connect pi to the internet via ethernet cable (either by plugging directly into a open network port - like your home router - or by sharing your laptop's wifi connection via its ethernet port).
* Pi will access the resin repos and update itself - you can see it connect and update on the resin dashboard - let it finish before disconnecting.

## To develop:
* Add your public sshkey to the resin account
* Clone this repo
* Make your changes and push to BOTH:
  - This repo for archive and code sharing: 
  ```bash
  $ git push master
  ```
  - The resin repo to cause applications on ALL pis to update whenever pis are connected to the internet as above
  ```bash
  $ git push resin
  ```
  - Push to resin will cause a recompile and update on their servers which you will see the output from and can debug errors this way before going to connect pis for release updates
  
  

