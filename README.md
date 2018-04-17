## Watermass Modelling

#### Instructions for loading:

#### You will need: Docker, docker-machine, docker-compose, a clone of this repo, and the woa13.csv file, available here: https://drive.google.com/open?id=1vTjUtVComxNLjOGj2iIL1069qWV27_Fe placed in watermassmodelling2/web 

  1) start docker-machine:
  
          docker-machine start

  2) configure docker-machine:
  
          docker-machine env
          eval $(docker-machine env)

  3) navigate into the clone (where the docker.yml file lives)


  4) Use docker-compose to build the container (go get a coffee, learn to play a song on the guitar...whatever, this will take a bit):
  
          docker-compose build 

  5) Fire up the images: 
  
          docker-compose up -d

#### At this juncture, it may seem like you'll be able to visit something or go somewhere, but that is not so. 

  6) Create the database:
  
          docker-compose run web /usr/local/bin/python create_db.py

#### Now you can ask for the ip address and give it a preliminary and relatively unsatisfying test.

  7) Get ip address from docker-machine:
  
          docker-machine ip

#### For a more satisfying experience, you need to copy the data from woa13.csv into the database.

  8) copy file from local directory to container:
  
          docker cp woa13.csv odm2_postgres_1:./woa13.csv

  9) exec into container postgres instance:
  
          docker exec -ti odm2_postgres_1 psql -U postgres

  10) copy data from csv file to table for specific column list:
  
          \copy woa13s  (index ,  station ,  longitude ,  latitude , depth , temperature , salinity ,  oxygen,  oxygen_saturation , aou , phosphate  , nitrate ) FROM 'woa13.csv' CSV HEADER;

  11) quit postgres:
  
          \q
  
#### With data now in the database, rebuild the container.

  12) rebuild:
  
          docker-compose build
 
#### And once more navigate to the ip address (or reload it--never hurts)



