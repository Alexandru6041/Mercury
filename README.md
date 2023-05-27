
# Mercury
Utilitar pentru convertirea fisierelor .xlsx in .xml pentru SagaC

## Cuprins
1. [Descrierea Proiectului](#descrierea-proiectului)
2. [Tehnologii Folosite](#tehnologii-folosite)
3. [Arhitectura Aplicatiei](#arhitectura-aplicatiei)
4. [Ghid de instalare](#ghid-de-instalare)

## Descrierea Proiectului
Pentru a usura munca contabililor din Romania ce primesc pe mana mii de facturi de intrari, respectiv iesiri, ce vin in diferite formate(fizic, pdf, xlsx etc), pe luna **Mercury** le primeste centralizate sub forma de **fisier .xlsx** si le transforma intr-un **fisier .xml 100% personalizabil** gata de import intr-unul dintre cele mai folosite programe de contabilitate din Romania, *SagaC*, conform [startingup.ro](https://startingup.ro/programe-de-facturare-si-contabilitate-ideale-pentru-orice-afacere/#:~:text=Printre%20cele%20mai%20căutate%20și,%2C%20SAGA%2C%20FACTURIS%2C%20CONTAZEN.&text=Smart%20Bill%20este%20cel%20mai,facilitățile%20pe%20care%20le%20înglobează.).

## Tehnologii Folosite
* Python - backend
* Django - UI, backend
* openpyxl - citirea fisierelor .xlsx
* bootstrap - frontend
* argon2 - criptare/hashing, backend

## Arhitectura Aplicatiei
Proiectul este structurat pe extensii(folder: converter, main) adaugate la aplicatia principala(folder: Mercury)
  ### Front End - bootstrap
  Fisierele *html* puse in folderele *templates* ale fiecarei extensii sunt randate de **DJANGO** si fisierele *css* sunt incarcate prin URLuri:
  ```html
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
  ```
  
  ### Back End - python, DJANGO
  Aplicatia foloseste frameworkul **DJANGO** pentru partea de backend a serverului. Requesturile sunt preluate si trimise catre functiile de *views* aferente urlurilor accesate si apoi sunt procesate si sunt randate template-urile *html*. Extensia [*converter*](https://github.com/Alexandru6041/Mercury/tree/main/converter) implementeaza functii proprii pentru a procesa fisierele *xlsx* incarcate de utilizator, folosindu-se de biblioteca **openpyxl** pentru a citi fisierele, din care extrag datele necesare pentru creerea rezultatelor *xml*.
  ### Baza de date - sqlite3
  Aplicatia foloseste o baza de date sqlite3 structurata de **DJANGO** in care sunt salvate datele utilizatorilor, grupurile de utilizatori si fisierele xlsx incarcate de utilizator. Aceasta are o interactiune directa cu interfata de *admin a site-ului* prin care se pot face interogari, modificari si stergeri in functie de permisiunile acordate fiecarui utilizator.
    


## Ghid de instalare
1. Pentru a instala librariile aditionale folosite rulati comanda:
    
    Windows
    ```bash
    pip install -r requirements.txt
    ```
    Linux based
    ```bash
    pip3 install -r requirements.txt
    ```
2. Porniti un server local folosind comanda:

    Windows
    ```bash
    python manage.py runserver
    ```
    Linux based
    ```bash
    python3 manage.py runserver
    ```
    * Puteti specifica adresa IP la care sa se deschida serverul dupa comanda *runserver*.

