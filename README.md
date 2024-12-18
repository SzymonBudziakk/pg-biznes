# Projekt: Tworzenie sklepu internetowego z wykorzystaniem PrestaShop

## Opis projektu:

Celem projektu jest praktyczne zastosowanie wiedzy dotyczącej stosowania, konfiguracji i wdrożenia oprogramowania Open Source do tworzenia sklepów internetowych. Porojekt ma na celu skopiowanie sklepu internetowego (https://wloczykijki.pl/) wraz z jego produktami.

---

## Użyte oprogramowanie:

- PrestaShop 1.7.8 (https://github.com/PrestaShop/PrestaShop/tree/1.7.8.x)
- Docker (https://www.docker.com/)
- DockerCompose (https://docs.docker.com/compose/)
- Selenium (https://www.selenium.dev/documentation/)
- Robot Framework (https://robotframework.org/)
- MySql 5.7 (https://hub.docker.com/_/mysql)

---

## Sposób uruchomienia:

1. Klonowanie repozytorium
   [w konsoli]
   git clone https://github.com/SzymonBudziakk/pg-biznes
   cd pg-biznes

2. Uruchomienie kontenerów
   [w konsoli]
   docker compose -f config/docker-compose.yml up --build

3. Wejście na stronę
   [w przeglądarce]
   localhost:8080

---

## Skład zespołu

- Olivier Stankiewicz
- Kamil Cwynar
- Norbert Zakrzewski
- Szymon Budziak
