
# Mercury
Utilitar pentru convertirea fisierelor .xlsx in .xml pentru SagaC

## Cuprins
1. [Descrierea Proiectului](#descrierea-proiectului)
2. [Tehnologii Folosite](#tehnologii-folosite)
3. [Ghid de instalare](#ghid-de-instalare)

## Descrierea Proiectului
Pentru a usura munca contabililor din Romania ce primesc pe mana mii de facturi de intrari, respectiv iesiri, ce vin in diferite formate(fizic, pdf, xlsx etc), pe luna **Mercury** le primeste centralizate sub forma de **fisier .xlsx** si le transforma intr-un **fisier .xml 100% personalizabil** gata de import intr-unul dintre cele mai folosite programe de contabilitate din Romania, *SagaC*, conform [startingup.ro](https://startingup.ro/programe-de-facturare-si-contabilitate-ideale-pentru-orice-afacere/#:~:text=Printre%20cele%20mai%20căutate%20și,%2C%20SAGA%2C%20FACTURIS%2C%20CONTAZEN.&text=Smart%20Bill%20este%20cel%20mai,facilitățile%20pe%20care%20le%20înglobează.).

## Tehnologii Folosite
* Python - backend
* Django - UI, backend
* openpyxl - citirea fisierelor .xlsx

## Ghid de instalare
Pentru o instalare rapida cu **pipenv** urmariti pasii de mai jos:
** *Python se presupune a fi instalat*
* Pentru a instala *pipenv*:

  Windows
  ```bash
  pip install pipenv
  ```
  Linux based
  ```bash
  pip3 install pipenv
  ```
1. Instalati environmentul deja definit in Pipfile.lock:
    ```bash
    pipenv sync
    ```
2. Activati environmentul:
    ```bash
    pipenv shell
    ```
3. Porniti un server local folosind comanda:

    Windows
    ```bash
    python manage.py runserver
    ```
    Linux based
    ```bash
    python3 manage.py runserver
    ```
    * Puteti specifica adresa IP la care sa se deschida serverul dupa comanda *runserver*.
## FAQ

